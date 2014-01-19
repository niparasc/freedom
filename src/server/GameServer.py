'''
Created on 24.2.2012

@author: f0392575
'''

import logging
from server.GameServerStates import WF_P1
from fgp.FGPServer import FGPServer
from interfaces.IFGPServInd import IFGPServInd

host = ""
port = 5555

# TODO: If GameServer dies kill all GameSessions.

# GameServer implements the interface IFGPServInd by extending it and overriding the method play().
# That is how interfaces are implemented in python.
class GameServer(IFGPServInd):
  def __init__(self):
    logging.debug("GameServer")
    self.state = WF_P1()
    self.fgpserver = FGPServer(self, host, port)
    while True:
      self.fgpserver.listen()
  
  def getState(self):
    return self.state
  
  def setState(self, state):
    logging.debug(self.state.name() + " --> " + state.name())
    self.state = state
  
  def getFGPServer(self):
    return self.fgpserver
  
  # Delegating incoming events to the states.
  
  # Interface IFGPServInd
  def play(self):
    self.state.play(self)

def main():
  logging.basicConfig(level=logging.DEBUG)
  GameServer()

if __name__ == '__main__':
  main()