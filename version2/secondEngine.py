#cet engine est un peu plus abouti en rajoutant de l'optimisation à negamax ce qui réduit considérablement le temps pour trouver un coup et évalue aussi la mobilité d'une pièce, son developpement et force la dame a ne pas trop être déplacée. Il a de grosses lacunes en développement et en endgame. Il peut résoudre des mates in 2 rapidement

import chess

board = chess.Board()

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

pieceType = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]

baseSquaresWhite = {
    1: [8, 9, 10, 11, 12, 13, 14, 15],
    2: [1, 6],
    3: [2, 5],
    4: [56, 63],
    5: [3],
    6: [4]
}

baseSquaresBlack = {
    1: [48, 49, 50, 51, 52, 53, 54, 55],
    2: [57, 62],
    3: [58, 61],
    4: [0, 7],
    5: [59],
    6: [60]
}

def analyse(board):
    evaluation = 0
    score = 0
    pieces = []
    piecesWhite = []
    piecesBlack = []

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
            pieces.append((piece, i))
            if piece.color:
                piecesWhite.append((piece, i))
            else:
                piecesBlack.append((piece, i))

    for piece in pieces:
        if piece[0].color == chess.WHITE:
            score = int(values.get(int(piece[0].piece_type), 0) + tables.get(int(piece[0].piece_type), 0)[piece[1]])
            evaluation += score
        if piece[0].color == chess.BLACK:
            evaluation -= int(values.get(int(piece[0].piece_type), 0) + tables.get(int(piece[0].piece_type), 0)[::-1][piece[1]]) #https://www.askpython.com/python/array/reverse-an-array-in-python

    for piece in pieceType:
        boardMobilityWhite = board.pieces(piece, chess.WHITE)
        boardMobilityBlack = board.pieces(piece, chess.BLACK)

        legalMovesWhite = [move for move in board.legal_moves if move.from_square in boardMobilityWhite]
        legalMovesBlack = [move for move in board.legal_moves if move.from_square in boardMobilityBlack]

        if piece == pieceType[0]:
            evaluation += 10 * (len(legalMovesWhite) - len(legalMovesBlack)) * 0.3

        if piece == pieceType[1] or piece == pieceType[2]:
            evaluation += 10 * (len(legalMovesWhite) - len(legalMovesBlack)) * 0.5

        if piece == pieceType[3] or piece == pieceType[4]:
            evaluation += 10 * (len(legalMovesWhite) - len(legalMovesBlack)) * 0.1

    if board.is_checkmate():
            if bool(chess.Color):
                evaluation += 9999999
            if not(bool(chess.Color)):
                evaluation -= 9999999

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece != None:
            if piece.piece_type in [1,2,3,4]:
                if piece.color and square in baseSquaresWhite.get(int(piece.piece_type), 0):
                    evaluation -= 10
                if not(piece.color) and square in baseSquaresBlack.get(int(piece.piece_type), 0):
                    evaluation += 10
            elif piece.piece_type == 6:
                if piece.color and square in baseSquaresWhite.get(int(piece.piece_type), 0):
                    evaluation -= 5
                if not(piece.color) and square in baseSquaresBlack.get(int(piece.piece_type), 0):
                    evaluation += 5
            elif piece.piece_type == 5:
                if board.fullmove_number <= 15:
                    if piece.color and square in baseSquaresWhite.get(int(piece.piece_type), 0):
                        evaluation += 10
                    if not(piece.color) and square in baseSquaresBlack.get(int(piece.piece_type), 0):
                        evaluation -= 10
                else:
                    if piece.color and square in baseSquaresWhite.get(int(piece.piece_type), 0):
                        evaluation -= 10
                    if not(piece.color) and square in baseSquaresBlack.get(int(piece.piece_type), 0):
                        evaluation += 10 


    return evaluation

def negamax(board, depth, alpha, beta, color): #https://en.wikipedia.org/wiki/Negamax
    if depth == 0 or board.is_game_over():
        return color * analyse(board)
    
    best_value = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        value = -negamax(board, depth - 1, -beta, -alpha, -color)
        board.pop()

        best_value = max(best_value, value)
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return best_value

def getBestMove(board, depth):
    if bool(board.turn):
        color = 1
    else:
        color = -1
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        value = -negamax(board, depth - 1, -beta, -alpha, -color)
        board.pop()

        if value >= best_value:
            best_value = value
            best_move = move

        alpha = max(alpha, value) #gros bug qui ruine tout

    return best_move 