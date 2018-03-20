# Introduction

The HT Blackjack is the game that is created to meet the requirements for milestone 
in Practical Python.

The users starts the game, the presented with a sign in page, then they enter a game
where the user receives two cards and given the option to hit (get another card ) or stay.
The user is also presented with the odd of bust or what are the odds that next card will
send the user's hand over 21.

When the user decided to stay the system automatically plays the dealer's hand.  At that point,
the winner is determined, the result of the game is recorded and leaderboard is presented.determined

## Technologies 

The game is written in python3.4.3, the python loaded on C9 platform.

This application was written in two phases:

* In first step, the program was developed as command line (CLI) based program run though the console.  The goal was to develop and perfect the game logic.

* In the secod step, once the game was operating, was to recode as a web based application using Flask. 
  To perseve the working program, in c9, I cloned the program into a new project and deployed the cloned
  project.   In retrospect, I should have created a git branch as well.

In the web version, my key technologies were:

* Boostrap 3.3.7
* Bootstrap template (base.html and basegame.html)
* WTForms
* HTML5 - used semantic tags
* Python session, pickle
* Flask

I also able to obtain images for my background and playing cards from open sources with
appropriate use licenses. 

From a program structure perspective, I made an effort to separate my program and
presenation logic.  Furthermore, program logic was further separated into essential
playing of the game and actions assoicated with a deck of cards.  A summary of key
python programs are below with each module having detailed documentation in the code.:

<dl>
  <dt>Game Logic </dt>
  <dd> blackjack.py  -  provides essential logic for basic blackjack card game.  It's function specific to
  to distributing cards, determining their value and determining oods of next card driving the 
  hand over 21.   It also includes the logic necessary to a cardshoe, the colleciton of cards of yet 
  uplayed cards.  This script also includes a helper program for sorting the list of user by score
  order so that a leaderboard can evenutally be posted.</dd>
  
  <dd>play_game.py - provides logic for user actual table play.  It includes functions for setting users list 
  include either creating a list if none exists or loading the exisitng list from server.  A list of user is
  kept a stored pickle object /data folder.  It also includes a function for when the user logs in
  it retrieves that user information for it's object.  All users are partterned after the Player object,
  which is defined in Player.py.  Finally, play_game includes a function that automaticall plays 
  out the dealer's hand.</dd>
  
  <dt> helper logic<dt>
  <dd> helper logic includes dataio.py, which provide generic script for saving and loading object 
  using python pickle.</dd>
  
  <dt>Server logic</dt>
  <dd> run.py is the main program loop.  It includes the necessary to set up the game, Flask routing
  rounting functions, the logic necessary to log in a user, deal cards and build up content to displayed 
  in both the game.html and dealer.html pages.  The game.html page shows the cards for the user,their score
  their odds and offers buttons for them to decided to to hit or stay.  
  
  The dealer.html show the card for the dealer, both the user's and dealer score, the winner
  and that user's running total.  It is show the leaderboard.</dd>
  
  <dt> Test logic </dt>
  <dd> the test logic includes the set of unit level tests.</dd>

</dl>

## Key Fromolders

* Template folders holds Flask html template.  the templates starting with "base.." are 
  part template from Bootstrap.

* Data folder holds stored objects for the working deck of cards and user list.

* Static folder includes  assets for that I playing cards and custom background images. The img folder
  are assets from the bootstrap and not used.  css and scss are style sheets, with some customization.
  vendor files are bootstrap and jquery file necesary to run those programs and features. 

## Testing - see testing.md

## Known Issues

There is one know issue where favicon, each time log in webpage is exercised, creates 
an user called favicon, which in turn starts to player a game and draw cards.  If cards
count runs below minimum value, set on top portion run.py, then card shoe is refilled after the user
finishes a game.  But still cards come out the deck that shouldn't.  The program
also removes favicon user, so that they don't show up in the leaderboard.

# Start program

To run the program, just requires at the terminal -  "python3 run.py".



