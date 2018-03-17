"""
play_game.py 

The program provides helper funtions required to play a hand of blackjack

- setup_bj() loads the users, the list of players from persistent storage.
    the users of list is comprised of Player objects.  When a user signs into the game,
    a player that keeps track of it's user name, score and active hand is created.
    If there is list of users, a pickle file, then an empty list is created.

- getuser(user, users) is as part of the game log in process to check if the username 
    logged in on the index page exists in the user list.  If not, it creates a new
    user using the Player object.   Returns the user's name, which is used as key
    to access that user's player object e.g. users[key]

- getwinner_web(player, dealer, deck) accepts: player - the user's hand, 
    dealer - the initial two hand card of the dealer, deck - the current working deck
    i.e. the card shoe.  The function then plays the rest of dealer's hand trying to
    beat the user.  It returns, a status code and the dealer's final hand.  The status
    is used to keep score in the leader board: 1 if player wins, -1 if dealer win and 
    0 for a push.  The dealer hand is used later on display the hand.
    
    
"""

from blackjack import hand_val, hit_me, Player
from dataio import savedata, loaddata

# loads list of active users from the server.  relies of functions
# from dataio.py
def setup_bj():
    try:
        users = loaddata("data/users.pickle")
        return users
    except:
        users = {}
        return users

#set's up user name, takes the user object, check the users list
#returns user's name, which is required as key to access Player attributes.
#key must be lower case.
def getuser(user, users):
    if user.lower() not in list(users.keys()):
        users[user.lower()] = Player(user.lower())
    return users[user.lower()].name            

# getwinner_web plays dealer's hand.  
# accepts player - a list of the player's card, dealer a list of dealers card, 
# deck, the list of all available cards to play,   The _web was artifact from
# orginal getwinner which similar, but written for the CLI version of the game.
def getwinner_web(player, dealer, deck):
    status = 0
    # if player hand is bust, the dealer wins.  No player required.
    if hand_val(player) > 21 and hand_val(dealer) <= 21:
        status = -1
        # print("dealer wins! player has {0}".format(hand_val(player)))
        return (status, dealer)
    
    #if the hand is tie, it's a push.     
    if hand_val(player) == hand_val(dealer):
        status = 0
        # print("It's a push! player and dealer has {0}".format(hand_val(player)))
        return (status, dealer)
    
    # if the dealer and player hand is less than 21 and dealer is greater than
    # 21, the dealer wins
    if hand_val(player) < hand_val(dealer):    
        status = -1
        # print("dealer wins! player has {0}".format(hand_val(player)))
        return (status, dealer)
    
    # plays out dealer, gets new cards until wins or bust or tie     
    while hand_val(dealer) < hand_val(player):
        dealer = hit_me(deck, dealer)
        # dealer loses, goes over
        if hand_val(dealer) > 21:
            status = 1
            break
        # a tie
        if hand_val(player) == hand_val(dealer):
            status = 0
            break
        # dealer wins
        if hand_val(dealer) > hand_val(player):
            status = -1
            break
    return (status, dealer)  
    
  