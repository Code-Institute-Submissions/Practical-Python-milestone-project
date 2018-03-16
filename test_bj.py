import unittest
import play_game
import blackjack

class  TestBlackjack(unittest.TestCase):
    """
    test_bj.py is unittest program for verifying the operation of
    various key functions in playgame.py and blackjack.py.
    
    Defines the test for blackjack.py key functions.
    
    function backjack.card_shoe(num) buils a shoe of multiple decks
    where num is number playing decks.
    
    Test peformed:
    
    - test to blackjack.card_shoe() correctly builds a card shoe of decks
    - test that blackjack.card_val correctly determine value of card
    - verifies that blackjack.hand_val() can calculate the value of hand
    - verifies that blackjack.getcard removes cards from the card shoe
    - verifies that blackjack.odds_to_bust correctly determines the odds that card will cause 
      player to go over 21.
    - verifies the dealer play and determine the winner play_game.getwinner
    
    
    """
    # defined a test build a deck of cards.   
    
    
    def test_cardshoe(self):
        cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        test_deck = ["2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
        "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS",
        "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",
        "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH"]
        
        
        # test default value of one deck. 

        self.assertEqual(blackjack.card_shoe(1), test_deck*1)
        self.assertEqual(blackjack.card_shoe(), test_deck*1)
        
        # build five decks
        self.assertEqual(blackjack.card_shoe(5), test_deck*5)
        # self.assertEqual(blackjack.card_shoe(), test_deck*5)  # test designed to fail.
    
        # if an integer not entered, convert to 1 deck
        self.assertEqual(blackjack.card_shoe(-1), test_deck*1)
        self.assertEqual(blackjack.card_shoe(4.5), test_deck*1)
        self.assertEqual(blackjack.card_shoe("a"), test_deck*1)
    
    """
    Test if the value of card is correct

    """
    
    # test to verify card values.
    def test_cardvalue(self):
        self.assertEqual(blackjack.card_val("JC"), 10)
        self.assertEqual(blackjack.card_val("QH"), 10)
        self.assertEqual(blackjack.card_val("KS"), 10)
        self.assertEqual(blackjack.card_val("10S"), 10)
        self.assertEqual(blackjack.card_val("2D"), 2)
        self.assertEqual(blackjack.card_val("5D"), 5)
        self.assertEqual(blackjack.card_val("9C"), 9)
        self.assertEqual(blackjack.card_val("AC"), 1)
        
    # test to verify hand value    
    def test_handvalue(self):
        self.assertEqual(blackjack.hand_val([]), 0)
        self.assertEqual(blackjack.hand_val(["3C","2H","9S"]), 14)
        self.assertEqual(blackjack.hand_val(["2C","2D","JS"]), 14)
        self.assertEqual(blackjack.hand_val(["6D","2H","QS"]), 18)
        self.assertEqual(blackjack.hand_val(["4S","2C","KD"]), 16)
        self.assertEqual(blackjack.hand_val(["4C","JD","KD"]), 24)
        self.assertEqual(blackjack.hand_val(["AS","2C"]), 13)
        self.assertEqual(blackjack.hand_val(["AH","AD"]), 12)
        self.assertEqual(blackjack.hand_val(["AC","JS"]), 21)
        self.assertEqual(blackjack.hand_val(["2D","AH","2C"]), 15)
        self.assertEqual(blackjack.hand_val(["2C","AC","AH"]), 14)
        self.assertEqual(blackjack.hand_val(["2H","AH","AC", "8S"]), 12)
        self.assertEqual(blackjack.hand_val(["2H","AH","AC","AS", "7S"]), 12)
        self.assertEqual(blackjack.hand_val(["8C","AC", "4D"]), 13)
        self.assertEqual(blackjack.hand_val(["8C","AC", "8D"]), 17)
    
    # test card is removed from the deck when it's drawn into a hand
    # the assetIn test was designed to fail.  
    def test_get_card(self):
        working_decks = blackjack.card_shoe(1)
        # self.assertIn(blackjack.getcard(working_decks), working_decks)
        self.assertNotIn(blackjack.getcard(working_decks), working_decks)
        
    # test if odds to player going over 21 are calculated correctly    
        
    def test_odd(self):
        working_decks = blackjack.card_shoe(1)
        self.assertEqual(blackjack.odds_to_bust(working_decks, 9),  100)
        self.assertEqual(blackjack.odds_to_bust(working_decks, 5),  100)
        self.assertEqual(blackjack.odds_to_bust(working_decks, 0),  100)
        self.assertEqual(blackjack.odds_to_bust(working_decks, 10), 100)
        self.assertEqual(blackjack.odds_to_bust(working_decks, 21), 0)
    
        working_decks = blackjack.card_shoe(1)
        self.assertEqual(blackjack.odds_to_bust(working_decks, 11),  92)
        
        working_decks = blackjack.card_shoe(2)
        self.assertEqual(blackjack.odds_to_bust(working_decks,11),  92)
        
        self.assertEqual(blackjack.odds_to_bust(working_decks,12),  69)
        self.assertEqual(blackjack.odds_to_bust(working_decks,15),  46)
        self.assertEqual(blackjack.odds_to_bust(working_decks,19),  15)
        
        #Test the dealer play, dealer draws cards to try to beat player's scoe
        #When either deal or player wins, getwinner() returns 0 for a push
        #-1 if the dealer wins and 1 if the player wins.  These scores are added
        # Player object score attribute to keep a running total.
        working_decks = blackjack.card_shoe(2)
        #if player > 21, dealer wins status -1
        self.assertEqual(play_game.getwinner(["QH", "5D", "10D"], ["5S", "9D"], working_decks), -1)
        #dealer hand equal value to player hand, it's a push
        self.assertEqual(play_game.getwinner(["QH", "AD"], ["AS", "KD"], working_decks), 0)
        self.assertEqual(play_game.getwinner(["3H", "AD"], ["AS", "3D"], working_decks), 0)
        self.assertEqual(play_game.getwinner(["3H", "9D"], ["6S", "6D"], working_decks), 0)
        
        #dealer goes bust, player wins
        
        #dealer less than or equal 21 and greater than player, deal wins
        #   requires loops, dealer wins or goes bust

if __name__ == '__main__':
    unittest.main()

