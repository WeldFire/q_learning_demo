# Maze Generation for a Q-Learning Bot!

## Overview
This code generates a more difficult set of mazes for a Q-Learning bot to practice on. 
This code is a submission for [this](https://youtu.be/A5eihauRQvo) video on Youtube by Siraj Raval. 
This is a simple example of a type of [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning) called [Q learning](https://en.wikipedia.org/wiki/Q-learning). 

	● Rules: The agent (yellow box) has to reach one of the goals to end the game (green or red cell).
	● Rewards: Each step gives a negative reward of -0.04. The red cell gives a negative reward of -1. The green one gives a positive reward of +1.
	● States: Each cell is a state the agent can be.
	● Actions: There are only 4 actions. Up, Down, Right, Left.

## Dependencies
 - Python (tested on 2.7, but I think 3 should work)
 - tkinter (sudo apt-get install python-tk)
 - noise (pip install noise)

## Usage
Run `python Learner.py` in terminal to see the the bot in action.

To have some more fun, edit the Map generation type or size in World.py!

## Map Types
### Layered Simplex Map Type
![](/example-maps/simplex.png?raw=true "Layered Simplex Map Type")
### 'Lava' Map Type
![](/example-maps/lava.png?raw=true "'Lava' Map Type")
### 'Core' Map Type
![](/example-maps/core.png?raw=true "'Core' Map Type")
### Random Map Type
![](/example-maps/random.png?raw=true "Random Map Type")

## Features
* Map was expanded and is dynamic to any size (can be changed in World.py)
* More obstacles can be generated based on the map type selected
* 4 Map type generators were added 
  - Core
  - Lava
  - Simplex
  - Random
* The bot will be positioned in a different safe position on each map creation
* Maps generated are tested to ensure that it is possible for the bot to complete 
* Map generation and validation is timed
* Q-Learning will halt when the bot has found the optimal route
  - You can now let it run in the background and look at how long it took!
* Total iterations until optimal route is calculated and displayed
* Timings until optimal route are calculated and displayed

## Possible Improvements
* More map generation types (Different kinds of noise?)
* Map Size, Type, and Verbosity set as startup arguments
* Hotkeys for building a new map/new map type
* Further bot enhancements
* Lots of code cleaning and commenting :/

## Credits
 - Initial code base [PhillipeMorere](https://github.com/PhilippeMorere).
 - Idea and starting code [Siraj](https://github.com/llSourcell).

