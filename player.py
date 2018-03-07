class Player:
    
    def __init__(self, name, hand=[], score=0):
        self.name = name
        self.hand = hand
        self.score = score

        
    def update_score(self, score):
        self.score = self.score + score
        
    def set_score(self, value):
       self.score = value
       
    def set_hand(self, hand):
        self.hand = hand
    
    def reset_hand(self):
        self.hand = []
        

 # build a function to find and sort the top ten scores
 
def test_users():
        users = {}
        users["joe"] = Player("joe", [], 90)
        users["sarah"] = Player("sarah", [], 10)
        users["Bill"] = Player("Bill", [], 60)
        users["bob"] = Player("bob", [], 1)
        return users

testdata = list(test_users().values())
sortdata = sorted(testdata, key=lambda users: users.score, reverse=True)
for i in range(4):
    print(sortdata[i].name + "\t" + str(sortdata[i].score))



        
    
       