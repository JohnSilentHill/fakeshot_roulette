<img width="1200" height="240" alt="github-header-banner(5)" src="https://github.com/user-attachments/assets/eb6ded4b-bb4a-44b8-ae63-b764a4d758fd" />

# Contents

- [Overview](#overview)
- [How to play](#how-to-play)
  - [Gameplay Loop](#gameplay-loop)
  - [Commands](#commands)
- [Boring Things](#boring-things)
- [Roadmap](#roadmap)

# Overview

This is a Python text-based recreation of Buckshot Roulette by Mike Klubnika. <br/>

Currently, there are *most* of the items from the original game bar a few multiplayer-specific ones that probably won't be added since this is offline only. 

You can read below, or use the `'info'` command in-game for help.

# How to play

### == Gameplay Loop ==

> This is brief, please refer to the [wiki!](https://buckshot-roulette.fandom.com/wiki/Buckshot_Roulette)

Imagine Russian Roulette but with a shotgun and a random amount of shells. A live shell deals damage, and a blank does not.

You have the choice of shooting yourself, your opponent, or using an item to your advantage.<br/>
If a live shell is shot at you, regardless of who fired it, it becomes your opponent's turn. This rule applies to them too.

The full list of items and their uses can be viewed in game and for the sake of conciseness, can also be found [here.](https://buckshot-roulette.fandom.com/wiki/Category:Items)

You win if your opponent runs out of lives whether that be by your hand or their own.

Good luck.

### == Commands ==

Main menu:

- [start] -- Starts the game
- [info] -- Opens the info menu
- [quit] -- Saves data to a .json file and quits

In-game:

- [item] -- Uses a specified item, e.g 'saw', 'beer'
- [me/ai] -- Shoots either you or your opponent
- [debug] -- Shows some debug info for testing purposes

# Boring things

- This project is highly WIP and you can view the roadmap below to get a general idea as to the progress so far. <br/>
Feel free to fork and create pull requests as you please. If you are more experienced with Python, please do take a look. <br/>

- Your save is blank by default, with no wins or money. You can simply play the game or edit your save manually to fix this glaring issue.

> Open the `savegame.json` file under the parent directory in a text exitor of your choice. The values are pretty self-explanatory.

------

*Disclaimer: This is a remake of the original title Buckshot Roulette. For that, all credit goes to [Mike Klubnika](https://mikeklubnika.com/).*

*The main soundtrack was sourced from the game files as I do own it on steam, however all the other sfx that aren't publically accessible were downloaded from royalty free libraries.*
<br/>

------

# Roadmap
*For a more detailed version of this, see the file 'detailed_todo.md'*


### == Completed ==

- [x] Main game loop
- [x] Basic usage of items
- [x] Optimisation using gamestates
- [x] Save file reading/loading (I think)
- [X] Debug command
- [X] More items to match original roster
- [X] Different rounds to mimic original game
- [X] Money
- [X] Better text output for a more visually appealing experience

### == Upcoming ==

- [ ] Intelligent AI -- I will literally just make it so it judges whether or not to shoot.
- [ ] Difficulties


