"""
blackjack.py

This program includes the basic building blocks for playing a blackjack hand. 

It starts by building up a card shoe, combining several decks into a single
stack of cards for playing.

Key objects:

- Player tracks the user, their current hand and aggregate score 


Key functions:

-   card_shoe(num = 1) 

    num is the number of decks, integer

    The card_shoe function accepts a number of decks and produces a collection
    of card decks.  If num is not specified or if num is not an integer, the value 
    of num defaults to a single deck.  It then builds a deck card from constants 
    and multiply decks by number of decks required, returning a list of cards e.g.
    two decks returns a list of 102 cards, two standard decks.  Cards in a deck
    are represented by number and suit pair.
    
    
- card_val(card):
    card_val accepts card, card number and suit, e.g. 2C for 2 of clubs,
    and determines the cards value.  Aces can be either 1 or 11.  They are handle
    in other functions.  

- hand_val(dealthand = [])
    accepts a list of card-suit pairs, dealthand, and uses card_val to determine the point 
    value of a particular hand.  Depending on the value and hand and number of aces,
    a total is calculated the highest score depending on if an ace is valued at 1 or 11.

- getcard(working_decks)
    accept list of cards representing the card show and pulls a card. 
    It removes the card from the deck and returns a tuple of (card, deck).
    The card is card retrieved by the deck and deck is the working_deck with that card
    removed.  A random number is used to identify an index of card to be removed. 
  
- init_deal(working_decks) accepts the current list of cards and returns a list 
    two cards, the initial blackdeal.  It uses getcard() to retrieve a card.

- hit_me(working_decks, hand) accepts the current list of cards and current hand
    uses getcard to retrieve a new card and append to current hand.  It returns
    a list of cards representing a new hand.
    
- odds_to_bust(working_deck, value), accepts the current list of card in the cardshoe,
    and value of current hand and determines odds to bust, by counting the cards that 
    can result in hand going over 21 vs the number of cards in the deck.
    returns percentage, as a integer, that reprents odds of hand going over 21.
    
- sort_leaderbd(leader) accepts a list of Player objects and sorts the list in 
    decending order and returns the sorted list
    
    
"""



import os
from random import choice, randint
from collections import Counter


# constants and list for building a deck
cards = ["2","3","4","5","6","7","8","9","10", "J", "Q", "K", "A"]
picture_cards = ["J", "Q", "K"]
# C for clubs, S for spades, D for diamonds and H for hearts
suits = ["C", "S", "D", "H"]
num_cards = ["2","3","4","5","6","7","8","9","10", "A"]
ace = "A"
hand = []

# creates a card shoe.  A cardshoe is the device that holds multiple of decks of cards.

class Player:
    
    """
    Player object is institaite for each user.  It has attributes to
    store the player's name, their current hand, and rolling score.
    
    The hand is set back to empty when the hand is finished.  The score is incremented  by one 
    for each hand won, reduced by 1 for each loss, and no action for a tie.
    
    """
    
    def __init__(self, name, hand=[], score=0):
        self.name = name
        self.hand = hand
        self.score = score

        
    # def update_score(self, score):
    #     self.score = self.score + score
        
    # def set_score(self, value):
    #   self.score = value
       
    # def set_hand(self, hand):
    #     self.hand = hand
    
    # def reset_hand(self):
    #     self.hand = []
        

 # build a function to find and sort the top ten scores
 

# Build card shoe, default value of 1 deck
def card_shoe(num = 1):
    # if num is less than 1, then set it to 1
    # if a number is not integer, 0 or negative, it default to a single deck
    
    try:
        x = int(num)
    except:
        num = 1
    
    if num != int(num):
        num = 1
        
    if num < 1:
        num = 1
    deck = []    
   
   # builds a deck from basic components of card digits and card suits.
    for suit in suits:
        for card in cards:
            newcard = card + suit
            deck.append(newcard)
    #creates shoe of multiple 52 card decks        
    shoe = deck * num
    return shoe
    
# detemines card's value.      
def card_val(card):
    # if the first digit is a J, Q, K it is given a value of 10
    if card[0] in picture_cards:
        return 10
    elif card[0] == ace:
        return 1
    # slices of the cards suit to detemine value.    
    elif card[0:2] == "10":  
        return 10
    else:
        return int(card[0])

# calculate a list of cards of point value.
def hand_val(dealthand = []):
    total_aces = 0
    total = 0
    for card in dealthand:
        # if list is empty
        if not dealthand:
            return 0
        # counts the number of aces    
        elif card[0] == ace:
            total_aces += 1
            # an ace is set to 1, so not send a hand bust
            if total >= 11: 
                total+= 1 
            else: total += 11    
        else:            
            total += card_val(card)
    # if a hand value is over 21, set ace to value of 1        
    if total > 21 and total_aces > 0:
            total = total - 10
    # return total value        
    return total

# randomly retrieve a card from the collection of cards
# and remove it from the deck
def getcard(working_decks):
    deck_lenth = len(working_decks)
    #determine size of list of cards, the working_deck
    #randomly selects card from the deck, by index
    random_idx = randint(0, deck_lenth - 1)
    next_card = working_decks[random_idx]
    #removes selected card from the deck
    del working_decks[random_idx]
    #returns selected card and updated list of cards
    return (next_card, working_decks)
    
# uses current list of cards and selects two cards    
def init_deal(working_decks):
    two_cards = []
    for x in range(2):
        card = getcard(working_decks)
        # grabs card from getcard return tuple
        two_cards.append(card[0])
    return two_cards    

# adds a new card to existing hand.  The hand is a list of cards.   
def hit_me(working_decks, hand):
    newcard = getcard(working_decks)
    hand.append(newcard[0])
    return hand
    
# calculates the odds to bust.
def odds_to_bust(working_deck, value):
    deck_size = len(working_deck)
    # if hand's value is less than 10, any card works.
    if value <= 10:
        return 100
    # if the value is over 21, no card works
    if value >= 21:
        return 0
        
    # if the value is 11, any card but aces work.
    # technically, an ace can be 1, so any card works, 
    # the difference is really major.
    if value == 11:
        num_aces = 0
        for card in working_deck:
            if card[0] == "A":
                num_aces += 1
        odds = ((deck_size - num_aces) / deck_size) * 100
        return round(odds)
        
    #if the value is over 11 count cards in the deck that 
    #keeps the total below 21
    if value > 11:
        totalTest = 0
        for card in working_deck:
            if card_val(card) <= 21 - value:
                totalTest += 1
        odds = (totalTest / deck_size) * 100
        return round(odds)       
        
def sort_leaderbd(leader):
    sortedboard = sorted(leader, key=lambda users: users.score, reverse=True)
    return sortedboard
            

    
    
    
   
    
        

    


    



