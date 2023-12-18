from stockfish import Stockfish
import chess
import time
import random
DEBUG = True

## Right before a check after a promotion
FEN = 'r1q1kbQ1/p1ppp2p/bpn5/5p2/8/8/PPPPPPP1/RNBQKBNR w KQq - 1 7'
## set up for en passant
FEN = '1r2kb1r/pppqp1pp/2np1p1n/1P3P1P/6b1/8/P1PPPKP1/RNBQ1BNR w k - 3 8'
## set up for castle
FEN = 'rnbqkbnr/ppppppp1/7p/1B6/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4'

FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


cpu_sleep_time = 0.001


class ChessGame:

  # This is the constuctor 
  def __init__(self, stockfish_path = 'stockfish/stockfish-macos-x86-64'):
    self.stockfish = Stockfish(path=stockfish_path)
    self.chess_board = chess.Board()
    self.is_white_turn = True
    self.is_checkmate = False
    self.is_check = False
    self.turn = 0

    self.stockfish.set_elo_rating(250)


  def getBestMove(self, timelimit = 1):
    '''
    timelimit is in milliseconds
    '''
    return self.stockfish.get_best_move_time(timelimit)


  def getNthBestMove(self, nth_move):
    moves = self.stockfish.get_top_moves(nth_move)
    nth_move = min(nth_move, len(moves))
    return moves[nth_move - 1]['Move']


  def getRandomMove(self, nth_move = 1):
    moves = self.stockfish.get_top_moves(nth_move)
    nth_move = min(nth_move, len(moves))
    nth_move = random.randint(0, nth_move)
    return moves[nth_move - 1]['Move']


  def checkStatus(self):
    print('is_stalemate', self.chess_board.is_stalemate())
    print('is_insufficient_material', self.chess_board.is_insufficient_material())
    print('can_claim_threefold_repetition', self.chess_board.can_claim_threefold_repetition())
    print('halfmove_clock', self.chess_board.halfmove_clock)
    print('can_claim_fifty_moves', self.chess_board.can_claim_fifty_moves())
    print('can_claim_draw', self.chess_board.can_claim_draw())

    print('is_fivefold_repetition', self.chess_board.is_fivefold_repetition())
    print('is_seventyfive_moves', self.chess_board.is_seventyfive_moves())


    print('outcome', self.chess_board.outcome())



  def isMoveLegal(self, move):
    return self.stockfish.is_move_correct(move)
  

  def makeMove(self, move):
    self.chess_board.push_san(move)
    return self.stockfish.make_moves_from_current_position([move])


  def getBoard(self, isPLayerWhite = True):
    if isPLayerWhite:
      return self.stockfish.get_board_visual()
    else:
      return self.stockfish.get_board_visual(False)


  def getEval(self):
    return self.stockfish.get_evaluation()


  def isMate(self):
    valuation = self.stockfish.get_evaluation()
    #print(valuation)
    if valuation['type'] == 'mate' and valuation['value'] == 0:
      return True
    else:
      return False


  def setELORating(self, rating = 1000):
    self.stockfish.set_elo_rating(rating)



def getUserInput(chessgame):

  userInput = input('Enter your move:')
  while(not chessgame.isMoveLegal(userInput)):
    print(userInput, 'is not a legal move.')      
    userInput = input('Enter your move:')
  return userInput

def isGame(chessgame):
  outcome = game.chess_board.outcome()

  if outcome:
    print(outcome)
    winner = 'draw'
    if outcome.winner:
      winner = 'white'
    elif outcome.winner == False:
      winner = 'black'

    if winner == 'draw':
      print('The game is a draw by', outcome.termination)
    else:
      print('Checkmate.', winner, 'is the winner')

    return True
  return False

