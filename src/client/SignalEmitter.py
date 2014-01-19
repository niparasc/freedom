'''
Created on 2.3.2012

@author: f0392575
'''

from PyQt4 import QtCore

class SignalEmitter(QtCore.QThread):
  def __init__(self):
    QtCore.QThread.__init__(self)
  
  def emitStatusBarText(self, text):
    self.emit(QtCore.SIGNAL("statusBarSig(QString)"), text)
  
  def emitWhiteScore(self, ws):
    self.emit(QtCore.SIGNAL("whiteScoreSig(int)"), ws)
    
  def emitBlackScore(self, bs):
    self.emit(QtCore.SIGNAL("blackScoreSig(int)"), bs)
  
  # TODO: Maybe this method can/should be replaced with emitMove? Or not?
  def emitLastMove(self, text):
    self.emit(QtCore.SIGNAL("lastMoveSig(QString)"), text)
  
  def emitMove(self, x, y, color):
    self.emit(QtCore.SIGNAL("moveMade(int, int, QString)"), x, y, color)
    
  def emitClearBoard(self):
    self.emit(QtCore.SIGNAL("clearBoard(QString)"), "")