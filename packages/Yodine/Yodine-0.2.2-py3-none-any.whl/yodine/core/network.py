from .entity import Manager, Component, Entity
from .vector import Vector
from typing import Callable

import time
import uuid
import socket
import trio
import pyglet

try:
    import simplejson as json

except ImportError:
    import json



class MultiplayerError(BaseException):
    pass

class MultiplayerProtocolError(MultiplayerError):
    pass

class MultiplayerUserError(MultiplayerError):
    pass


def dump_arg(arg):
    if isinstance(arg, Vector):
        return { 't': 'vec', 'coord': [arg.x,arg.y] }

    elif isinstance(arg, Component):
        return { 't': 'cmp', 'eid': arg.entity.id, 'name': arg.name, 'value': arg.value }

    elif isinstance(arg, Entity):
        return { 't': 'ent', 'eid': arg.id }

    elif isinstance(arg, pyglet.window.BaseWindow):
        return { 't': 'wnd' }

    elif isinstance(arg, list):
        return { 't': 'lst', 'values': [dump_arg(a) for a in arg] }

    elif isinstance(arg, tuple):
        return { 't': 'tpl', 'values': [dump_arg(a) for a in arg] }

    elif isinstance(arg, dict):
        return { 't': 'dct', 'items': { k: dump_arg(v) for k, v in arg.items() } }

    return { 't': '', 'value': arg }


