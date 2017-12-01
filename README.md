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
* `drawPressKeyMsg()` function shows the press key message on the start screen at the bottom right corner.
* `checkForKeyPress()` function checks for an event(*key press in our case*) and returns the same.
* `show()` function displays the game screen after each key press and also matches the defined colours with the respective cells.
* `runGame` is the function that controls the overall game. It is called in an infinite loop in the `main` function. It calls the `randomfill` function and even checks for the pressed key by calling the `key` function. It stores the copy of the previous table and matches with the present state. This is the function controlling the whole state of the game.
* `moveDown` function is defined for the actions to be undertaken when the downward key is pressed.

## Screenshots

[![Screenshot_from_2017-12-01_12_43_59.png](https://s2.postimg.org/5tyl7niux/Screenshot_from_2017-12-01_12_43_59.png)](https://postimg.org/image/qe3f64ylx/)


[![Screenshot_from_2017-12-01_12_43_14.png](https://s2.postimg.org/s4mg7pnvt/Screenshot_from_2017-12-01_12_43_14.png)](https://postimg.org/image/a1tdghs11/)

## Issues

* Complete the code for other moving options `moveup`, `moveright` and `moveleft`. 
* Make the start screen look more attractive with options for different levels and leaderboard.
* Make a leaderboard for storing high scores calculated on basis of *Points earned* and *Time taken*.
* It will be great to implement AI techniques which can provide the player with hints for the next step.

## Contributing

Any contributions are more than welcome. Just **fork** the repo and start contributing. 


