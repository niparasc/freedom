'''
Created on 24.2.2012

@author: f0392575
'''

from abc import ABCMeta, abstractmethod
import logging
from server.GameSession import GameSession
from copy import deepcopy

class GameServerState(object):
  __metaclass__ = ABCMeta
  
  #def __init__(self):
    #logging.debug("Abstract Server State")
  
  @abstractmethod
  def name(self):
    pass
  
  @abstractmethod
  def play(self, ctx):
    pass

class WF_P1(GameServerState):
  def __init__(self):
    super(WF_P1, self).__init__()
    logging.debug("GameServerState: WF_P1")
  
  def name(self):
    return "WF_P1"
  
  def play(self, ctx):
    ctx.setState(WF_P2())

class WF_P2(GameServerState):
  def __init__(self):
    super(WF_P2, self).__init__()
    logging.debug("GameServerState: WF_P2")
  
  def name(self):
    return "WF_P2"
  
  def play(self, ctx):
    sendersqueuecopy = deepcopy(ctx.getFGPServer().getSendersQueue()) # copying the senders queue before passing it to the new session !
    GameSession(sendersqueuecopy).start()
    ctx.setState(WF_P1())
