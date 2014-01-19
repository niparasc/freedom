'''
Created on 25.2.2012

@author: f0392575
'''

from abc import ABCMeta, abstractmethod
from fgp.PDUs import UpdatePDU, GameOverPDU, DropPDU
from client.Game import Piece
import logging

class GameSessionState(object):
  __metaclass__ = ABCMeta
  
  #def __init__(self):
    #logging.debug("Abstract Session State")
  
  @abstractmethod
  def name(self):
    pass
  
  @abstractmethod
  def move(self, ctx):
    pass
  
  @abstractmethod
  def drop(self, ctx):
    pass

class WF_P1_MOVE(GameSessionState):
  def __init__(self):
    super(WF_P1_MOVE, self).__init__()
    logging.debug("GameSessionState: WF_P1_MOVE")
  
  def name(self):
    return "WF_P1_MOVE"
  
  def move(self, ctx):
    if ctx.isMoveLegal(ctx.clientMsg.getX(), ctx.clientMsg.getY()):
      logging.debug("P1 legal move at " + str(ctx.clientMsg.getX()) + ", " + str(ctx.clientMsg.getY()))
      ctx.getBoard().addPiece(Piece("white"), ctx.clientMsg.getX(), ctx.clientMsg.getY())
      # Count score
      score = ctx.countScore()
      minus = score.find("-")
      ws = score[0:minus]
      bs = score[minus+1:]
      if ctx.getBoard().isBoardFull():
        gameoverpdu = GameOverPDU()
        gameoverpdu.setX(ctx.clientMsg.getX())
        gameoverpdu.setY(ctx.clientMsg.getY())
        gameoverpdu.setWhiteScore(int(ws))
        gameoverpdu.setBlackScore(int(bs))
        gameoverpdu.setSendersays("Game Over!")
        #gameoverpdu.setSendersays("Score: " + score + ", Game Over!")
        ctx.getFGPSession().send(gameoverpdu, 0) # Broadcast
        ctx.getFGPSession().send(gameoverpdu, 1)
        # Kill Session
        ctx.stopListening()
      else:
        updatepdu = UpdatePDU()
        updatepdu.setX(ctx.clientMsg.getX())
        updatepdu.setY(ctx.clientMsg.getY())
        updatepdu.setWhiteScore(int(ws))
        updatepdu.setBlackScore(int(bs))
        updatepdu.setSendersays("It is black's turn!")
        #updatepdu.setSendersays("Score: " + score + ", Opponent played at (" + str(ctx.clientMsg.getX()) + ", " + str(ctx.clientMsg.getY()) + ")." + " Make a move!")
        ctx.getFGPSession().send(updatepdu, 0)
        ctx.getFGPSession().send(updatepdu, 1)
        ctx.setState(WF_P2_MOVE())
    else:
      logging.debug("P1 illegal move")
      # Count score
      score = ctx.countScore()
      minus = score.find("-")
      ws = score[0:minus]
      bs = score[minus+1:]
      updatepdu = UpdatePDU()
      updatepdu.setX(-1)
      updatepdu.setY(-1)
      updatepdu.setWhiteScore(int(ws))
      updatepdu.setBlackScore(int(bs))
      updatepdu.setSendersays("Dude, that was illegal! Make a new move!")
      #updatepdu.setSendersays("Score: " + score + ", Dude, that was illegal! Make a new move!")
      ctx.getFGPSession().send(updatepdu, 0) # Send it to player who made the illegal move.
      ctx.setState(WF_P1_MOVE())
  
  def drop(self, ctx):
    sendersqueue = ctx.fgpsession.getSendersQueue()
    lastsender = ctx.fgpsession.getLastSender()
    
    if lastsender == sendersqueue[0]:           # who sent the drop? reply to the other one.
      droppdu = DropPDU()
      droppdu.setSendersays("Opponent quit!")
      ctx.fgpsession.send(droppdu, 1)
      ctx.stopListening()
    else:
      ctx.setState(DROP_PENDING())

