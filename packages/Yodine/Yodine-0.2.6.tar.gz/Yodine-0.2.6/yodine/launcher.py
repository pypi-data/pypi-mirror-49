import pkg_resources
import os
import random

from tkinter import *
from . import game



class InputRow(object):
    rows = {}

    def __init__(self, master, **kwargs):
        self.master = master
        
        self.row = InputRow.rows.setdefault(master, 0)
        InputRow.rows[master] += 1

        self.init_widgets(**kwargs)

    def init_widgets(self, label=None, initial='', options=None, **_):
        if label is not None:
            self.label_text = StringVar(value=label)
            self.label = Label(self.master, textvariable=self.label_text, bg='white')
            self.label.grid(row=self.row, column=0, sticky='e')

        if options:
            self.value = StringVar()
            self.value.set(initial)
            self.input = OptionMenu(self.master, self.value, *options)

        else:
            self.value = StringVar(value=initial)
            self.input = Entry(self.master, textvariable=self.value)

        self.input.grid(row=self.row, column=1, sticky='nswe')


class LauncherArea(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bd=2, relief=SUNKEN, **kwargs)

        self.init_widgets()

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def init_widgets(self):
        pass


class LauncherInputArea(LauncherArea):
    def init_widgets(self):
        self.games = []

        for ep in pkg_resources.iter_entry_points('yodine.plugin'):
            self.games.append(ep.name)

        self.games = list(set(self.games))

        if 'yodine_data' in self.games:
            init_game = 'yodine_data'

        else:
            init_game = random.choice(self.games)

        self.player_name = InputRow(self, label='Player Name*', initial=os.environ.get('YODINE_NAME', None)).value
        self.game_name = InputRow(self, label='Game', options=self.games, initial=init_game).value
        self.save_name = InputRow(self, label='Save Filename*').value
        self.server_addr = InputRow(self, label='Connect to*', initial=os.environ.get('YODINE_CONNECT', None)).value

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        
        notice = Label(self, text='* optional', justify=CENTER, bg='white')
        notice.grid(column=0, columnspan=2, sticky='we')


class YodineLauncher(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(column=0, row=0, sticky='nswe')

        self.init_widgets()

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def init_widgets(self):
        self.title = Label(self, text="Yodine Launcher", bg='white')
        self.title.grid(row=0)

        self.form = LauncherInputArea(self, bg='white')
        self.form.grid(row=1, sticky='nswe')

        self.start_button = Button(self, command=self.on_start, text="Run")
        self.start_button.grid(row=2, sticky='we')

    def on_start(self):
        self.master.destroy()
        run_game(self.form.game_name.get(), self.form.save_name.get(), self.form.server_addr.get(), self.form.player_name.get())


def run_game(game_name, save_name = None, connect_to = None, player_name = None):
    this_game = game.Game(game_name, save_name or None, client_addr=connect_to or None, player_name=player_name or None)
    print('Starting...')
    this_game.run()


def main():
    root = Tk()
    root.title('Yodine Launcher')

    frame = YodineLauncher(root, background='white')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()



if __name__ == '__main__':
    main()