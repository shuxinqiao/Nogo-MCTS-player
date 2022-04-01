#!/usr/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from board import GoBoard

# Assignment 4 import
from ucb import runUcb
from pattern import pattern_move, check_neighbor
import numpy as np
import os


# Assignment 4 Global
cwd = os.getcwd()
weights_data = np.loadtxt(cwd + "weights.txt")

#################################################
'''
This is a uniform random NoGo player served as the starter code
for your (possibly) stronger player. Good luck!
'''
class NoGo:
    def __init__(self):
        """
        NoGo player that selects moves randomly from the set of legal moves.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """

        self.name = "NoGo4"
        self.version = 1.0
        self.simulations_per_move = 200
        self.best_move = None

        # Assignment 4 New
        self.ucb_C = 0.4


    def simulate(self, board, move, toplay):
        """
        Run a simulated game for a given move.
        """
        cboard = board.copy()
        cboard.play_move(move, toplay)
        #opp = GoBoardUtil.opponent(toplay)
        return self.simulate_game(cboard), cboard


    def simulate_game(self, board):
        limit=50

        for _ in range(limit):
            color = board.current_player
            # random move
            move = GoBoardUtil.generate_random_move(board, color)

            if move == None:
                return GoBoardUtil.opponent(color)
            board.play_move(move, color)
            
        if GoBoardUtil.generate_legal_moves(board, color) == []:
            return GoBoardUtil.opponent(color)
        else:
            return color
    
    

    def get_move(self, board:GoBoard, color:int):
        """
        Select a random move.
        """
        board = board.copy()
        moves = GoBoardUtil.generate_legal_moves(board, board.current_player)
        toplay = board.current_player
        assert color == toplay
        self.best_move = moves[0]
        move = runUcb(self, board, self.ucb_C, moves, toplay, weights_data)
        return move
        #move = GoBoardUtil.generate_random_move(board, color)
        #return move
        
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(NoGo(), board)
    con.start_connection()

if __name__ == "__main__":
    run()
