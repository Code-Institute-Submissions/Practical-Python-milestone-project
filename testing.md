#Testing

The testing process was progressive.  In the developing, I started first by working on
logic logic.  During verifyt the game logic,  a series of unittest, defined in test_bj.py
verified all the operation in of blackjack.py and play_game.py.   The specs were written 
with first with goal of both failing then passing to provide confidence the function worked
properly.   See the documentation in the file more details.

After I verified that functions in run.py work property, I had  two phased approach to continue with my testing.
A CLI program was built that enabled me through the use print() statements to verify that operation
various elements of program such as deck creation, loading and saving the user object, score keeping, 
card play and the leaderboard funtionality.  Once, those elements were verified, the print 
statements were removed, so that game play would run without information clutter.  

The old CLI is not deployed in heroku, but is stored in C9.   In hindsight, I should have 
created a git branch that would still available in github as evidence of this approach.  But in
practice, I just continue to git commit over the cli program. 

After I had confidence that CLI program and game play logic, I modified run.py for Flask.
To test that functionality, I added text to web page along with the current presentation to
test that graphics such as for cords matched the underlying logic.    For example, using
webpage to display the card count number, alerted me to favicon issue described in Readme.

For usability, I tested webpages on Google Chrome, Apple Sarafi, Windows Edge, Firefox.  I also
tested it on iphone8 and Ipad Pro.



Manual test include:

using print statements and python console:

* inspect the user object after play to see the player's scoce and that stored hand was
  reset to empty.

* used console print statement to verify that cards were removed by seeing the decksize
  decrease and also testing the function in console by inspecting a small deck before and after
  getcard funciton was used.

* used print statement to show hands and values.

* used print statemeent to see the users scores before and after.

* used print statement and for loops compare the users objects and leaderboard sorting functions
  to verify that sore worked.

* used print statements to watch gamewinner() build a dealer's hand.

In discussing the testing in final review with my mentor, it also became clearer that
using logging functions would also acheived a better aproach, while creating less
clutter on the terminal.