class Client(object):
    def __init__(self, game: '..game.Game', server_addr):
        self.game = game
        self.manager = game.manager
        self.client = socket.create_connection(server_addr)
        self.client.setblocking(False)
        self.addr = server_addr
        self.players = {}
        self.events = []
        self.writes = []
        self.buffer = b''
        self.outbound = b''
        self.running = True

        self.last_server_state = Manager(self.game, self.game.window)
        self.last_server_state.tile_types = self.manager.tile_types
        self.last_server_state.loader = self.manager.loader

    def send(self, command, *args):
        self._write('\x00'.join([command, *(json.dumps(dump_arg(a)) for a in args)]).encode('utf-8') + b'\n')

    def emit(self, source, name, *args, **kwargs):
        self.send('BROADCAST', source.id, name, args, kwargs)

    def stop(self):
        self._write(b'LEAVE\n')
        self.client.close()

        self.running = False

    def load_arg(self, arg):
        if arg['t'] == 'vec':
            return Vector(arg['coord'])

        elif arg['t'] == '':
            return arg['value']

        elif arg['t'] == 'cmp':
            e = self.manager.find_entity(arg['eid'])

            if arg['name'] in e:
                c = e[arg['name']]
                c.force_set(arg['value'])

            else:
                c = Component(e, arg['name'], arg['value'])
                e.level.entity_component_index[e.id][c.name] = c

            return c

        elif arg['t'] == 'ent':
            return self.manager.find_entity(arg['eid'])

        elif arg['t'] == 'wnd':
            return self.manager.window

        elif arg['t'] == 'lst':
            return [self.load_arg(a) for a in arg['values']]

        elif arg['t'] == 'tpl':
            return tuple([self.load_arg(a) for a in arg['values']])

        elif arg['t'] == 'dct':
            return { k: self.load_arg(v) for k, v in arg['items'].items() }
        
        else:
            raise ValueError("Unknown JSON argument type: {}".format(repr(arg['t'])))

    def process_writes(self):
        nw = []

        for when, data in self.writes:
            self.outbound += data

        self.writes = nw

    def _write(self, data):
        #self.outbound += data
        self.writes.append((time.time(), data))

    async def run(self):
        self.running = True        
        self.buffer = b''

        commands = {}

        def command(name):
            def _decorator(func):
                commands[name.upper()] = func
                
                return func
            return _decorator

        self.ignore_events_until = 0

        @command('DELTA')
        def receive_delta(*changes):
            # print('Received changes!')

            for change in changes:
                args = change[1:]

                if change[0] == 'set':
                    eid, cname, cval = args
                    self.last_server_state[eid][cname] = cval

                elif change[0] == 'mkc':
                    eid, cname, cval, ckind = args
                    self.last_server_state[eid].create_component(cname, cval, ckind)

                elif change[0] == 'del':
                    eid, cname = args

                    e = self.last_server_state[eid]
                    
                    if cname in e:
                        del e[cname]

                elif change[0] == 'crt':
                    eid, level = args

                    if level is None:
                        e = self.last_server_state.create_entity([], eid)

                    else:
                        e = self.last_server_state.levels[level].create_entity([], eid)

                elif change[0] == 'dsp':
                    eid, = args
                    self.last_server_state[eid].remove()

                elif change[0] == 'tsf':
                    eid, level = args

                    if level is None:
                        self.last_server_state[eid].transfer(self.last_server_state)

                    else:
                        self.last_server_state[eid].transfer(self.last_server_state.levels[level])

                elif change[0] == 'clv':
                    level, = args

                    self.last_server_state.change_level(level)
                    self.manager.change_level(level)

                elif change[0] == 'nlv':
                    level, save = args

                    if level not in self.last_server_state.levels:
                        self.last_server_state.add_level_save(level, save)
                        self.manager.add_level_save(level, save)

            if changes:
                self.last_server_state.update(self.manager)

        #@command('EVENT')
        #def receive_broadcast_event(when, local, source, event_name, args, kwargs):
        #    if when <= self.ignore_events_until:
        #        return
        #
        #    if time.time() - when < 1 / 4:
        #        self.manager.emit_local(source, event_name, local, *args, **kwargs)
        #
        #    elif time.time() - when > 2:
        #        self.ignore_events_until = time.time()
        #        self.send('SNAPSHOT')

        @command('ERR')
        def got_error(code, err):
            category = str(code)[0]
            msg = 'Status code {}: {}'.format(code, err)
            
            if category == '1':
                raise MultiplayerProtocolError(msg)

            elif category == '2':
                raise MultiplayerUserError(msg)

            else:
                raise MultiplayerError(msg)

        @command('INIT_LEVELS')
        def init_levels(start, *levels):
            del self.manager.levels
            self.manager.levels = {}

            for v in levels:
                lid = v['lid']
                assert 'deltas' in v

                self.manager.add_level_save(lid, v)
                self.last_server_state.add_level_save(lid, v)

            self.manager.change_level(start)
            self.last_server_state.change_level(start)

            print('Received levels.')

        #@command('JOINED')
        #def on_joined(local, v):
        #    eid = v['eid']
        #    level = v.get('level', None)
        #    components = v['components']
        #
        #    print(local, 'is joining our party!')
        #
        #    if level:
        #        e = self.manager.levels[level].create_entity(components, eid)
        #
        #    else:
        #        e = self.manager.create_entity(components, eid)
        #
        #    if e.has('name', 'localplayer'):
        #        self.players[e['name'].value] = e

        @command('INIT_ENTITIES')
        def init_entities(*entities):
            for e in self.manager:
                e.remove()

            for e in self.last_server_state:
                e.remove()

            for v in entities:
                eid = v['eid']
                level = v.get('level', None)
                components = v['components']

                if level:
                    self.last_server_state.levels[level].create_entity(components, eid)
                    self.manager.levels[level].create_entity(components, eid)

                else:
                    self.last_server_state.create_entity(components, eid)
                    self.manager.create_entity(components, eid)

            print('Received entities.')

        @command('RNG')
        def set_rng_state(*state):
            self.game.random.setstate(state)
            print('Received RNG state.')

        async def _recv(data):
            self.buffer += data
            lines = self.buffer.split(b'\n')
            self.buffer = lines[-1]

            for data in lines[:-1]:
                try:
                    data = data.decode('utf-8')

                except UnicodeDecodeError:
                    print(data)
                    raise

                keycode = data.split('\x00')[0]
                values = [self.load_arg(json.loads(a)) for a in data.split('\x00')[1:]]

                if keycode.upper() in commands:
                    commands[keycode.upper()](*values)

        print('Joining...')
        self.send('JOIN', self.game.id, self.game.player_name)

        while self.events:
            e = self.events.pop(0)
            self.send_event(e)
        
        self.events = None

        async with trio.open_nursery() as nursery:
            while self.running:
                sleep_amount = 1 / 30
                data = b''

                try:
                    data = self.client.recv(8192)

                    if data == b'':
                        self.stop()
                        return

                    else:
                        nursery.start_soon(_recv, data)

                except ConnectionResetError:
                    self.stop()
                    return

                except BlockingIOError:
                    sleep_amount = 1 / 20

                self.process_writes()

                try:
                    sent = self.client.send(self.outbound)

                except BlockingIOError:
                    pass

                else:
                    self.outbound = self.outbound[sent:]

                    if self.outbound or len(data) == 8192:
                        sleep_amount = 1 / 60
                    
                await trio.sleep(sleep_amount)

            self.outbound = b''
            

