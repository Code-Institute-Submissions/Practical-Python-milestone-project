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
    
    
# def per_play(player, dealer, deck):
    # playerhand = hand_val(player)
    # dealerhand = hand_val(dealer)
    # odds = 100 - odds_to_bust(deck, playerhand)
    # for crd in player:
        # print(crd)
    # print(" player's hand value: {0}, odds of going bust a hit {1}%.".format(playerhand, odds ))
    # print(" dealer's hand value: {0}.".format(dealerhand))
    # print("cards in the deck are {0} \n".format(len(deck)))

# return status one if player wins, 0 for tie and -1 for a loss
# track number of games played and score per user



# depreciated code, used in the CLI version of the game
# def getwinner(player, dealer, deck):
#     status = 0
#     if hand_val(player) > 21 and hand_val(dealer) <= 21:
#         status = -1
#         print("dealer wins! player has {0}".format(hand_val(player)))
#         return status
        
#     if hand_val(player) == hand_val(dealer):
#         status = 0
#         print("It's a push! player and dealer has {0}".format(hand_val(player)))
#         return status
        
#     if hand_val(player) < hand_val(dealer):    
#         status = -1
#         print("dealer wins! player has {0}".format(hand_val(player)))
#         return status
        
#     while hand_val(dealer) < hand_val(player):
#         dealer = hit_me(deck, dealer)
#         print("player's hand is {0}, dealer has {1} {2}".format(hand_val(player), hand_val(dealer), dealer))
#         if hand_val(dealer) > 21:
#             status = 1
#             print("dealer goes bust with {0}".format(list(dealer)))
#             break
#         if hand_val(player) == hand_val(dealer):
#             status = 0
#             print("It's a push! player and dealer has {0}".format(hand_val(player)))
#             break
#         if hand_val(dealer) > hand_val(player):
#             print("dealer wins with {0} vs player {1}".format(hand_val(dealer), hand_val(player)))
#             status = -1
#             break
#     print("status: {0}".format(status))
#     return status    
    
# def play_game(deck, user):
#     users[user].hand = []
#     dealer_hand = []
#     choice = "Y"
#     status = "init"
#     #build the card shoe
#     #initial deal
#     users[user].hand = init_deal(deck)
#     dealer_hand = init_deal(deck)
#     per_play(users[user].hand, dealer_hand, deck)
#     # user plays
#     while choice == "Y":
#         value = hand_val(users[user].hand)
#         if value == 21 and status == "init":
#             print("Blackjack! Congrats")
#             break
#         choice = input("hit me (Y or N): ")
#         if choice.upper() == "N":
#             break
#         choice = "Y"
#         status = "active"
#         users[user].hand = hit_me(deck, users[user].hand)
#         per_play(users[user].hand, dealer_hand, deck)
#         if hand_val(users[user].hand) > 21:
#             print("you've gone bust")
#             break
#     #dealer plays
#     users[user].score = users[user].score + getwinner(users[user].hand,dealer_hand, deck)   
#     users[user].hand = []
#     return
    


# Depreciated code, used in the CLI version of the game

# def game_loop_cli(deck, user):
#     while True:
#         play_game(deck, user)
#         savedata(users,"data/users.pickle" )
#         print("{0} score: {1}".format(user, users[user].score))
#         print("\n \n")
        
#         leaderbd = list(users.values())
#         leaderbd = sort_leaderbd(leaderbd)
#         if len(leaderbd) < LEADERBD_SIZE:
#             for i in range(len(leaderbd)):
#                 print(leaderbd[i].name + "\t" + str(leaderbd[i].score))
#         else:
#             for i in range(LEADERBD_SIZE):
#                 print(leaderbd[i].name + "\t" + str(leaderbd[i].score))
        
#         print("\n \n")
#         play = input("Play another game? Y/N: ")
#         if play.upper() != "Y":
#             break
#         if len(working_deck) < 50:
#             deck = card_shoe(num_decks)
    
    
    
# if __name__ == '__main__':
#     users = setup_bj()
#     working_deck = card_shoe(num_decks)

#     # starts game, builds working deck of cards.
#     print("Welcome to Blackjack\n")

    # sets up the current user, by their name, which is key to
    # player's object.    The player's object keeps the user hand and score.
    
    # currentuser =  getuser() 
    
    # game_loop_cli(working_deck, currentuser)


    