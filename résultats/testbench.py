#https://pypi.org/project/stockfish/
#ce code est très peu structuré et était utile uniquement pour trouver les résultats. Normalement, vous n'avez pas besoin de le toucher. (Si vous le voulez il faudra donner un chemin d'accèes aux différents engines dans le repo en plus de spécifié le chemin d'accès à votre installation de stockfish)
#stockfish est trouvable ici: https://stockfishchess.org/

from thirdEngine.thirdEngine import getBestMove as getBestMoveThree
from secondEngine.secondEngine import getBestMove as getBestMoveTwo
from firstEngine.firstEngine import getBestMove as getBestMoveOne
from bruteForceEngine.botRandom import idiot as getBestMoveIdiot
from finalVer.finalVer import getBestMove as getBestMoveFinal
import chess
from stockfish import Stockfish
import matplotlib.pyplot as plt
import numpy as np
import time
import math
import chess.pgn

pathToStockfish=''

plt.style.use('_mpl-gallery')

baseBoardFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' 
board = chess.Board(baseBoardFen)

fish = Stockfish(pathToStockfish)

fish.set_skill_level(0)

def gameAgainstFish(StockfishColor, depthEngine, evalFunction, goal):
    timeList = []
    moveList = []
    board.reset_board()
    fish.set_fen_position(baseBoardFen)
    turn = True

    while not(board.is_game_over()):
        if turn != StockfishColor:
            start = time.time()
            move = evalFunction(board, depthEngine)
            end = time.time()
            timeList.append(float(format(end-start)))
            board.push(move)
        else:
            fish.set_fen_position(board.board_fen())
            move = fish.get_best_move()
            board.push_uci(move)
            move = chess.Move.from_uci(move)

        moveList.append(move.uci())

        turn = not(turn)


    if goal == "time":
        return timeList
    if goal == "win":
        return board.result()
    if goal == "moves":
        return moveList

"""def engineAgainstEngine(FirstEvalFunc, depthFirst, secondEvalFunc, depthSecond, firstEngineColor, goal):
    board.reset_board()
    turn = True

    while not(board.is_game_over()):
        if turn == firstEngineColor:
            move = FirstEvalFunc(board, depthFirst)
            board.push(move)
        else:
            move = secondEvalFunc(board, depthSecond)
            board.push(move)
        turn = not(turn)

    return board.result()"""

"""def testSinglePosition(evalFunction, depthEngine, board):
    move = evalFunction(board, depthEngine)
    return(move)

listEval = []
listTimes = []
baseStockfishEval = fish.get_evaluation()["value"]
for i in range(1, 5):
    fish.set_fen_position(baseBoardFen)
    start = time.time()
    move = testSinglePosition(getBestMoveOne, i, board)
    end = time.time()
    fish.make_moves_from_current_position([move.uci()])
    stockfishAfterMove = fish.get_evaluation()["value"]
    
    listEval.append(stockfishAfterMove - baseStockfishEval)
    listTimes.append(float(format(end-start)))"""

"""StockfishWin = 0
StockfishColor = True
for i in range(0, 16):
    result = gameAgainstFish("win")
    if StockfishColor and result == "1-0":
        StockfishWin += 1
    elif not(StockfishColor) and result == "0-1":
        StockfishWin += 1

    winrate = (15-StockfishWin)/15"""

"""x = np.arange(1, 6)
y = listEval
print(y)

y.append(0)

fig, ax = plt.subplots()

plt.title("EngineV1 problème ouverture différence d'évaluation entre la position initiale et finale")
plt.xlabel("profondeur")
plt.ylabel("deltaEval")

ax.bar(x, y, width=1, edgecolor="white", linewidth = 0.7)

ax.set(xlim = (1, 4), xticks = np.arange(1, 5),
    ylim = (math.floor(1.1*min(y)), math.ceil(1.1*max(y))), yticks = np.arange(math.floor(1.1*min(y)), math.ceil(1.1*max(y)), 100))

plt.show()"""

"""fish.set_fen_position(baseBoardFen)
baseStockfishEval = fish.get_evaluation()["value"]
start = time.time()
move = getBestMoveFinal(board, 4)
print(move)
end = time.time()
fish.make_moves_from_current_position([move.uci()])
stockfishAfterMove = fish.get_evaluation()["value"]

print(-baseStockfishEval + stockfishAfterMove)
print(float(format(end-start)))"""

"""for i in range(0, 4):
    fish.set_elo_rating(1300 + 0*i)

    win = 0
    for i in range(0, 4):
        x = (gameAgainstFish(False, "adaptative", getBestMoveFinal, "win"))
        if x == "1-0":
            win += 1
        print(win)

    elo = (1300+0*i)
    print('stockfish ' + elo + 'elo: ' + win/5)"""

fish.set_elo_rating(1400)
print(gameAgainstFish(False, "adaptative", getBestMoveFinal, "win"))