class Server(object):
    def emit(self, source, event_name, *args, **kwargs):
        for sess in self.clients.keys():
            self.send(sess, 'EVENT', self.game.id, source, event_name, args, kwargs)

    def load_arg(self, arg):
        if arg['t'] == 'vec':
            return Vector(arg['coord'])

        elif arg['t'] == '':
            return arg['value']

        elif arg['t'] == 'cmp':
            e = self.manager.find_entity(arg['eid'])

            if arg['name'] in e:
                c = e[arg['name']]
                c.force_set(arg['value'])

            else:
                c = Component(e, arg['name'], arg['value'])
                e.level.entity_component_index[e.id][c.name] = c

            return c

        elif arg['t'] == 'ent':
            return self.manager.find_entity(arg['eid'])

        elif arg['t'] == 'wnd':
            return self.manager.window

        elif arg['t'] == 'lst':
            return [self.load_arg(a) for a in arg['values']]

        elif arg['t'] == 'tpl':
            return tuple([self.load_arg(a) for a in arg['values']])

        elif arg['t'] == 'dct':
            return { k: self.load_arg(v) for k, v in arg['items'].items() }
        
        else:
            raise ValueError("Unknown JSON argument type: {}".format(repr(arg['t'])))

    def send(self, session, command, *args):
        self._write(session, '\x00'.join([
            command,
            *(json.dumps(dump_arg(a)) for a in args),
        ]).encode('utf-8') + b'\n')

    def send_deltas(self):
        self.last_t = time.time()

        for s in self.clients.keys():
            #for chg in self.change_accum:
            #    print('delta sent:   ', *chg)

            self.send(s, 'DELTA', *self.change_accum)

        self.change_accum = []

    def __init__(self, game: '..game.Game', port: int, player_type: str = 'player'):
        self.game = game
        self.manager = game.manager
        self.player_names = set()
        self.clients = {}
        self.players = {}
        self.outbound = {}
        self.writes = {}
        self.locals = {}
        self.change_accum = []
        self.port = int(port)
        self.player_type = player_type
        self.running = False

        self.buffer = ''

    def _write(self, s, data):
        self.writes[s].append((time.time(), data))

    async def accept(self, client: socket.socket, address):
        client.setblocking(0)

        session = str(uuid.uuid4())
        self.outbound[session] = b''
        self.writes[session] = []

        self.players[session] = None
        self.clients[session] = None

        commands = {}

        def _write(data):
            self._write(session, data)

        def error(*args):
            self.send(session, 'ERR', *args)

        print('New client connected from:', ':'.join(str(x) for x in address))

        async def _recv(data):
            try:
                lines = (_recv.buffer + data.decode('utf-8')).split('\n')

            except ValueError:
                #_write(b'ERR\x00102\x00malformed command line buffering' + b'\n')
                error(102, 'malformed command line buffering')
                return

            _recv.buffer = lines[-1]

            for command in lines[:-1]:
                command = command.strip()

                try:
                    name = command.split('\x00')[0]

                except ValueError:
                    #_write(b'ERR\x00103\x00malformed command arguments' + b'\n')
                    error(103, 'malformed command arguments')

                for target_name, func in commands.items():
                    if name.upper() == target_name.upper():
                        #print('  -  Executing command:', target_name.upper())
                        values = []

                        for val in command.split('\x00')[1:]:
                            try:
                                values.append(self.load_arg(json.loads(val)))

                            except json.JSONDecodeError:
                                error(101, 'bad JSON data')
                                #_write(b'ERR\x00101\x00bad JSON data' + b'\n')

                                print(command.replace('\x00', ' \x1B[1m|\x1B[0m '))
                                return

                            except BaseException as err:
                                print(command.replace('\x00', ' \x1B[1m|\x1B[0m '))
                                raise
                        
                        func(*values)

        _recv.buffer = ''

        def command(target_name: str):
            def _decorator(func: Callable):
                commands[target_name] = func
                return func
                                
            return _decorator

        def send_entities():
            loaded = []

            for entity in self.manager:
                comp = [(comp.name, comp.value, type(comp).__name__) for comp in entity.get_components()]

                e = {
                    'eid': entity.id,
                    'components': comp
                }

                if entity.level is not self.manager:
                    e['level'] = entity.level.id

                loaded.append(e)

            #_write('\x00'.join(['INIT_ENTITIES', *(json.dumps(dump_arg(x)) for x in loaded)]).encode('utf-8') + b'\n')
            self.send(session, 'INIT_ENTITIES', *loaded)
            print('Sent entities')
        
        @command('join')
        def on_join(local_id, name):
            if self.players[session]:
                print('/!\ Already joined:', name)
                error(201, 'already joined')

            elif name in self.player_names:
                print('/!\ Name taken:', name)
                error(203, 'name taken')

            else:
                lvls = []

                for lid, level in self.manager.levels.items():
                    lvls.append({
                        'lid': lid,
                        'deltas': level.deltas
                    })
                    
                self.send(session, 'INIT_LEVELS', self.manager.current_level.id, *lvls)
                send_entities()
                self.send(session, 'RNG', *self.game.random.getstate())
                
                p = None

                for e in self.manager:
                    if e.has('name', 'localplayer') and e['name'].value == name:
                        p = e
                        p['localplayer'] = local_id
                        
                        break

                if not p:
                    lvl = self.manager.current_level

                    if not lvl:
                        lvl = self.manager

                    print('Creating player...')
                    p = lvl.create_templated_entity(self.player_type, [('name', name), ('localplayer', local_id)])

                eid = p.id

                self.players[session] = p
                self.locals[session] = local_id

                print('Joined:', name, '(local: {}, id: {})'.format(local_id, eid))

                # Force resending deltas
                if time.time() - self.last_t > update_interval:
                    self.send_deltas()

        @command('snapshot')
        def on_request_snapshot():
            if session in self.players:
                send_entities()

        @command('leave')
        def on_leave():
            if self.players[session] is None:
                error(202, 'tried to leave a game the client is already not connected to', "You're just like the kid who's not invited to the party, but comes anyway, and takes a dump in the pool just for the reactions.")
                print('/!\ Not in the game', address)

            else:
                print('Left:', self.players[session]['name'].value)
                self.players[session].remove()

        @command('broadcast')
        def on_event(source, event_name, args, kwargs):
            local = self.locals[session]
            
            for sess in self.clients.keys():
                if sess != session:
                    self.send(sess, 'EVENT', time.time(), local, source, event_name, args, kwargs)

            if source not in self.manager.all_entity_ids():
                error(204, 'no such entity')

            self.manager.emit_local(self.manager[source], event_name, local, *args, **kwargs)

        update_interval = 1 / 10
        self.last_t = time.time()

        async with trio.open_nursery() as nursery:
            while self.running:
                sleep_amount = 1 / 30
                data = b''

                try:
                    data = client.recv(8192)

                    if data == b'':
                        del self.clients[session]

                        if session in self.players: del self.players[session]
                        if session in self.locals: del self.locals[session]

                        return

                    else:
                        nursery.start_soon(_recv, data)

                except (ConnectionResetError, BrokenPipeError):
                    del self.clients[session]

                    if session in self.players: del self.players[session]
                    if session in self.locals: del self.locals[session]
                            
                    return

                except BlockingIOError:
                    sleep_amount = 1 / 20

                if time.time() - self.last_t > update_interval:
                    self.send_deltas()
                    
                self.process_writes(session)

                try:
                    sent = client.send(self.outbound[session])

                except (ConnectionResetError, BrokenPipeError):
                    del self.clients[session]

                    if session in self.players: del self.players[session]
                    if session in self.locals: del self.locals[session]

                    return

                except BlockingIOError:
                    pass

                else:
                    self.outbound[session] = self.outbound[session][sent:]

                    if self.outbound or len(data) == 8192:
                        sleep_amount = 1 / 60
                    
                await trio.sleep(sleep_amount)
        
    async def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(5)
        self.socket.setblocking(False)

        self.running = True

        async with trio.open_nursery() as nursery:
            while self.running:
                try:
                    (conn, addr) = self.socket.accept()

                except BlockingIOError:
                    pass

                else:
                    nursery.start_soon(self.accept, conn, addr)

                await trio.sleep(0.5)

        self.clients = {}

    def stop(self):
        self.running = False

    def process_writes(self, s):
        nw = []

        for when, data in self.writes[s]:
            #if time.time() - when > 5:
            #    continue

            self.outbound[s] += data

        self.writes[s] = nw