def engineSelfPlay(game, delayTime = 0.1):
  while(True):
    if(DEBUG):
      print('sFish:', game.stockfish.get_fen_position())
      # print('Chess:', game.chess_board.fen())
      # game.checkStatus()
      # input('')

    botsmove = game.getRandomMove(2)
    game.makeMove(botsmove)

    print('\nWhite\'s Move:', botsmove)
    print(game.getBoard())

    if isGame(game):
      break


    # if game.isMate():
    #   print('White wins')
    #   break


    time.sleep(delayTime)
    if(DEBUG):
      print('sFish:', game.stockfish.get_fen_position())
      # print('Chess:', game.chess_board.fen())
      # game.checkStatus()
      # input('')


    botsmove = game.getRandomMove(10)
    game.makeMove(botsmove)
    print("\nBlack's Move:", botsmove)
    print(game.getBoard())


    if isGame(game):
      break
    # if game.isMate():
    #   print('White wins')
    #   break

    time.sleep(delayTime)


def playerBlackGame(game):
  while(True):
    print(game.getBoard(False))
    if(DEBUG):
      print(game.stockfish.get_fen_position())
    # get player's move
    botsmove = game.getNthBestMove(10)
    game.makeMove(botsmove)
    print(game.getBoard(False))
    if game.isMate():
      print('White wins')
      break
    if game.isMate():
      print('Black wins')
      break
    

    # make bot's move
    #botsmove = game.getBestMove()
    usermove = getUserInput(game)
    game.makeMove(usermove)
    print(game.getBoard(False))
    if game.isMate():
      print('Black wins')
      break

def playerWhiteGame(game):
  while(True):
    if(DEBUG):
      print(game.stockfish.get_fen_position())
    # get player's move
    usermove = getUserInput(game)
    game.makeMove(usermove)
    print(game.getBoard())
    if game.isMate():
      print('White wins')
      break
    

    # make bot's move
    #botsmove = game.getBestMove()
    botsmove = game.getNthBestMove(10)
    game.makeMove(botsmove)
    print(game.getBoard())
    if game.isMate():
      print('Black wins')
      break
    


if __name__ == "__main__":
  game = ChessGame()

  if(DEBUG):
    game.stockfish.set_fen_position(FEN)
    game.chess_board = chess.Board(FEN)

  print('Welcome AI Chess Bot')

  isPlayerWhite = True
  isCPUvsCPU = False

  while(True):

    userinput = input("Do you want to play as white, black, or sit down and enjoy computer's performance?")
    userinput = userinput.lower()

    if userinput == "black" or userinput == "b":
      print("You are playing as black.")
      isPlayerWhite = False
      break
    elif userinput == "white" or userinput == "w":
      print("You are playing as white.")
      isPlayerWhite = True
      break
    elif userinput == "cpu" or userinput == "c" or userinput == "com"  or userinput == "computer"  or userinput == "ai":
      print('Enjoy the game!')
      isCPUvsCPU = True
      isPlayerWhite = False
      break
    else:
      print("choose again.")

  print(game.getBoard(isPlayerWhite))

  if isCPUvsCPU:
    engineSelfPlay(game, cpu_sleep_time)
  elif isPlayerWhite:
    playerWhiteGame(game)
  else:
    playerBlackGame(game)

  print('Thank you for playing')

'''



How chess is played:

1) white make move
2) Check for check
    if check:
    a) check for mate
      if mate
        game is over
    b) announce check
3) black make move
4) Check for check
    if check:
    a) check for mate
      if mate
        game is over
    b) announce check
5) goto to 1)



How our Ai/Bot will play (Assuming its Black):
1) wait for player to make move 
    - Use camera to see if a white piece has legally moved (CAMERA)
    - Get notation from move (PTYHON)
    - Update stockfish state (STOCKFISH)
2) check for game over
    - Ask stockfish is there's a mate (STOCKFISH)
3) Evaluate best move
    - Ask stockfish for next best move (give it a time limit) (STOCKFISH)
4) Move piece / Make move
    - Using the motors and camera move the correct piece to the correct spot (ROBOT)
    - If caputuring also remove caputred piece first (ROBOT)
    - Also consider promitions. Might be difficult!! (ROBOT)
5) do step 2) again 
6) Go to step 1) 
7) Tell User the game is over / who own somehow (MISC.)



https://en.wikipedia.org/wiki/Chess_notation
https://en.wikipedia.org/wiki/Algebraic_notation_(chess)

'''