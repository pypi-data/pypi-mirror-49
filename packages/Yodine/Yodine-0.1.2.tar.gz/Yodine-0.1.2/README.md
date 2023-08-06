# Yodine

Briefly put, Yodine is a special, flexible, fun, easily extensible game, written in Python, with advanced plugin support,
that uses pyglet and an involved Entity-Component-System infrastructure.

It is easy to write plugins for Yodine. And it is easy to _feel the structure_. (Just don't let the cows do so. They're evil,
`.py`-file-eating monsters.)

**Notice: the game is currently in a development stage. Expect bugs and a lack of features.**




## How to play

In order to install the game, simply run:

```
pip install yodine
```

Running it is quite simple, too:

```
python -m yodine
```



## Writing Plugins

In order to write a plugin for Yodine, you may run the following module:

```
python -m yodine.utils.plugin_init
```

After answering a few questions, a generous, helpful filesystem structure will be generated. The files are
heavily commented, to aid you in your quest to add to the game. Let's build a castle?



## License

This project and its source code are available under [the MIT license](https://opensource.org/licenses/MIT),
under the autorship of Gustavo Ramos Rehermann (`rehermann6046@gmail.com`).