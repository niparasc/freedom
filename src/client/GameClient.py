'''
Created on 24.2.2012

@author: f0392575
'''

import sys
import logging
from PyQt4 import QtGui
from Game import Board
from GameClientGUI import GameClientGUI
from fgp.FGPClient import FGPClient
from GameClientStates import IDLE
from interfaces.IFGPCInd import IFGPCInd
from interfaces.IGCReq import IGCReq
from client.SignalEmitter import SignalEmitter

# GameClient implements the interfaces IFGPCInd and IGCReq by extending them and overriding their methods.
# That is how interfaces are implemented in python.
class GameClient(IFGPCInd, IGCReq):
  def __init__(self):
    logging.debug("GameClient")
    self.board = Board()
    self.signalemitter = SignalEmitter()
    self.gameclientgui = GameClientGUI(self)
    self.serverMsg = None
    self.state = IDLE()
    self.fgpclient = FGPClient(self)
  
  def getBoard(self):
    return self.board
  
  def getGameClientGui(self):
    return self.gameclientgui
  
  def getSignalEmitter(self):
    return self.signalemitter
  
  def getServerMsg(self):
    return self.serverMsg;
  
  def setServerMsg(self, serverMsg):
    self.setServerMsg(serverMsg)
  
  def getState(self):
    return self.state
  
  def setState(self, state):
    logging.debug(self.state.name() + " --> " + state.name())
    self.state = state

  # Delegating incoming events to the states.
  
  # Interface IGCReq
  def play(self, host, port):
    self.state.play(self, host, port)
  
  # Interface IGCReq
  def move(self, x, y):
    self.state.move(self, x, y)

  # Interface IGCReq
  def quit_freedom(self):
    self.state.quit_freedom(self)

  # Interface IFGPCInd
  def update(self, msg):
    self.serverMsg = msg
    self.state.update(self)
  
  # Interface IFGPCInd
  def gameover(self, msg):
    self.serverMsg = msg
    self.state.gameover(self)
  
  # Interface IFGPCInd
  def drop(self, msg):
    self.serverMsg = msg
    self.state.drop(self)

def main():
  logging.basicConfig(level=logging.DEBUG)
  app = QtGui.QApplication(sys.argv)
  GameClient()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()