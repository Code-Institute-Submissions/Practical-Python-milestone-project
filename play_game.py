from blackjack import *
from dataio import savedata, loaddata


num_decks = 5
min_num_card  = 100

LEADERBD_SIZE = 4

		
def per_play(player, dealer, deck):
    playerhand = hand_val(player)
    dealerhand = hand_val(dealer)
    odds = 100 - odds_to_bust(deck, playerhand)
    for crd in player:
        print(crd)
    print(" player's hand value: {0}, odds of going bust a hit {1}%.".format(playerhand, odds ))
    print(" dealer's hand value: {0}.".format(dealerhand))
    print("cards in the deck are {0} \n".format(len(deck)))

# return status one if player wins, 0 for tie and -1 for a loss
# track number of games played and score per user

def getwinner(player, dealer, deck):
    status = 0
    if hand_val(player) > 21 and hand_val(dealer) <= 21:
        status = -1
        print("dealer wins! player has {0}".format(hand_val(player)))
        return status
        
    if hand_val(player) == hand_val(dealer):
        status = 0
        print("It's a push! player and dealer has {0}".format(hand_val(player)))
        return status
        
    if hand_val(player) < hand_val(dealer):    
        status = -1
        print("dealer wins! player has {0}".format(hand_val(player)))
        return status
        
    while hand_val(dealer) < hand_val(player):
        dealer = hit_me(deck, dealer)
        print("player's hand is {0}, dealer has {1} {2}".format(hand_val(player), hand_val(dealer), dealer))
        if hand_val(dealer) > 21:
            status = 1
            print("dealer goes bust with {0}".format(list(dealer)))
            break
        if hand_val(player) == hand_val(dealer):
            status = 0
            print("It's a push! player and dealer has {0}".format(hand_val(player)))
            break
        if hand_val(dealer) > hand_val(player):
            print("dealer wins with {0} vs player {1}".format(hand_val(dealer), hand_val(player)))
            status = -1
            break
    print("status: {0}".format(status))
    return status    
    
def play_game(deck, user):
    users[user].hand = []
    dealer_hand = []
    choice = "Y"
    status = "init"
    #build the card shoe
    #initial deal
    users[user].hand = init_deal(deck)
    dealer_hand = init_deal(deck)
    per_play(users[user].hand, dealer_hand, deck)
    # user plays
    while choice == "Y":
        value = hand_val(users[user].hand)
        if value == 21 and status == "init":
            print("Blackjack! Congrats")
            break
        choice = input("hit me (Y or N): ")
        if choice.upper() == "N":
            break
        choice = "Y"
        status = "active"
        users[user].hand = hit_me(deck, users[user].hand)
        per_play(users[user].hand, dealer_hand, deck)
        if hand_val(users[user].hand) > 21:
            print("you've gone bust")
            break
    #dealer plays
    users[user].score = users[user].score + getwinner(users[user].hand,dealer_hand, deck)   
    users[user].hand = []
    return
    
def getuser():
    user = input("Enter user name:  ")
    if user.lower() not in list(users.keys()):
        users[user.lower()] = Player(user.lower())
    return users[user.lower()].name    


    
if __name__ == '__main__':
    # trys to load users dictionary.
    
    try:
        users = loaddata("data/users.pickle")
    except:
        users = {}
    
    # starts game, builds working deck of cards.
    print("Welcome to Blackjack\n")
    working_deck = card_shoe(num_decks)
    
    # sets up the current user, by their name, which is key to
    # player's object.    The player's object keeps the user hand and score.
    
    currentuser =  getuser() 

    while True:
        play_game(working_deck, currentuser)
        savedata(users,"data/users.pickle" )
        print("{0} score: {1}".format(currentuser, users[currentuser].score))
        print("\n \n")
        leaderbd = list(users.values())
        leaderbd = sort_leaderbd(leaderbd)
        if len(leaderbd) < LEADERBD_SIZE:
            for i in range(len(leaderbd)):
                print(leaderbd[i].name + "\t" + str(leaderbd[i].score))
        else:
            for i in range(LEADERBD_SIZE):
                print(leaderbd[i].name + "\t" + str(leaderbd[i].score))
        
        print("\n \n")
        play = input("Play another game? Y/N: ")
        if play.upper() != "Y":
            break
        if len(working_deck) < 50:
            working_deck = card_shoe(num_decks)
    
    