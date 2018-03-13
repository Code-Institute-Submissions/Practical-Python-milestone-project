import os, json
from play_game import *
from flask import Flask, render_template, request, redirect
import cards

app = Flask(__name__)
  

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect(request.form["username"])
    return render_template("index.html")

@app.route('/<username>', methods=["GET", "POST"])
def user(username):
    # load user and get a shoe of cards
    users = setup_bj()
    working_deck = card_shoe(num_decks)
    currentuser =  getuser(username, users)
    #Play Game
    users[currentuser].hand = []
    dealer_hand = []
    choice = "Y"
    status = "init"
    #build the card shoe
    #initial deal
    users[currentuser].hand = init_deal(working_deck)
    dealer_hand = init_deal(working_deck)
    # hand = " ".join(str(x) for x in users[currentuser].hand)
    playerhand = []
    for card in users[currentuser].hand:
        playerhand.append("static/assets/SVG-cards/" + cards.cards[card])

    return render_template("game.html", username = username, playerhand=playerhand)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

