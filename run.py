import os, json
from play_game import *
from flask import Flask, render_template, request, redirect, session, url_for
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import cards

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'well-secret-password'

# working_deck = card_shoe(num_decks) 
working_deck = card_shoe(1)
users = setup_bj()

def update_deck(working_deck):
    if len(working_deck) < 50:
        working_deck = card_shoe(num_decks)
    

class Bj_player(Form):
    name = StringField(label='Name')
    hit = SubmitField(label='Hit Me')
    stay = SubmitField(label='Stay')
    new_gm = SubmitField(label='New Game')
    quit_gm = SubmitField(label='Quit')
    

def display_cards(hand):
    playerhand = []
    for card in hand:
        playerhand.append("static/assets/SVG-cards/" + cards.cards[card])
    return playerhand    

# def clean_users(usr):
#     if "favicon.ico" in users.keys():
#         del usr["favicon.ico"]
#     return usr    
    
def game_msg(status):
    if status == 0:
        return "Tie, it's a push"
    if status == -1:
        return "Dealer Wins"
    if status == 1:
        return "Player Wins!"




@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["status"] ="initial"
        return redirect(request.form["username"])
    return render_template("index.html")
    

@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    form = Bj_player()
    # form2 = Bj_dealer()
    playerhand = []
    dealer_hand = []
    currentuser =  getuser(username, users)
    
    def teardn():
        users[currentuser].hand = []
        if "favicon.ico" in users.keys():
            del users["favicon.ico"]
        savedata(users,"data/users.pickle" )
        session["status"] = "initial"
        session["player_hand"] = []
        
        
        return
    # test value
    decksize = len(working_deck)
    #
    if session["status"] == "initial": 
        users[currentuser].hand = []
        users[currentuser].hand = init_deal(working_deck)
        session["status"] = "player"
        session["player_hand"] = users[currentuser].hand
        player_val = hand_val(users[currentuser].hand)
        playerhand = display_cards(users[currentuser].hand)
        odds = 100 - odds_to_bust(working_deck, player_val)
        
        #if player hand value 
        
    else:
        users[currentuser].hand = session["player_hand"]
        player_val = hand_val(users[currentuser].hand)
        playerhand = display_cards(users[currentuser].hand)
        odds = 100 - odds_to_bust(working_deck, player_val)
        
    #examine cards to see if their is a winner.  Get dealers cards.
    
    dealer_hand = init_deal(working_deck)     
    
    if form.validate_on_submit():
        name=form.name.data
        # button="hit" if form.hit.data else "stay"
        if form.hit.data:
            button = "hit"
        elif form.stay.data:
            button = "stay"
        elif form.new_gm.data:  
            button = "new"
        else:
            button = "quit"
        
        
        if  button == "hit":
            users[currentuser].hand = session["player_hand"]
            users[currentuser].hand = hit_me(working_deck, users[currentuser].hand)
            
            session["player_hand"] = users[currentuser].hand
            
            player_val = hand_val(users[currentuser].hand)
            playerhand = display_cards(users[currentuser].hand)
            odds = 100 - odds_to_bust(working_deck, player_val)
            
            if player_val > 21:
                dealerhand = display_cards(dealer_hand)
                dealer_val = hand_val(dealer_hand)
                users[currentuser].score = users[currentuser].score + -1  
                msg = game_msg(-1)
                if "favicon.ico" in users.keys():
                    del users["favicon.ico"]
                leaderbd = list(users.values())
                leaderbd = sort_leaderbd(leaderbd)
                leaderbd_len = len(leaderbd)
                teardn()
                
                return render_template("dealer.html", username = username, playerhand=playerhand, playerval=player_val, 
                dealerhand=dealerhand, dealerval=dealer_val, score = users[currentuser].score, form=form, msg = msg, 
                leaderbd=leaderbd, leaderbd_len=leaderbd_len)
           
            # if message is 21
            if player_val == 21:
                session["status"] = "dealer"
                game_result = getwinner_web(users[currentuser].hand, dealer_hand, working_deck)
                msg = game_msg(game_result[0])
                dealer_hand = display_cards(game_result[1])
                dealer_val = hand_val(game_result[1])
                users[currentuser].score = users[currentuser].score + game_result[0]
                if "favicon.ico" in users.keys():
                    del users["favicon.ico"]
                leaderbd = list(users.values())
                leaderbd = sort_leaderbd(leaderbd)
                leaderbd_len = len(leaderbd)
               
                teardn()
                
                return render_template("dealer.html", username = username, playerhand=playerhand, playerval=player_val, 
                dealerhand=dealer_hand, dealerval=dealer_val, score = users[currentuser].score, form=form, msg = msg,
                leaderbd=leaderbd, leaderbd_len=leaderbd_len)
            
          
            return render_template("game.html", username = username, playerhand=playerhand, playerval=player_val, form=form, odds=odds)
            
        if button == "stay":  
             
            session["status"] = "dealer"
            game_result = getwinner_web(users[currentuser].hand, dealer_hand, working_deck)
            msg = game_msg(game_result[0])
            dealer_hand = display_cards(game_result[1])
            dealer_val = hand_val(game_result[1])
            users[currentuser].score = users[currentuser].score + game_result[0]
            if "favicon.ico" in users.keys():
                del users["favicon.ico"]
            leaderbd = list(users.values())
            leaderbd = sort_leaderbd(leaderbd)
            leaderbd_len = len(leaderbd)
            teardn()
            
            # users[currentuser].hand = []
            # savedata(users,"data/users.pickle" )
            # session["status"] = "initial"
            # session["player_hand"] = []
            
            return render_template("dealer.html", username = username, playerhand=playerhand, playerval=player_val, 
            dealerhand=dealer_hand, dealerval=dealer_val, score = users[currentuser].score, form=form, msg = msg, 
            leaderbd=leaderbd, leaderbd_len=leaderbd_len)
            
        if button == "quit":
            
            return redirect(url_for('index'))
            
        if button == "new":
            
            return redirect( url_for('user', username = username))    

    return render_template("game.html", username = username, playerhand=playerhand, playerval=player_val, form=form, odds=odds,
    decksize=decksize)




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
          

