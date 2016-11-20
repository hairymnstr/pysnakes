License
=======

    Pysnakes 1 or 2 player snake game
    Copyright (C) 2009  Nathan Dumont

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact nathan@nathandumont.com
    Visit http://www.nathandumont.com/blog/pysnakes

PySnakes documentation
----------------------

So open source apps are famously badly documented, especially when, like this one, they were one man projects.

Here's some stuff you might want to know about the game.

Pre-requisites
--------------

To run PySnakes you need a copy of Python, and the corresponding pygame package.  On Ubuntu you should just need to run

	sudo apt-get install python-pygame

On a RaspberryPi it should just run.

On Windows you'll need to go to <http://python.org> to get a version of Python and <http://pygame.org> to get the matching version of PyGame.

Once you're ready to run it, on Windows just click the pysnakes.py file.  On Linux open a terminal in the directory and enter

	python pysnakes.py

Key bindings
------------

There are no mouse controls at all in this game. Most of the menu type options are up and down cursor
keys with enter to pick the highlighted option. The “Controls” option in the main menu has more
details on key presses to set options, and also gives access to customise the keyboard controls for
directing your snake in game.

Additionally Escape will usually drop you back to the main menu (from highscores or controls
options), and Pause/Break will pause the game (this reduces frequency of refresh so the processor
usage drops, and also pauses the game time counter.)

Aim of the Game
---------------

Your aim is to gain as many points in as little time as possible. The high scores table is ranked on
score, then on time, so if you have a higher score you will be at the top, if you have an equal score but a
faster time you will be at the top etc.

To gain points you need to grab the fruit (looks a bit like an apple). This gives you points but also
makes you grow. There are 10 fruit per level, and later fruit are worth more points, but make you grow
more.

You can loose points if you die, this also costs you a life, of which you have only 3 so avoid getting
killed.

You will die if you crash into a wall, or your own tail, or in the two player version into your opponents
tail.

In two player mode the aim is to get the most points, you can do this by getting to fruit first and by
forcing your opponent into situations where they will crash (like Tron style games).

Customising the game play
-------------------------

There are a few things you can do to customise play. As stated previously you can go to the Controls
section on the main menu which lets you set the key-bindings, it also allows you to pick a custom game
speed (default is 125 mS per frame, but other options are available) and to set the level set. The default
level set is in the plain text file called “default” in the pysnakes installation directory. To create your
own custom levels I advise copying this file. Probably best not to edit it directly.

There is almost no error checking on the level files when they're read in so if you do something wrong
in your custom level set then expect the program to crash when you start a game. The good news is
that you can change the level in the Controls menu without the program trying to load a level. This
means if it does crash you can always go back to default and play.

Take a look in the default level set for some notes on the level file format. Basically it's based on an
old snakes game (nibbles for MS QuickBasic if you're interested) which was an ascii based interface so
it's 40 columns by 29 lines of blocks to make a level. Anything shorter than 40 lines is discarded by
the loading routine so you can leave as many blank lines in the level set as you like and any comments
less than 40 characters long will also be ignored. A 1 is a wall and a 0 is not. In fact a 1 is a wall and
anything else is not, but I'd advise you not to rely on this in case there are more features added in later
versions (perhaps??).

Once you've made your masterpiece level set, you need to copy it to the level set folder. This is placed
with all of the other config info for pysnakes in your home folder (/home/<username> on Linux) in a
hidden folder called “.pysnakes” (For those of you new to Linux files starting with a dot are hidden
files). In here you'll find the settings file that contains your personal settings in a plain text file, the
high scores file and a folder called “levelsets” (if it isn't there either make it yourself or start pysnakes
and go into the controls menu, this makes the folder if it isn't already there). All your custom level sets
need to go in this folder and be called something other than default. Once that's done run pysnakes
again and you should find in the Controls menu that your custom level is now in the list of available
level sets, select it choose Save and Exit and then play away.

Reasons for writing the game
----------------------------

This game was written for a Linux Format (<http://www.linuxformat.co.uk>) reader competition. There
is an acknowledgement to this fact in level 10 if you ever get that far (you can always make a custom
level set with less of the preceding levels if you really want to see it but where's the fun in that?)

It was written in about 2 weeks of spare evenings with minimal effort, which shows how good the PyGame
SDL bindings really are.

Any thoughts or comments?
-------------------------

Please inform the author if you have any thoughts or comments, either on GitHub:

https://github.com/hairymnstr/pysnakes

or via email:

nathan@nathandumont.com

Source
------

All of the game source is in the file "pysnakes.py".  The SVG source for logos and graphics are in the src folder.  These were created with Inkscape.