class WF_P2_MOVE(GameSessionState):
  def __init__(self):
    super(WF_P2_MOVE, self).__init__()
    logging.debug("GameSessionState: WF_P2_MOVE")
  
  def name(self):
    return "WF_P2_MOVE"
  
  def move(self, ctx):
    if ctx.isMoveLegal(ctx.clientMsg.getX(), ctx.clientMsg.getY()):
      logging.debug("P2 legal move at " + str(ctx.clientMsg.getX()) + ", " + str(ctx.clientMsg.getY()))
      ctx.getBoard().addPiece(Piece("black"), ctx.clientMsg.getX(), ctx.clientMsg.getY())
      # Count score
      score = ctx.countScore()
      minus = score.find("-")
      ws = score[0:minus]
      bs = score[minus+1:]
      if ctx.getBoard().isBoardFull():
        gameoverpdu = GameOverPDU()
        gameoverpdu.setX(ctx.clientMsg.getX())
        gameoverpdu.setY(ctx.clientMsg.getY())
        gameoverpdu.setWhiteScore(int(ws))
        gameoverpdu.setBlackScore(int(bs))
        gameoverpdu.setSendersays("Game Over!")
        #gameoverpdu.setSendersays("Score: " + score + ", Game Over!")
        ctx.getFGPSession().send(gameoverpdu, 0) # Broadcast
        ctx.getFGPSession().send(gameoverpdu, 1)
        # Kill Session
        ctx.stopListening()
      else:
        updatepdu = UpdatePDU()
        updatepdu.setX(ctx.clientMsg.getX())
        updatepdu.setY(ctx.clientMsg.getY())
        updatepdu.setWhiteScore(int(ws))
        updatepdu.setBlackScore(int(bs))
        updatepdu.setSendersays("It is white's turn!")
        #updatepdu.setSendersays("Score: " + score + ", Opponent played at (" + str(ctx.clientMsg.getX()) + ", " + str(ctx.clientMsg.getY()) + ")." + " Make a move!")
        ctx.getFGPSession().send(updatepdu, 0)
        ctx.getFGPSession().send(updatepdu, 1)
        ctx.setState(WF_P1_MOVE())
    else:
      logging.debug("P2 illegal move")
      # Count score
      score = ctx.countScore()
      minus = score.find("-")
      ws = score[0:minus]
      bs = score[minus+1:]
      updatepdu = UpdatePDU()
      updatepdu.setX(-1)
      updatepdu.setY(-1)
      updatepdu.setWhiteScore(int(ws))
      updatepdu.setBlackScore(int(bs))
      updatepdu.setSendersays("Dude, that was illegal! Make a new move!")
      #updatepdu.setSendersays("Score: " + score + ", Dude, that was illegal! Make a new move!")
      ctx.getFGPSession().send(updatepdu, 1) # Send it to player who made the illegal move.
      ctx.setState(WF_P2_MOVE())
  
  def drop(self, ctx):
    sendersqueue = ctx.fgpsession.getSendersQueue()
    lastsender = ctx.fgpsession.getLastSender()
    
    if lastsender == sendersqueue[1]:           # who sent the drop? reply to the other one.
      droppdu = DropPDU()
      droppdu.setSendersays("Opponent quit!")
      ctx.fgpsession.send(droppdu, 0)
      ctx.stopListening()
    else:
      ctx.setState(DROP_PENDING())

class DROP_PENDING(GameSessionState):
  def __init__(self):
    super(DROP_PENDING, self).__init__()
    logging.debug("GameSessionState: DROP_PENDING")
  
  def name(self):
    return "DROP_PENDING"
  
  def move(self, ctx):
    sendersqueue = ctx.fgpsession.getSendersQueue()
    lastsender = ctx.fgpsession.getLastSender()
    droppdu = DropPDU()
    droppdu.setSendersays("Opponent quit!")
    if lastsender == sendersqueue[0]:
      ctx.fgpsession.send(droppdu, 0)
    else:
      ctx.fgpsession.send(droppdu, 1)
    ctx.stopListening()
  
  def drop(self, ctx):
    ctx.stopListening()
  
  