#cet engine est très rudimentaire. Il est dôté d'une recherche negamax (sans optimisation) et il évalue que le matériel en rajoutant une notion de positionnement de ce dernier avec les tables de pièces. Il est capable de trouver des mates in 1 rapidement

import chess

board = chess.Board('r2qkb1r/pp2nppp/3p4/2pNN1B1/2BnP3/3P4/PPP2PPP/R2bK2R w KQkq - 1 1')

pawnValue = 100
knightValue = 320
bishopValue = 330
rookValue = 500
queenValue = 900
kingValue = 20000

pawnTable = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

knightTable = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

bishopTable = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

rookTable = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

queenTable = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

kingTable = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

def analyse(board):
    evaluation = 0
    score = 0

    values = {
        1:pawnValue,
        2:knightValue,
        3:bishopValue,
        4:rookValue,
        5:queenValue,
        6:kingValue
    }

    tables = {
        1:pawnTable,
        2:knightTable,
        3:bishopTable,
        4:rookTable,
        5:queenTable,
        6:kingTable
    }

    for i in chess.SQUARES:
        piece = board.piece_at(i)
        if piece != None:
            if piece.color == chess.WHITE:
                score = int(values.get(int(piece.piece_type), 0) + tables.get(int(piece.piece_type), 0)[i])
                evaluation += score
            if piece.color == chess.BLACK:
                evaluation -= int(values.get(int(piece.piece_type), 0) + tables.get(int(piece.piece_type), 0)[::-1][i]) #https://www.askpython.com/python/array/reverse-an-array-in-python

    if board.is_checkmate():
            if not(bool(chess.Color)):
                evaluation += 9999999
            if bool(chess.Color):
                evaluation -= 9999999

    return evaluation

def negamax(board, depth, color): #https://en.wikipedia.org/wiki/Negamax
    if depth == 0 or board.is_game_over():
        return color * analyse(board)
    
    best_value = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        value = -negamax(board, depth - 1, -color)
        board.pop()

        best_value = max(best_value, value)

    return best_value

def getBestMove(board, depth):
    best_move = None
    best_value = float('-inf')

    for move in board.legal_moves:
        if bool(board.turn):
            color = 1
        else:
            color = -1
        board.push(move)
        value = -negamax(board, depth - 1, -color)
        board.pop()

        if value >= best_value:
            best_value = value
            best_move = move

    return best_move 

#temps pour un éval: 0:00:00.000049 (https://stackoverflow.com/questions/7370801/how-do-i-measure-elapsed-time-in-python) si l'on prend environ 31 coups légaux par position, pour depth = 1, le programme prendrait ~25 minutes pour s'éxecuter (sur mon pc)