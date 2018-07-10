"""
run.py is the main program loop and starts the game.

The blackjack game is buit using Python Flask and Python 3.4.

The game is designed to:

-   present the user with a sign in page.  The user enters their name, and if that user
    has played the game before, their running score is retrieve.  If they're a new
    user, a new profile is set up.
    
-   Once the user is signed in, then they are presented with the initial two card deal.
    In the background, the dealer is also dealt two cards.   
    
    The user is given the option to request an additional card, hit me button or stay.
    The user's score is display as well as odd of going bust (1 - (available to win / total cards available ))
    Once the user selects stay, the dealer is hand is automatically played an displayed.
    
    The dealer's hand is displayed, the dealer's score and statement of who won.
    Also a leader board is shown, showing the top players.  The leader board is filtered
    to only show the top portion of list.  
    
    The user is presented with the options to continue player, new game button or quit.
    If the user quits, the game returns to it's starting state.

Key variables:
 - users
    a list of active Player objects.  Player object defined in Player.py.
    The users list is stored in /data file to create persistance and loaded at the start
    of the game.
    
- working_deck
    A list of available cards to play.
    
    
Key functions:    

- update_deck(deck) 
    accepts a deck of cards and returns a updated card shoe, if the deck is below
    the minimum size as defined by the min_num_card variable.
    
- Bj_player(Form) 
    sets up a WTForms form object which is used to managed the hit me and stay buttons on
    game.html and new game and quit buttons on the dealer.html
    
- display_cards(hand) 
    accepts a list of cards and returns a list of the location of graphic for each card.
    The returned list is used by game.html and dealer.html to display the cards for each hand.

- game_msg(status)
    accepts a status code generated by blackjack.getwinner_web and returns a message to
    be displayed in dealer.html designating the winner of the hand.

"""
#!/usr/bin/env python3

# imports key helper functions from blackjack.py, play_game.py, dataio.py, cards.py
# wtforms is used to create and manage buttons on the game.html and dealer.html pages.
import os, json
from flask import Flask, render_template, request, redirect, session, url_for
from play_game import setup_bj, getwinner_web, getuser
from blackjack import *
from dataio import savedata, loaddata
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import cards

# configures Flask
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'well-secret-password'

# defines the number of decks in card shoe. Card shoe is a list of available cards to play.
num_decks = 10
# min size of card shoe before it needs to be refilled.
min_num_card  = 100
# number of leader board players to be presented.
LEADERBD_SIZE = 4

# loads the card shoe.  card_shoe from blackjack.py
# .... how do I  make this global....
working_deck = card_shoe(num_decks)
savedata(working_deck,"data/deck.pickle" )

# loads users from file -  play_game.setup_bj() 
users = setup_bj()

# checks if the card shoe needs to be refilled. 
# def update_deck(deck):
#     if len(deck) < min_num_card:
#         deck = card_shoe(num_decks)
#     return deck    
    
# sets up WTForms object for managing web page buttons
class Bj_player(FlaskForm):
    name = StringField(label='Name')
    hit = SubmitField(label='Hit Me')
    stay = SubmitField(label='Stay')
    new_gm = SubmitField(label='New Game')
    quit_gm = SubmitField(label='Quit')
    
# Create a list of playing card locations.  Accepts a hand e.g.6C, 7S
# returns a list of file locations of graphic corresponding to each card.
def display_cards(hand):
    playerhand = []
    for card in hand:
        playerhand.append("static/assets/SVG-cards/" + cards.cards[card])
    return playerhand    

# generates a message to be displayed on dealer.html
def game_msg(status):
    if status == 0:
        return "Tie, it's a push"
    if status == -1:
        return "Dealer Wins"
    if status == 1:
        return "Player Wins!"
"""
Flask route /
Starts the game, but generating the landing page,
index.html.   The landing page only has a form to accept user's name.

Once the user logs, posts their user name, the page is redireted to
the game page for that user.
"""

@app.route('/', methods=["GET", "POST"])
def index():
    #if user name is posted, start the game and go /<username> page.
    if request.method == "POST":
        # once user name is accepted status is set to initial.
        # status is used in this script to track the flow of game and represents
        # start of game where two hands are dealt.
        session["status"] ="new"
        return redirect(request.form["username"])
    return render_template("index.html")


