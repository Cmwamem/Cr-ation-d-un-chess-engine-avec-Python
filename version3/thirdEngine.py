#https://chess.stackexchange.com/questions/35448/looking-for-polyglot-opening-books a été utilisé pour trouver le livre d'ouverture et https://chess.massimilianogoi.com/download/tablebases/ pour l'endgame
#les lacunes du 2ème engine sont renforcées par la recherche dans des tables pour l'ouverture et l'endgame.


import chess
import chess.polyglot
import chess.syzygy

pathToOpeningBook = ''
pathToEndgameTable = ''

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

def defineGameState(board):
    pieces = []

    with chess.polyglot.open_reader(pathToOpeningBook) as reader:
        isOpening = len(list(reader.find_all(board)))

    for i in chess.SQUARES:
        piece = board.piece_at(i)
        if piece != None:
            pieces.append(piece)

    if isOpening > 0:
        return "opening"
    elif len(pieces) <= 5: #la raison de 5 est que, en bref, pour 6 pièces, il faudrait une table d'endgame de 150GB et 16,7TB pour 7 pièces (je n'ai pas la place pour ça)
        return "endgame"
    else:
        return "midgame"
    

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
            evaluation += 10 * (len(legalMovesWhite) - len(legalMovesBlack)) * 0.3

        if piece == pieceType[3] or piece == pieceType[4]:
            evaluation += 10 * (len(legalMovesWhite) - len(legalMovesBlack)) * 0.1

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            evaluation -= 9999999
        else:
            evaluation += 9999999

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

    for square in chess.SQUARES:
        pieceOnSquare = board.piece_at(square)
        if pieceOnSquare != None:
            if pieceOnSquare in piecesWhite and board.pin(chess.BLACK, square):
                evaluation += 100
            elif pieceOnSquare in piecesBlack and board.pin(chess.WHITE, square):
                evaluation -= 100

    return evaluation

def negamax(board, depth, alpha, beta, color): #https://en.wikipedia.org/wiki/Negamax
    if depth == 0 or board.is_game_over() or defineGameState(board) != "midgame":
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

    gameState = defineGameState(board)

    if gameState == "midgame":
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
    
    elif gameState == "opening":
        with chess.polyglot.open_reader(pathToOpeningBook) as reader:
            best_move = reader.find(board).move

    elif gameState == "endgame":
        best_move = None
        best_dtz = None

        with chess.syzygy.open_tablebase(pathToEndgameTable) as tablebase:
            if board.turn == chess.WHITE:
                color = 1
            else:
                color = -1

            for move in board.legal_moves:
                board.push(move)
                try:
                    dtz = tablebase.probe_dtz(board)
                    if best_dtz is None or color*dtz > color*best_dtz:
                        best_dtz = dtz
                        best_move = move
                except chess.syzygy.MissingTableError:
                    pass
                board.pop()

    return best_move 

"""while board.is_game_over:
    x = ""
    print(board)
    if not(bool(board.turn)):
        coups = []
        for move in board.legal_moves:
            coups.append(move.uci())
        while x not in coups:
            x = input("quel coup?")
            if x == "help":
                print("les coups possibles sont", coups)
            elif x in coups:
                board.push(chess.Move.from_uci(x))  
            else:
                print("coup illégal") 
    else:
        move = getBestMove(board, 3)
        print(move)
        board.push(move)"""