'''
Created on 24.2.2012

@author: f0392575
'''

from abc import ABCMeta, abstractmethod
import logging
from fgp.PDUs import PlayPDU, MovePDU, DropPDU
from Game import Piece

class GameClientState(object):
  __metaclass__ = ABCMeta
  
  #def __init__(self):
    #logging.debug("Abstract State")
  
  @abstractmethod
  def name(self):
    pass
  
  @abstractmethod
  def play(self, ctx, host, port):
    pass
  
  @abstractmethod
  def move(self, ctx, x, y):
    pass
  
  @abstractmethod
  def update(self, ctx):
    pass
  
  @abstractmethod
  def gameover(self, ctx):
    pass
  
  @abstractmethod
  def drop(self, ctx):
    pass
  
  @abstractmethod
  def quit_freedom(self, ctx):
    pass
  
class IDLE(GameClientState):
  def __init__(self):
    super(IDLE, self).__init__()
    logging.debug("GameClientState: IDLE")
  
  def name(self):
    return "IDLE"
  
  def play(self, ctx, host, port):
    # Clear the board if this is not the first game.
    if ctx.getBoard().getOldSquare() != None:
      ctx.getBoard().clearBoard()
      ctx.getSignalEmitter().emitClearBoard()
      ctx.getSignalEmitter().emitWhiteScore(0)
      ctx.getSignalEmitter().emitBlackScore(0)
      ctx.getSignalEmitter().emitLastMove("None")

    playpdu = PlayPDU()
    ctx.fgpclient.setServHost(host)
    ctx.fgpclient.setServPort(port)
    ctx.fgpclient.send(playpdu)
    ctx.setState(WF_OPPONENT())
    ctx.getSignalEmitter().emitStatusBarText("Waiting for opponent to join.")
    ctx.fgpclient.listen()
  
  # Do nothing.
  def move(self, ctx, x, y):
    pass
  
  # Do nothing.
  def update(self, ctx):
    pass
  
  def gameover(self, ctx):
    pass
  
  def drop(self, ctx):
    pass
  
  def quit_freedom(self, ctx):
    logging.debug("Exiting...")

class WF_OPPONENT(GameClientState):
  def __init__(self):
    super(WF_OPPONENT, self).__init__()
    logging.debug("GameClientState: WF_OPPONENT")
    
  def name(self):
    return "WF_OPPONENT"
    
  # Do nothing.
  def play(self, ctx, host, port):
    pass

  # Do nothing.
  def move(self, ctx, x, y):
    pass

  def update(self, ctx):
    x = ctx.getServerMsg().getX()
    y = ctx.getServerMsg().getY()
    ws = ctx.getServerMsg().getWhiteScore()
    bs = ctx.getServerMsg().getBlackScore()
    sendersays = ctx.getServerMsg().getSendersays()
    
    if x == -1 and y == -1: # First move of this client or illegal move of this client
      if ctx.getBoard().getOldSquare() == None: # First move
        ctx.getBoard().getPlayer().setPieceColor("* { background-color: rgb(255,255,255) }") # white
        ctx.getBoard().getOpponent().setPieceColor("* { background-color: rgb(0,0,0) }") # black
        ctx.setState(WF_USER())
        ctx.getSignalEmitter().emitStatusBarText(sendersays)
      else: # Illegal move
        ctx.setState(WF_USER())
        if ctx.getBoard().getOldSquare().getPiece() != None: # If there was a piece on the square
          ctx.getBoard().getSquare(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY()).setPiece(ctx.getBoard().getOldSquare().getPiece())
          ctx.getSignalEmitter().emitMove(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY(), ctx.getBoard().getOldSquare().getPiece().getColor())
        else:
          ctx.getBoard().getSquare(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY()).setPiece(ctx.getBoard().getOldSquare().getPiece())
          ctx.getSignalEmitter().emitMove(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY(), "* { background-color: rgb(232,192,134) }")
        ctx.getSignalEmitter().emitStatusBarText(sendersays)
    else: # Legal move of opponent
      if ctx.getBoard().getOldSquare() == None: # The client sets the colors of players' pieces
        ctx.getBoard().getPlayer().setPieceColor("* { background-color: rgb(0,0,0) }") # black
        ctx.getBoard().getOpponent().setPieceColor("* { background-color: rgb(255,255,255) }") # white
      piece = Piece(ctx.getBoard().getOpponent().getPieceColor())
      ctx.getBoard().addPiece(piece, x, y)
      ctx.setState(WF_USER())
      ctx.getSignalEmitter().emitMove(x, y, piece.getColor())
      ctx.getSignalEmitter().emitStatusBarText(sendersays)
      ctx.getSignalEmitter().emitWhiteScore(ws)
      ctx.getSignalEmitter().emitBlackScore(bs)
      ctx.getSignalEmitter().emitLastMove("(" + str(x) + ", " + str(y) + ")")

  def gameover(self, ctx):
    x = ctx.getServerMsg().getX()
    y = ctx.getServerMsg().getY()
    ws = ctx.getServerMsg().getWhiteScore()
    bs = ctx.getServerMsg().getBlackScore()
    sendersays = ctx.getServerMsg().getSendersays()
    if ctx.getBoard().isBoardFull() == False:
      piece = Piece(ctx.getBoard().getOpponent().getPieceColor())
      ctx.getBoard().addPiece(piece, x, y)
      ctx.getSignalEmitter().emitMove(x, y, piece.getColor())
    ctx.setState(IDLE())
    ctx.getSignalEmitter().emitStatusBarText(sendersays)
    ctx.getSignalEmitter().emitWhiteScore(ws)
    ctx.getSignalEmitter().emitBlackScore(bs)
    ctx.getSignalEmitter().emitLastMove("(" + str(x) + ", " + str(y) + ")")
  
  def drop(self, ctx):
    sendersays = ctx.getServerMsg().getSendersays()
    ctx.setState(IDLE())
    ctx.getSignalEmitter().emitStatusBarText(sendersays)
  
  def quit_freedom(self, ctx):
    droppdu = DropPDU()
    ctx.fgpclient.send(droppdu)
    logging.debug("Exiting...")

