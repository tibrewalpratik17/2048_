# 2048_
A pygame implementation of the game 2048

## Requirements

* Python 2.7.6(*usually pre-installed in Ubuntu*)
* Pygame package for the specified python version

*For installing the requirements you can check the following [link](https://inventwithpython.com/pygame/chapter1.html).*

## The code

Here is a brief summary to get you started:

* `showStartScreen()` function basically shows the first screen on executing the code.
* `randomfill(TABLE)` function randomly fills the table in empty spaces.
* `checkForKeyPress()` function checks for an event(*key press in our case*) and returns the same.
* `show()` function displays the game screen after each key press and also matches the defined colours with the respective cells.
* `runGame` is the function that controls the overall game. It is called in an infinite loop in the `main` function. It calls the `randomfill` function and even checks for the pressed key by calling the `key` function. It stores the copy of the previous table and matches with the present state. This is the function controlling the whole state of the game.
* `moveDown` function is defined for the actions to be undertaken when the downward key is pressed.
* `moveUp` function is defined for the actions to be undertaken when the upward key is pressed.
* `moveRight` function is defined for the actions to be undertaken when the right key is pressed.
* `moveLeft` function is defined for the actions to be undertaken when the left key is pressed.
* `createButton` function is used to create a new button.
* `gameOver()` return true if no further move is possible.
* `showGameOverMessage` funtion is defined to display game over screen.

## Screenshots

[![Screenshot_from_2017-12-08_00-39-42.png](https://s2.postimg.org/41ek94sbt/Screenshot_from_2017-12-08_00-39-42.png)](https://postimg.org/image/bu5813yat/)
[![Screenshot_from_2017-12-04_19-39-27.png](https://s7.postimg.org/sea0arqsr/Screenshot_from_2017-12-04_19-39-27.png)](https://postimg.org/image/e7u9fjfxj/)
[![Screenshot_from_2017-12-04_12_43_15.png](https://s7.postimg.org/y4gw2ok7v/2017-12-04.png)](https://postimg.org/image/dx3gadmqf/)

## Issues

* Make the start screen look more attractive with options for different levels and leaderboard.
* Make a leaderboard for storing high scores calculated on basis of *Points earned* and *Time taken*.
* It will be great to implement AI techniques which can provide the player with hints for the next step.

## Contributing

Any contributions are more than welcome. Just **fork** the repo and start contributing.
