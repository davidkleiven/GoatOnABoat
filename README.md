![Build status](https://travis-ci.org/davidkleiven/GoatOnABoat.svg?branch=master)
# Goat On A Boat
Goat on a boat quizgame

# Installation
The game depends on the following packages
* [Google Chrome (not Chromium)](https://www.google.com/chrome/)
* [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/)

So install these first.

To install the game
```bash
pip install -r requirements.txt
pip install .
```

For developers change the last command to
```bash
pip install -e .
```

# Starting the game
The game can be started by running the *goat_boat.py* command.
The name of the players are given as a list on the command line.
Example:
```bash
goat_boat.py Name1 Name2 Name3
```