"""
Flask route /<username>

Starts game play for a user.  The program builds the initial user and dealer hands,
determines the value and display them game.html page.  The user plays out their 
hand, the program plays the dealer hand and display it on the dealer.html page.

key functions:

- teardn()
    At the end of player, sets various points back to their initial state and
    save the updated user object so that user's name and score attributes are 
    perserved. 
    
    NOTE: somehow, favicon.ico gets added to the users list.  function removes 
    it.
"""

@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    # set up html buttons using WFTforms object
    form = Bj_player()
    # form2 = Bj_dealer(), tried to create a second wtforms object. didn't work.
    playerhand = []
    dealer_hand = []
    
    if session["status"] == "new":
        working_deck = loaddata("data/deck.pickle")
        session["status"] ="initial"
        if len(working_deck) < min_num_card:
            working_deck = card_shoe(num_decks)
        session["deck"] = working_deck
        
    
    # grabs current user's Player.name attribute. getuser is from blackjack.py
    currentuser =  getuser(username, users)
    
    #resets status varioble to starting point, save users list to disk.
    def teardn():
        #clears Player.hand attribute
        users[currentuser].hand = []
        # removes unwanted favicon.ico user
        if "favicon.ico" in users.keys():
            del users["favicon.ico"]
        #uses dataio.savedata to store updated user list    
        savedata(users,"data/users.pickle" )
        # reset session members to starting state.
        session["status"] = "initial"
        session["player_hand"] = []
        return
    
    # test value, for determining size of working deck
    working_deck = session["deck"]
    decksize = len(working_deck)
    
    # start of the play, status is initial
    if session["status"] == "initial": 
        users[currentuser].hand = []
        # player draws two cards -blackjack.init_deal, and stores hand.
        users[currentuser].hand = init_deal(working_deck)
        session["status"] = "player"
        session["player_hand"] = users[currentuser].hand
        #determine value of hand, odds and creates list of card graphics
        player_val = hand_val(users[currentuser].hand)
        playerhand = display_cards(users[currentuser].hand)
        odds = 100 - odds_to_bust(working_deck, player_val)
        
        #if for some reason, the webpage is reloaded before any user actions
        #reset key variables, for stored settings.
        # hand_val, odds_to_bust is from blackjack.py
        
    else:
        users[currentuser].hand = session["player_hand"]
        player_val = hand_val(users[currentuser].hand)
        playerhand = display_cards(users[currentuser].hand)
        odds = 100 - odds_to_bust(working_deck, player_val)
    
    #gets the dealer's two cards 
    dealer_hand = init_deal(working_deck)     
    
  
    # The form processing section represent the user player's play loop.
    # One the initial, game.html page the user is presented with hit and stay buttons
    # If the hits, they get a card.  If they stay, it moves to the dealer's turn.
    # the program deals the dealer hand, and displays it cards and winner's information.
    # play_game. getwinner_web() is controls the dealers play.
    
    # on the dealer.html page, there are two buttons, new and quit.
    # the new button, for that user plays another hand, but relaading 
    #/username page.
    #quit redirects the page back to index.html.
    
    if form.validate_on_submit():
        name=form.name.data
        # button="hit" if form.hit.data else "stay"
        if form.hit.data:
            button = "hit"
        elif form.stay.data:
            button = "stay"
        elif form.new_gm.data:  
            button = "new"
        else:
            button = "quit"
        
        # if user hits, the user draws a new card. 
        # the session object is used to store current version
        # user hand.
        if  button == "hit":
            #retrieve, update and store user hand.
            #new hand is retrieved from blackjack.hit_me()
            users[currentuser].hand = session["player_hand"]
            users[currentuser].hand = hit_me(working_deck, users[currentuser].hand)
            session["player_hand"] = users[currentuser].hand
            # calculates key value of hand, list of card graphics and odds to bust
            player_val = hand_val(users[currentuser].hand)
            playerhand = display_cards(users[currentuser].hand)
            odds = 100 - odds_to_bust(working_deck, player_val)
            
            # if user's hand is bust, dealer automatically wins
            if player_val > 21:
                #gets graphics for dealer's card.  
                dealerhand = display_cards(dealer_hand)
                dealer_val = hand_val(dealer_hand)
                # updates the users score for the loss and get's message for display
                users[currentuser].score = users[currentuser].score + -1  
                msg = game_msg(-1)
                #removes artifact from the user's list
                if "favicon.ico" in users.keys():
                    del users["favicon.ico"]
                
                #creates a leader board. create a list of user names
                #customer sort function in blackjack.py that sorts user names
                #by scores in ascending order.
                leaderbd = list(users.values())
                leaderbd = sort_leaderbd(leaderbd)
                #dealer.html will show only show up to 4 leaders
                leaderbd_len = len(leaderbd)
                #resets variables
                teardn()
                
                # launches dealer.html
                return render_template("dealer.html", username = username, playerhand=playerhand, playerval=player_val, 
                dealerhand=dealerhand, dealerval=dealer_val, score = users[currentuser].score, form=form, msg = msg, 
                leaderbd=leaderbd, leaderbd_len=leaderbd_len)
           
            # If user's hand is 21, the dealer tries to win.
            if player_val == 21:
                session["status"] = "dealer"
                # runs play_game.getwinner_web to play dealer hand and determine winner.
                game_result = getwinner_web(users[currentuser].hand, dealer_hand, working_deck)
                #builds winner message, cards for display and dealer's hand value
                msg = game_msg(game_result[0])
                dealer_hand = display_cards(game_result[1])
                dealer_val = hand_val(game_result[1])
                #updates user's score
                users[currentuser].score = users[currentuser].score + game_result[0]
                #cleans out unwanted artifact
                if "favicon.ico" in users.keys():
                    del users["favicon.ico"]
                #creates leader board    
                leaderbd = list(users.values())
                leaderbd = sort_leaderbd(leaderbd)
                leaderbd_len = len(leaderbd)
               # resets system variables
                teardn()
                # launches dealer.html page
                return render_template("dealer.html", username = username, playerhand=playerhand, playerval=player_val, 
                dealerhand=dealer_hand, dealerval=dealer_val, score = users[currentuser].score, form=form, msg = msg,
                leaderbd=leaderbd, leaderbd_len=leaderbd_len)
            # test value, for determining size of working deck
            decksize = len(working_deck)
            #launches game.html page, user is still playing their hand          
            return render_template("game.html", username = username, playerhand=playerhand, playerval=player_val, form=form, odds=odds,
            decksize=decksize)
        
        # user stays, dealer starts it's play    
        if button == "stay":  
            session["status"] = "dealer"
            # runs play_game.getwinner_web to play dealer hand and determine winner.
            game_result = getwinner_web(users[currentuser].hand, dealer_hand, working_deck)
            #builds winner message, cards for display and dealer's hand value
            msg = game_msg(game_result[0])
            dealer_hand = display_cards(game_result[1])
            dealer_val = hand_val(game_result[1])
            #updates user's score
            users[currentuser].score = users[currentuser].score + game_result[0]
            #cleans out unwanted artifact
            if "favicon.ico" in users.keys():
                del users["favicon.ico"]
            #creates leader board     
            leaderbd = list(users.values())
            leaderbd = sort_leaderbd(leaderbd)
            leaderbd_len = len(leaderbd)
            # resets system variables
            teardn()
            # launches dealer.html page
            return render_template("dealer.html", username = username, playerhand=playerhand, playerval=player_val, 
            dealerhand=dealer_hand, dealerval=dealer_val, score = users[currentuser].score, form=form, msg = msg, 
            leaderbd=leaderbd, leaderbd_len=leaderbd_len)
            
        if button == "quit":
            
            return redirect(url_for('index'))
            
        if button == "new":
            
            return redirect( url_for('user', username = username))    

    #renders game page before user decideds to hit or stay.
    return render_template("game.html", username = username, playerhand=playerhand, playerval=player_val, form=form, odds=odds,
    decksize=decksize)




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
          

