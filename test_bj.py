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
    
    """
    Test if the value of card is correct

    """
    
    def test_cardvalue(self):
        self.assertEqual(blackjack.card_val("J"), 10)
        self.assertEqual(blackjack.card_val("Q"), 10)
        self.assertEqual(blackjack.card_val("K"), 10)
        self.assertEqual(blackjack.card_val("2"), 2)
        self.assertEqual(blackjack.card_val("5"), 5)
        self.assertEqual(blackjack.card_val("9"), 9)
        self.assertEqual(blackjack.card_val("A"), (1, 11))
        
    def test_handvalue(self):
        self.assertEqual(blackjack.hand_val([]), 0)
        self.assertEqual(blackjack.hand_val(["1","2","9"]), 12)
        self.assertEqual(blackjack.hand_val(["1","2","J"]), 13)
        self.assertEqual(blackjack.hand_val(["6","2","Q"]), 18)
        self.assertEqual(blackjack.hand_val(["4","2","K"]), 16)
        self.assertEqual(blackjack.hand_val(["4","J","K"]), 24)
        self.assertEqual(blackjack.hand_val(["A","2"]), 13)
        self.assertEqual(blackjack.hand_val(["A","A"]), 12)
        self.assertEqual(blackjack.hand_val(["A","J"]), 21)
        self.assertEqual(blackjack.hand_val(["2","A","2"]), 15)
        self.assertEqual(blackjack.hand_val(["2","A","A"]), 14)
        self.assertEqual(blackjack.hand_val(["2","A","A", "8"]), 12)
        self.assertEqual(blackjack.hand_val(["2","A","A","A", "7"]), 12)

if __name__ == '__main__':
    unittest.main()

