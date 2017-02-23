import numpy as np
import random

class Game:

    def __init__(self):
        self.players = ['white', 'black']
        self.board = [[] for _ in range(24)]
        self.on_bar = {}
        self.off_board = {}
        self.pieces_left = {}
        for p in self.players:
            self.on_bar[p] = []
            self.off_board[p] = []
            self.pieces_left[p] = 15

        # Initialize the board with a hard coded set-up for each point (0 indexed!)
        for i in range(2):
            self.board[0].append('white')
        self.board[1].append('black')
        for i in range(4):
            self.board[5].append('black')
        for i in range(3):
            self.board[7].append('black')
        for i in range(5):
            self.board[11].append('white')
        for i in range(5):
            self.board[12].append('black')
        for i in range(3):
            self.board[16].append('white')
        for i in range(5):
            self.board[18].append('white')
        for i in range(2):
            self.board[23].append('black')

    def roll_dice(self):
        return (random.randint(1,6), random.randint(1,6))


    def find_moves(self, roll, player):
        moves = []

        for i in range(len(self.board)):
            self.print_point(i)

        # Probably can get rid of this and just reference the indices of the roll
        r1, r2 = roll[0], roll[1]

        j = 2

        # Did we roll doubles? Alter j to 4 if this is to be handled
        if r1 == r2:
            print("Player {} rolled double {}'s! But we won't worry about that".format(player, r1))

        for i in range(j):
            k = i - 1
            r = roll[k]
            print("R = {}".format(r))
            # Are there pieces on the bar for the given player?
            if len(self.on_bar[player]) >= 1:
                print("Player {} has pieces on the bar".format(self.on_bar[player]))
                # Does the point where we would put the piece have no pieces or is it controlled by the player?
                if self.board[r] <=1 or self.board[len(self.board[r])- 1 ] == player:
                    # Does the point where we would put the piece have 1 stone that is the opposite player's color?
                    if self.board[r] == 1 and self.board[len(self.board[r])- 1] != player:
                        # piece = self.on_bar[player].pop()
                        if self.board[r] == get_opponent(player):
                            # hit = self.board[r1-1].pop()
                            # self.on_bar[get_opponent(player)].append(hit)
                            # self.board[r1-1].append(piece);
                            moves.append(('bar', r))

                #piece = self.on_bar[p].pop()
                #self.board[r].append(piece)

            print("Player {} has no pieces on the bar".format(player))

            # Can we bear off?
            if player == 'white':
                for i in range(len(self.board) - 1):
                    if len(self.board[i]) > 0:
                        if self.board[i][0] == player:
                            if (i + r) > len(self.board):
                                print("Player {} can bear off!".format(player))
                                moves.append((i, 'off'))

            # Can the player hit the other player?
            for i in range(len(self.board) - 1):
                if len(self.board[i]) > 0:
                    if self.board[i][0] == player:
                        # Check to see if the point a roll away has 1 opponent piece
                        if (i + r) <= len(self.board) -1:
                            if len(self.board[i + r]) == 1 and self.board[i + r][0] == self.get_opponent(player):

                                print("Player {} can hit on point {}".format(player, [i + r]))
                                #hit_piece = self.board[i + r].pop()
                                #self.on_bar[self.get_opponent(player)].append(hit_piece)
                                #moved_piece = self.board[i].pop()
                                #self.board[i + r].append(moved_piece)
                                moves.append((i, i + r))
                                # print("Player {} has {} pieces on the bar".format(self.get_opponent(player), len(self.on_bar[self.get_opponent(player)])))
                                # for i in range(len(self.board)):
                                #     self.print_point(i)

            # Can the player make a valid move with the roll?
            for i in range(len(self.board) - 1):
                if len(self.board[i]) > 0:
                    if self.board[i][0] == player:
                        if i + r <= len(self.board) - 1:
                            if len(self.board[i + r]) == 0 or self.board[i + r][0] == player:
                                move = (i, i + r)
                                # moves.append[(i, i + r)]
                                moves.append(move)

        # Can the player make a valid move with the combination of rolls?
        combo = r1 + r2
        for i in range(len(self.board) - 1):
            if len(self.board[i]) > 0:
                if self.board[i][0] == player:
                    # Check to see if a valid move w/ roll 1 can be made to to bear off with combo
                    if (i + r1 <= len(self.board)) and (i + combo> len(self.board)):
                        moves.append((i, 'off'))
                    # Check validity of rest of moves
                    if i + combo <= len(self.board):
                        if len(self.board[i + combo]) <= 1:
                            # When taking action, check for hit!
                            moves.append((i, i + combo))

        print("Player {} possible moves: {}".format(player, moves))

    # def take_action(self, player, action):
        # for i in range(len(self.board)):
        #     if len(self.board[i]) > 0:
        #         if self.board[i][0] == player:
        #             if i + r1 <= len(self.board):
        #                 if len(self.board[i + r1]) == 0 or self.board[i + r1][0] == player:
        #                     print("moving a piece from point {} to point {}".format(i, i + r1))
        #                     piece = self.board[i].pop()
        #                     self.board[i + r1].append(piece)
        #                     for i in range(len(self.board)):
        #                         self.print_point(i)

    # Check to see if the game is over
    def game_over(self):
        for p in self.players:
            if (self.off_board[p] == 15 and self.pieces_left[p] == 0):
                True
            else:
                return False

    # Get the opposite color of the given player (useful for hitting)
    def get_opponent(self, player):
        for p in self.players:
            if p != player:
                return p

    # Determine which player has won
    def find_winner(self):
        if (self.off_board[0] == 15 and self.pieces_left[0] == 0):
            self.players[0]

        return self.players[1]

    # Print the contents of a desired point on the board
    def print_point(self, point):
        print("Point #{} has {} pieces: {}".format(point, len(self.board[point]), self.board[point]))
