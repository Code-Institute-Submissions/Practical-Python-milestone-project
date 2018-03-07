import os
from random import choice, randint
from collections import Counter

cards = ["2","3","4","5","6","7","8","9","10", "J", "Q", "K", "A"]
picture_cards = ["J", "Q", "K"]
suits = ["C", "S", "D", "H"]
num_cards = ["2","3","4","5","6","7","8","9","10", "A"]
ace = "A"
hand = []

# creates a card shoe.  A cardshoe is the device that holds multiple of decks of cards.

def card_shoe(num = 1):
    # if num is less than 1, then set it to 1
    try:
        x = int(num)
    except:
        num = 1
    
    if num != int(num):
        num = 1
        
    if num < 1:
        num = 1
    deck = []    
   
    for suit in suits:
        for card in cards:
            newcard = card + suit
            deck.append(newcard)
    shoe = deck * num
    return shoe
    
def card_val(card):
    if card[0] in picture_cards:
        return 10
    elif card[0] == ace:
        return 1
    elif card[0:2] == "10":  
        return 10
    else:
        return int(card[0])

def hand_val(dealthand = []):
    total_aces = 0
    total = 0
    for card in dealthand:
        if not dealthand:
            return 0
        elif card[0] == ace:
            total_aces += 1
            if total >= 11: 
                total+= 1 
            else: total += 11    
        else:            
            total += card_val(card)
    if total > 21 and total_aces > 0:
            total = total - 10
    return total


def getcard(working_decks):
    deck_lenth = len(working_decks)
    random_idx = randint(0, deck_lenth - 1)
    next_card = working_decks[random_idx]
    del working_decks[random_idx]
    return (next_card, working_decks)
    
    
def init_deal(working_decks):
    #get two cars
    two_cards = []
    for x in range(2):
        card = getcard(working_decks)
        two_cards.append(card[0])
    return two_cards    
    
def hit_me(working_decks, hand):
    newcard = getcard(working_decks)
    hand.append(newcard[0])
    return hand

def odds_to_bust(working_deck, value):
    deck_size = len(working_deck)
    
    if value <= 10:
        return 100
    
    if value >= 21:
        return 0
    
    if value == 11:
        num_aces = 0
        for card in working_deck:
            if card[0] == "A":
                num_aces += 1
        odds = ((deck_size - num_aces) / deck_size) * 100
        return round(odds)
    
    if value > 11:
        totalTest = 0
        for card in working_deck:
            if card_val(card) <= 21 - value:
                totalTest += 1
        odds = (totalTest / deck_size) * 100
        return round(odds)       

    
    
    
   
    
        

    


    



