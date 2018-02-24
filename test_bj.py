import unittest
import blackjack

class  TestBlackjack(unittest.TestCase):
    """
    Defines the test for blackjack.py key functions.
    
    function backjack.card_shoe(num) buils a shoe of multiple decks
    where num is number playing decks.
    """
    # defined a test build a deck of cards.   
    
    
    def test_cardshoe(self):
        cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        test_deck = cards * 4
        
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
        

if __name__ == '__main__':
    unittest.main()

