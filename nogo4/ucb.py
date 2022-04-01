from math import sqrt, log
import numpy as np

# Assignment 4 import
from pattern import check_neighbor


INFINITY = float("inf")


def mean(stats, i):
    return stats[i][0] / stats[i][1]

def rave(stats_rave, mu_ucb, beta, i):
    mu_rave = mean(stats_rave, i)
    return (1 - beta) * mu_ucb + beta * mu_rave

def ucb(board, stats, stats_rave, C, i, n, weights_data, moves):
    if stats[i][1] == 0:
        return INFINITY
    mu_ucb = mean(stats, i)
    beta = setBeta(stats, i, n)
    rave_val = rave(stats_rave, mu_ucb, beta, i)
    weight = check_neighbor(board, moves[i], weights_data)
    return rave_val + C * sqrt(log(n) / stats[i][1]) + weight

def setBeta(stats, i, n):
    k = 5 * n
    # lec
    return sqrt(k / (3 * n + k))
    # paper
    #beta = stats[i][0] 

def findBest(board, stats, stats_rave, C, n, weights_data, moves):
    best = -1
    bestScore = -INFINITY
    for i in range(len(stats)):
        score = ucb(board, stats, stats_rave, C, i, n, weights_data, moves)
        if score > bestScore:
            bestScore = score
            best = i
    assert best != -1
    return best

def bestMoveSet(player, move):
    player.best_move = move

def bestArm(stats):  # Most-pulled arm
    best = -1
    bestScore = -INFINITY
    for i in range(len(stats)):
        if stats[i][1] > bestScore:
            bestScore = stats[i][1]
            best = i
    assert best != -1
    return best

'''
# tuple = (move, percentage, wins, pulls)
def byPercentage(tuple):
    return tuple[1]
'''

# tuple = (move, percentage, wins, pulls)
def byPulls(tuple):
    return tuple[3]


def runUcb(player, board, C, moves, toplay, weights_data):
    stats = [[0, 0] for _ in moves]
    stats_rave = [[0, 0] for _ in moves]
    num_simulation = len(moves) * player.simulations_per_move
    for n in range(num_simulation):
        moveIndex = findBest(board, stats, stats_rave, C, n, weights_data, moves)
        bestMoveSet(player, moves[np.argmax(stats,axis=0)[0]])
        #bestMoveSet(player, moves[bestArm(stats)])
        result, cboard = player.simulate(board, moves[moveIndex], toplay)
        if result == toplay:
            stats[moveIndex][0] += 1  # win +1
            # rave
            if cboard.board[moves[moveIndex]] == toplay:
                stats_rave[moveIndex][0] += 1   # move appear and win
        stats[moveIndex][1] += 1  # game played +1

        # rave
        if cboard.board[moves[moveIndex]] == toplay:
            stats_rave[moveIndex][1] += 1   # move appear

    #bestIndex = bestArm(stats)
    #bestIndex = bestArm(stats)
    # move index with maximum count
    max_index = np.argmax(stats,axis=0)[0]
    # update best move
    best = moves[max_index]
    bestMoveSet(player, best)
    #writeMoves_ucb(board, moves, stats)
    return best