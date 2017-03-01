import Game
import time
import random
import math

g = Game.Game()
white_move_count = 0
black_move_count = 0

# print("White player rolled {}, Black player rolled {}".format(p1Roll[0] + p1Roll[1], p2Roll[0] + p2Roll[1]))
p1Roll = (0,0)
p2Roll = (0,0)
while sum(p1Roll) == sum(p2Roll):
    p1Roll = g.roll_dice()
    p2Roll = g.roll_dice()

    if sum(p1Roll) > sum(p2Roll):
        print("White player gets the first turn...")
        g.turn = g.players[0]
    else:
        print("Black player gets the first turn")
        g.turn = g.players[1]
start = 1
move_count = 1

while not g.game_over():
        actions = []

        if start == 1:
                actions = g.find_moves(p1Roll, g.turn)
                start = 0
        else:
                actions = g.find_moves(g.roll_dice(), g.turn)
        states = []

        if len(actions) == 0:
            g.turn = g.get_opponent(g.turn)

        else:
            move_count += 1
            g.take_action(g.turn, actions[random.randint(0,len(actions) - 1)])
            g.turn = g.get_opponent(g.turn)


        # for action in actions:
        #     states.append(g.take_action(g.turn, action))
        #     g.turn = g.get_opponent(g.turn)

        # print(len(states))
        # time.sleep(1)
        print("MOVE COUNT: {}".format(move_count))
