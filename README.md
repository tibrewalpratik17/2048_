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
![2017-12-14](https://user-images.githubusercontent.com/16771666/33991606-333daa2a-e0f5-11e7-9cf0-885904297f58.png)

Enter the LEVEL number (between 3 and 7)

![2017-12-14 2](https://user-images.githubusercontent.com/16771666/33991601-2cee778a-e0f5-11e7-9f93-639075cc93da.png)

![2017-12-14 1](https://user-images.githubusercontent.com/16771666/33991574-17ce934e-e0f5-11e7-90bc-b2d251e36a59.png)

Use backspace Key to Undo a move.


