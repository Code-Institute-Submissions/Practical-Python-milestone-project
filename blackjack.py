import os
import random

# creates a card shoe.  A card shoe is the device that holds multiple of decks of cards.

def card_shoe(num = 1):
    # if num is less than 1, then set it to 1
    if num < 1:
        num = 1
        print("negative becomes {0}".format(num))
    
    if num != int(num):
        num = 1
        print("float becomes {0}".format(num))
    
    deck = ["2","3","4","5","6","7","8","9","10", "J", "Q", "K", "A"] * 4
    shoe = deck * num
    return shoe
    



