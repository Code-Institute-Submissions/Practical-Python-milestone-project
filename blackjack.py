import os
import random

cards = ["2","3","4","5","6","7","8","9","10", "J", "Q", "K", "A"]
picture_cards = ["J", "Q", "K"]
ace = "A"
hand = []

# creates a card shoe.  A card shoe is the device that holds multiple of decks of cards.

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
        
    deck = cards * 4
    shoe = deck * num
    return shoe
    
def card_val(card):
    if card in picture_cards:
        return 10
    elif card == ace:
        return (1, 11)
    else:
        return int(card)

def hand_val(dealthand = []):
    total_aces = 0
    total = 0
    for card in dealthand:
        if not dealthand:
            return 0
        elif card == ace:
            if total >= 11: 
                total_aces += 1
                total+= 1 
            else: total += 11    
        else:            
            total += card_val(card)
    if total > 21 and total_aces >= 1:
            total -= 10
    return total

# build function to be dealt a hand....
# function get a card....
    



