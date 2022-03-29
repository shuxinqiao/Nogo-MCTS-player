import numpy as np
from board_util import GoBoardUtil, EMPTY, BLACK, WHITE

#weights_data = np.loadtxt(".weights.txt")

def pattern_move(board, color, weights_data):
    weights = []
    legal_moves = GoBoardUtil.generate_legal_moves(board, color)
    if legal_moves == []:
        return None
    else:
        for move in legal_moves:
            weights.append(check_neighbor(board, move, weights_data))
        return select_best_move(legal_moves, weights)

def check_neighbor(board, point, weights_data):
    positions = [point + board.NS - 1,
                point + board.NS,
                point + board.NS + 1,
                point - 1,
                point,
                point + 1,
                point - board.NS - 1,
                point - board.NS,
                point - board.NS + 1,]
    
    counter = 0
    base_4 = 0
    for pos in positions:
        if pos == point:
            pass
        else:
            base_4 += board.board[pos] * (4 ** counter)
            #print(board.board[pos], counter)
            counter += 1

    return weights_data[base_4][1]

def select_best_move(moves, moveWins):
    max_child = np.argmax(moveWins)
    return moves[max_child]
