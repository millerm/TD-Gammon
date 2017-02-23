import Game

g = Game.Game()

r = g.roll_dice()
g.find_moves(r, g.players[0])