class WF_USER(GameClientState):
  def __init__(self):
    super(WF_USER, self).__init__()
    logging.debug("GameClientState: WF_USER")
  
  def name(self):
    return "WF_USER"
  
  # Do nothing.
  def play(self, ctx, host, port):
    pass

  def move(self, ctx, x, y):
    piece = Piece(ctx.getBoard().getPlayer().getPieceColor())
    ctx.getBoard().addPiece(piece, x, y)
    movepdu = MovePDU()
    movepdu.setX(x)
    movepdu.setY(y)
    ctx.fgpclient.send(movepdu)
    ctx.getSignalEmitter().emitMove(x, y, piece.getColor())
    ctx.getSignalEmitter().emitStatusBarText("Waiting for move confirmation.")
    ctx.setState(WF_MOVE_CONFIRM())
    ctx.fgpclient.listen()

  # Do nothing.
  def update(self, ctx):
    pass
  
  def gameover(self, ctx):
    pass
  
  def drop(self, ctx):
    pass
  
  def quit_freedom(self, ctx):
    droppdu = DropPDU()
    ctx.fgpclient.send(droppdu)
    logging.debug("Exiting...")

class WF_MOVE_CONFIRM(GameClientState):
  def __init__(self):
    super(WF_MOVE_CONFIRM, self).__init__()
    logging.debug("GameClientState: WF_MOVE_CONFIRM")
  
  def name(self):
    return "WF_MOVE_CONFIRM"
  
  def play(self, ctx, host, port):
    pass

  def move(self, ctx, x, y):
    pass
  
  def update(self, ctx):
    x = ctx.getServerMsg().getX()
    y = ctx.getServerMsg().getY()
    ws = ctx.getServerMsg().getWhiteScore()
    bs = ctx.getServerMsg().getBlackScore()
    sendersays = ctx.getServerMsg().getSendersays()
    
    if x == -1 and y == -1: # Illegal move of this client
      ctx.setState(WF_USER())
      if ctx.getBoard().getOldSquare().getPiece() != None: # If there was a piece on the square
        ctx.getBoard().getSquare(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY()).setPiece(ctx.getBoard().getOldSquare().getPiece())
        ctx.getSignalEmitter().emitMove(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY(), ctx.getBoard().getOldSquare().getPiece().getColor())
      else:
        ctx.getBoard().getSquare(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY()).setPiece(ctx.getBoard().getOldSquare().getPiece())
        ctx.getSignalEmitter().emitMove(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY(), "* { background-color: rgb(232,192,134) }")
      ctx.getSignalEmitter().emitStatusBarText(sendersays)
    else: # legal move
      ctx.getSignalEmitter().emitStatusBarText(sendersays)
      ctx.getSignalEmitter().emitWhiteScore(ws)
      ctx.getSignalEmitter().emitBlackScore(bs)
      ctx.getSignalEmitter().emitLastMove("(" + str(x) + ", " + str(y) + ")")
      ctx.setState(WF_OPPONENT())
      ctx.fgpclient.listen()
  
  def gameover(self, ctx):
    x = ctx.getServerMsg().getX()
    y = ctx.getServerMsg().getY()
    ws = ctx.getServerMsg().getWhiteScore()
    bs = ctx.getServerMsg().getBlackScore()
    sendersays = ctx.getServerMsg().getSendersays()
    ctx.setState(IDLE())
    ctx.getSignalEmitter().emitStatusBarText(sendersays)
    ctx.getSignalEmitter().emitWhiteScore(ws)
    ctx.getSignalEmitter().emitBlackScore(bs)
    ctx.getSignalEmitter().emitLastMove("(" + str(x) + ", " + str(y) + ")")
  
  def drop(self, ctx):
    # Undo the color of the square.
    if ctx.getBoard().getOldSquare().getPiece() != None: # If there was a piece on the square
      ctx.getBoard().getSquare(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY()).setPiece(ctx.getBoard().getOldSquare().getPiece())
      ctx.getSignalEmitter().emitMove(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY(), ctx.getBoard().getOldSquare().getPiece().getColor())
    else:
      ctx.getBoard().getSquare(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY()).setPiece(ctx.getBoard().getOldSquare().getPiece())
      ctx.getSignalEmitter().emitMove(ctx.getBoard().getOldSquare().getX(), ctx.getBoard().getOldSquare().getY(), "* { background-color: rgb(232,192,134) }")
    
    sendersays = ctx.getServerMsg().getSendersays()
    ctx.setState(IDLE())
    ctx.getSignalEmitter().emitStatusBarText(sendersays)
  
  def quit_freedom(self, ctx):
    pass
