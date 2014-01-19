'''
Created on 26.2.2012

@author: f0392575
'''

import logging
from copy import deepcopy

class Player(object):
  def __init__(self):
    self.pieceColor = None
  
  def getPieceColor(self):
    return self.pieceColor
  
  def setPieceColor(self, piececolor):
    self.pieceColor = piececolor

class Board(object):
  def __init__(self):
    logging.debug("Board")
    self.player = Player()
    self.opponent = Player()
    self.squares = list()
    self.createSquares()
    self.oldSquare = None
  
  def getPlayer(self):
    return self.player
  
  def getOpponent(self):
    return self.opponent
  
  def getSquares(self):
    return self.squares
  
  def getOldSquare(self):
    return self.oldSquare
  
  def createSquares(self):
    gamex = 1
    gamey = 10
    for i in range(0, 100):
      self.squares.append(Square(gamex, gamey))
      # Calculate game coordinates.
      if gamex < 10:
        gamex = gamex + 1
      elif gamex == 10:
        gamex = 1
        gamey = gamey -1

  def clearBoard(self):
    self.squares = list()
    self.createSquares()
    self.oldSquare = None

  def getSquare(self, x, y):
    for square in self.squares:
      if square.getX() == x and square.getY() == y:
        return square

  def addPiece(self, piece, x, y):
    square = self.getSquare(x, y)                           # on this square new move is happening
    self.oldSquare = deepcopy(square)
    logging.debug("oldSquare piece before = " + str(self.oldSquare.getPiece()))
    # copy.deepcopy() can do the following
#    self.oldSquare = Square(square.getX(), square.getY())   # creating new square to hold the old square's values (in case of undo)  
#    if square.getPiece() != None:                           # it might be the first move
#      self.oldpiece = Piece(square.getPiece().getColor())
#      self.oldSquare.setPiece(self.oldpiece)
    
    square.setPiece(piece)                                  # now that the old square is copied, update square by putting the piece on it
    logging.debug("oldSquare piece after = " + str(self.oldSquare.getPiece()))
  
  def isBoardFull(self):
    retvalue = True
    for square in self.squares:
      if square.isOccupied() == False:
        retvalue = False
        break
    return retvalue

class Square(object):
  def __init__(self, x, y):
    #logging.debug("Square: " + str(x) + ", " + str(y))
    self.x = x
    self.y = y
    self.piece = None
  
  def getX(self):
    return self.x
  
  def getY(self):
    return self.y
  
  def getPiece(self):
    return self.piece
  
  def setPiece(self, piece):
    self.piece = piece
  
  def isOccupied(self):
    if self.piece == None:
      return False
    else:
      return True

class Piece(object):
  def __init__(self, color):
    logging.debug("Piece")
    self.color = color
  
  def getColor(self):
    return self.color
