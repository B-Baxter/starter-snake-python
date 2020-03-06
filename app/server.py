import json
import os
import random
import math

import bottle
from bottle import HTTPResponse


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#009999", "headType": "sand-worm", "tailType": "bwc-bonhomme"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    print("MOVE:", json.dumps(data))
    working_data = sort_it(data)
    move = decision_tree(working_data)
    final_move = collision(move)

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "PyGod!"

    response = {"move": final_move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )
def decision_tree(in_put):
    nfl,nel = in_put
    for i in range(0,len(nel)):
        if nfl[i][1] < nel[0][1]:
            choice = move_to(nfl[i][0])
            break
        elif nfl[i][1] > nel[0][1]:
            choice = move_away(nel[i][1])
            break
        elif nfl[i][1] == nel[0][1]:
            choice = evade_move()
            break
        else:
            pass
    return choice
def move_to(location):
    if (location[0]["x"] - me[0]["x"]) > (location[0]["y"] - me[0]["y"]):
        if location[0]["x"] > me[0]["x"]:
            return "up"
        elif location[0]["x"] < me[0]["x"]:
            return "down"
    elif (location[0]["x"] - me[0]["x"]) <= (location[0]["y"] - me[0]["y"]):
        if location[0]["y"] > me[0]["y"]:
            return "left"
        elif location[0]["y"] < me[0]["y"]:
            return "right"

def move_away(location):
    if (location[0]["x"] - me[0]["x"]) > (location[0]["y"] - me[0]["y"]):
        if location[0]["x"] > me[0]["x"]:
            return "down"
        elif location[0]["x"] < me[0]["x"]:
            return "up"
    elif (location[0]["x"] - me[0]["x"]) <= (location[0]["y"] - me[0]["y"]):
        if location[0]["y"] > me[0]["y"]:
            return "right"
        elif location[0]["y"] < me[0]["y"]:
            return "left"

def evade_move():
    directions = ["up", "down", "left", "right"]
    move = random.choice(directions)
    return move

def collision(move):
    me_rn = me
#Get new position
    if move == "right":
        me_rn[0]["x"] = (me_rn[0]["x"] + 1)
    elif move == "left":
        me_rn[0]["x"] = (me_rn[0]["x"] - 1)
    elif move == "up":
        me_rn[0]["y"] = (me_rn[0]["y"] + 1)
    elif move == "down":
        me_rn[0]["y"] = (me_rn[0]["y"] - 1)
#evalute new position
    if (me_rn > height or me_rn == 0):
        move = evade_move()
    elif (me_rn > height or me_rn == 0):
        move = evade_move()
    for snake in enemy:
        for segment in snake[body]:
            if me_rn == segment:
                move = evade_move()
    return move


def get_distance(coord1,coord2): 
    print(coord1,type(coord1))
    print(coord2,type(coord2))
    return (abs(coord1["x"]-coord2["x"]) + abs(coord1["y"]-coord2["y"]))

def sort_it(data):
    #state = json.loads(data.text)
    state = data
    game = state["game"]["id"]
    height = state["board"]["height"]
    width =  state["board"]["width"]
    turn = state["turn"]
    food = state["board"]["food"]
    enemy = state["board"]["snakes"]
    me = state["you"]["body"]
    food_distance = []
    for morsel in food:
        dist = get_distance(morsel,me[0])
        food_distance.append([morsel,dist])
    enemy_distance = []
    for npc in enemy:
        dist = get_distance(npc["body"][0],me[0])
        enemy_distance.append([npc,npc["id"],dist])
    nearest_food_list = sorted(food_distance, key=lambda food: food[1])
    neartest_enemy_list = sorted(enemy_distance, key=lambda enemy: enemy[2])
    return nearest_food_list,neartest_enemy_list

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
