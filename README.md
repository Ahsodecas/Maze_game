# Maze_game
## Table of content
* [Overview](#overview)
* [Files](#files)
* [How to use](#how-to-use)
* [Tests](#tests)
* [Technologies](#technologies)
## Overview
A simple maze game that can generate different random mazes using the BFS algorithm. \
The current version of the game is version 1.0. Some new features are planned for the next version.

The design was inspired by the novel "Omniscient Reader's Viewpoint" by Sing Shong.

## Files
* main.py contains the main functionality, Player and Maze classes.
* generator.py generates one random maze for the current game.
* bfs.py is used by the generator to check whether the created maze is doable.
* test_bfs.py contains unit tests.
* *.png files are the images for player, goal, icon and background.

## How to use
The player can be moved with ↓←↑→ keyboard symbols. 

![image](https://github.com/Ahsodecas/Maze_game/assets/96869680/a6a7ccc7-f7f5-469e-b0b3-a2f7784264f2)

Once the player reaches the goal, the game over screen is displayed. 

![image](https://github.com/Ahsodecas/Maze_game/assets/96869680/be92a959-901c-4832-9f1b-2489df6e3b12)

To exit the game one can click the ✖ button in the top right corner.


## Tests
In test_bfs.py, there are some tests to check whether bfs and maze_generator functions work properly. All tests run correctly.
![image](https://github.com/Ahsodecas/Maze_game/assets/96869680/b6ed5908-92ea-4608-b6d9-409777233a70)
## Technologies
Python 3.9.7 \
Packages: pygame \
You can install it using the following command on Windows:\
  pip install pygame
