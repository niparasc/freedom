'''
Created on 25.2.2012

@author: f0392575
'''

import logging
from threading import Thread
from GameSessionStates import WF_P1_MOVE
from fgp.FGPSession import FGPSession
from interfaces.IFGPSessInd import IFGPSessInd
from fgp.PDUs import UpdatePDU
from client.Game import Board

# GameSession implements the interface IFGPSessInd by extending it and overriding the method move().
# That is how interfaces are implemented in python.
class GameSession(Thread, IFGPSessInd):
  def __init__(self, sendersqueue):
    super(GameSession, self).__init__()
    logging.debug("GameSession")
    # Some debugging
    p1 = sendersqueue[0]
    p2 = sendersqueue[1]
    logging.debug("Players in game: " + p1[0] + ":" + str(p1[1]) + ", " + p2[0] + ":" + str(p2[1]))
    # End of debugging
    self.board = Board()
    self.clientMsg = None
    self.state = None
    self.fgpsession = FGPSession(self, sendersqueue)
    self.listening = True

  def getBoard(self):
    return self.board

  def getState(self):
    return self.state
  
  def setState(self, state):
    if self.state != None:
      logging.debug(self.state.name() + " --> " + state.name())
    self.state = state
  
  def getFGPSession(self):
    return self.fgpsession
  
  def stopListening(self):
    self.listening = False
  
  def isMoveLegal(self, x, y):  
    if x in range(1, 11) and y in range (1, 11):              # move is on board
      logging.debug("on board")
      if self.getBoard().getOldSquare() != None:              # move is not the first in the game
        movesquare = self.board.getSquare(x, y)
        if movesquare.isOccupied() == False:                  # square is not occupied
          logging.debug("not occupied")
          opx = self.getBoard().getOldSquare().getX()   
          opy = self.getBoard().getOldSquare().getY()
          dx = x - opx
          dy = y - opy          
          if dx >= -1 and dx <= 1 and dy >= -1 and dy <= 1:   # move is adjacent to opponent's move
            logging.debug("adjacent to previous")
            return True
          else:                                               # is the player allowed for a free move
            logging.debug("Freedom Check against move: " + str(opx) + ", " + str(opy))
            for ix in range(-1, 2):
              for jy in range(-1, 2):
                logging.debug("ix: " + str(ix) + " jy: " + str(jy))
                if ix == 0 and jy == 0:                       # center - the piece we are checking
                  logging.debug("Center piece: ix: " + str(ix) + " jy: " + str(jy))
                  pass
                else:
                  logging.debug("Square to be checked: " + str(opx - ix) + ", " + str(opy - jy))
                  if opx - ix <= 10 and opx - ix >= 1 and opy - jy <= 10 and opy - jy >= 1: # on board
                    logging.debug(" -the square is on board")
                    if self.getBoard().getSquare(opx-ix, opy-jy).isOccupied() == False: # No piece
                      logging.debug("No piece at " + str(opx-ix) +"," + str(opy-jy))
                      return False                            # No freedom
            return True                                       # No moves - Freedom!
      else:                                                   # move is the first in the game and it is within the borders of the board
        logging.debug("first move")
        return True
      
    return False

  def countScore(self):
    scoreWhite = 0
    scoreBlack = 0
    #Directions used by the algorithm - NOTE: Only one direction per line has to be checked to cover all possibilities!
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)] # N, E, NE, NW
    
    for y in range(1, 11):                              # Go through the squares on the board from bottom left, line by line to top right
        for x in range(1, 11):
            startSquare = self.board.getSquare(x, y)    # Set a point of operation
            if startSquare.isOccupied():                # square is occupied - there is a piece to check
                for d in directions:                    # Go through squares in directions for lines of pieces up to 4 but no more
                    for length in range(1, 5):          # Length up to 4, if the line is longer than 4 you do not score :: length == 0 -> startSquare
                        dx = d[0] * length + x
                        dy = d[1] * length + y
                            
                        if(dx < 11 and dx > 0 and dy < 11 and dy > 0 ):  #if the square is on board 1 < x < 10 AND 1 < y < 10
                            lineSquare = self.board.getSquare(dx, dy)    #Set a point of reference
                            if (lineSquare.isOccupied() == False) or (lineSquare.getPiece().getColor() != startSquare.getPiece().getColor()):                   #color doesn't match - line does not continue
                                if length == 4:     #line changes color at the 5th piece
                                    #check one step to -1 direction
                                    dx = d[0] * (-1) + x
                                    dy = d[1] * (-1) + y
                                    if(dx < 11 and dx > 0 and dy < 11 and dy > 0 ):  #if the square is on board 1 < x < 10 AND 1 < y < 10
                                      backSquare = self.board.getSquare(dx, dy)    #Set a point of reference
                                      if (backSquare.isOccupied() == False) or (backSquare.getPiece().getColor() != startSquare.getPiece().getColor()):                   #color doesn't match - line does not continue
                                        #SCORE +1
                                        logging.debug("Score! Base: (" + str(x) + "," + str(y) + "), d: " + str(d) + ", color: " + startSquare.getPiece().getColor())
                                        if startSquare.getPiece().getColor() == "white":
                                          scoreWhite = scoreWhite + 1
                                        elif startSquare.getPiece().getColor() == "black":
                                          scoreBlack = scoreBlack + 1
                                        else:   #should not come here
                                          logging.debug("Unexpected color when scoring!")
                                        
                                      elif backSquare.getPiece().getColor() == startSquare.getPiece().getColor(): #the line continues -> no score
                                      #  logging.debug("-1: too long line")
                                        break
                                    else: #not on board -> SCORE!
                                      logging.debug("Score! Base: (" + str(x) + "," + str(y) + "), d: " + str(d) + ", color: " + startSquare.getPiece().getColor())
                                      if startSquare.getPiece().getColor() == "white":
                                        scoreWhite = scoreWhite + 1
                                      elif startSquare.getPiece().getColor() == "black":
                                        scoreBlack = scoreBlack + 1
                                      else:   #should not come here
                                        logging.debug("Unexpected color when scoring!")
                                        
                                        
                                else:           #line changes color before 4 in a row -> no score
                                    #logging.debug("Less than 4 in a row - no score")
                                    break       #Go to next direction
                            elif (lineSquare.getPiece().getColor() == startSquare.getPiece().getColor()): #the line continues
                                if length == 4: #line over 4 long - no score
                                    #logging.debug("Line over 4 long - no score")
                                    break
                            
                        
                        else:               #square is not on board...
                            #logging.debug("Square out of board and...")
                            if length == 4:  # BUT we have a line of 4 on the same color -> Score
                              #check one step to -1 direction
                              dx = d[0] * (-1) + x
                              dy = d[1] * (-1) + y
                              if(dx < 11 and dx > 0 and dy < 11 and dy > 0 ):  #if the square is on board 1 < x < 10 AND 1 < y < 10
                                backSquare = self.board.getSquare(dx, dy)    #Set a point of reference
                                if (backSquare.isOccupied() == False) or (backSquare.getPiece().getColor() != startSquare.getPiece().getColor()):                   #color doesn't match - line does not continue
                                  #SCORE +1
                                  logging.debug("Score! Base: (" + str(x) + "," + str(y) + "), d: " + str(d) + ", color: " + startSquare.getPiece().getColor())
                                  if startSquare.getPiece().getColor() == "white":
                                      scoreWhite = scoreWhite + 1
                                  elif startSquare.getPiece().getColor() == "black":
                                      scoreBlack = scoreBlack + 1
                                  else:   #should not come here
                                      logging.debug("Unexpected color when scoring!")
                                elif backSquare.getPiece().getColor() == startSquare.getPiece().getColor(): #the line continues -> no score
                                # logging.debug("-1: too long line")
                                  break
                              else: #square not on board -> SCORE +1
                                logging.debug("Score! Base: (" + str(x) + "," + str(y) + "), d: " + str(d) + ", color: " + startSquare.getPiece().getColor())
                                if startSquare.getPiece().getColor() == "white":
                                  scoreWhite = scoreWhite + 1
                                elif startSquare.getPiece().getColor() == "black":
                                  scoreBlack = scoreBlack + 1
                                else:   #should not come here
                                  logging.debug("Unexpected color when scoring!")
    
                            else:           #line less than 4 long and next square out of board -> no score
                                #logging.debug("OOB: Less than 4 in a row - no score")
                                break           #Go to next direction
                        
            else:
                logging.debug("No piece on square: " + str(x) + ", " + str(y))
                
    #return "White(" + str(scoreWhite*4) + "), " + "Black(" + str(scoreBlack*4) + ")"
    return str(scoreWhite*4) + "-" + str(scoreBlack*4)

  # Delegating incoming events to the states.
  
  # Interface IFGPSessInd
  def move(self, msg):
    self.clientMsg = msg
    self.state.move(self)
  
  # Interface IFGPSessInd  
  def drop(self, msg):
    self.clientMsg = msg
    self.state.drop(self)

  def run(self):
    # Create and send update(-1,-1) to first player to start game.
    updatepdu = UpdatePDU()
    updatepdu.setX(-1)
    updatepdu.setY(-1)
    updatepdu.setSendersays("Game started! Make first move!")
    self.fgpsession.send(updatepdu, 0) # first player's host and port are in position 0 of sendersqueue.
    self.setState(WF_P1_MOVE())
    while self.listening:
      self.fgpsession.listen()
