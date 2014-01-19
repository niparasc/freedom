'''
Created on 22.2.2012

@author: f0392575
'''

from PyQt4 import QtGui
from PyQt4 import QtCore
import logging

class GameClientGUI(QtGui.QMainWindow):
  def __init__(self, gameclient):
    super(GameClientGUI, self).__init__()
    logging.debug("GameClientGUI")
    self.gameclient = gameclient
    self.threadpool = list() # Qt needs a reference to all the threads. Otherwise, CRASH! "QThread: Destroyed while thread is still running"
    self.connect(self.gameclient.getSignalEmitter(), QtCore.SIGNAL("statusBarSig(QString)"), self.updateStatusBar)
    self.connect(self.gameclient.getSignalEmitter(), QtCore.SIGNAL("whiteScoreSig(int)"), self.updateWhiteScore)
    self.connect(self.gameclient.getSignalEmitter(), QtCore.SIGNAL("blackScoreSig(int)"), self.updateBlackScore)
    self.connect(self.gameclient.getSignalEmitter(), QtCore.SIGNAL("lastMoveSig(QString)"), self.updateLastMove)
    self.connect(self.gameclient.getSignalEmitter(), QtCore.SIGNAL("moveMade(int, int, QString)"), self.moveMade)
    self.connect(self.gameclient.getSignalEmitter(), QtCore.SIGNAL("clearBoard(QString)"), self.clearBoard)
    self.boardbuttons = list()
    self.initUI()

  # What happens when we close the window.
  def closeEvent(self,event):
    self.gameclient.quit_freedom()    

  def initUI(self):
    # Everything's on a grid.
    self.grid = QtGui.QGridLayout()
    # Removing spaces between board's boxes.
    self.grid.setSpacing(0)

    # Board's boxes will be placed on the following positions.
    # These positions include x (letters) and y (numbers) axis.
    j = 0
    pos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
           (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
           (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
           (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
           (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10),
           (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10),
           (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10),
           (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10),
           (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10),
           (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10),
           (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10)]

    # These are the indexes of the first column. Here we will put the numbers 1-10.
    first_col = [0, 11, 22, 33, 44, 55, 66, 77, 88, 99]

    logging.debug("Adding 10x10 squares to the board.")
    # Adding the board boxes.
    gameBoardSquares = self.gameclient.getBoard().getSquares()
    k = 0
    for i in range(0, 110):
      if j not in first_col:
        button = boardButton(pos[j][0], pos[j][1], gameBoardSquares[k].getX(), gameBoardSquares[k].getY())
        k = k + 1
        self.boardbuttons.append(button)
        button.clicked.connect(self.boardButtonClicked)
        button.setMinimumWidth(50)
        button.setMinimumHeight(50)
        button.setStyleSheet("* { background-color: rgb(232,192,134) }")
        self.grid.addWidget(button, pos[j][0], pos[j][1])
      j = j + 1

    # Adding first column numbers.
    for i in range(0, 10):
      lbl = QtGui.QLabel(str(10 - i) + " ", self)
      lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
      self.grid.addWidget(lbl, pos[first_col[i]][0], pos[first_col[i]][1])

    # Adding last row letters.
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    last_row = [111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
    for i in range(0, 10):
      lbl = QtGui.QLabel(letters[i], self)
      lbl.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
      self.grid.addWidget(lbl, pos[last_row[i]][0], pos[last_row[i]][1])

    # Adding host, port, play.
    self.grid.setColumnMinimumWidth(11, 10)
    self.hostEdit = QtGui.QLineEdit('localhost')
    self.portEdit = QtGui.QLineEdit('5555')
    self.grid.addWidget(self.hostEdit, 0, 12, QtCore.Qt.AlignTop)
    self.grid.addWidget(self.portEdit, 1, 12, QtCore.Qt.AlignTop)
    self.play = QtGui.QPushButton("Play")
    self.play.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    self.play.clicked.connect(self.playButtonClicked)
    self.grid.addWidget(self.play, 2, 12, 1, 2)
    
    # Adding score, last move.
    self.wh_score_lbl = QtGui.QLabel("White: 0")
    self.bl_score_lbl = QtGui.QLabel("Black: 0")
    self.grid.addWidget(self.wh_score_lbl, 4, 12, 1, 2, QtCore.Qt.AlignLeft)
    self.grid.addWidget(self.bl_score_lbl, 4, 12, 1, 2, QtCore.Qt.AlignRight)
    self.last_move_lbl = QtGui.QLabel("Last move: None")
    self.grid.addWidget(self.last_move_lbl, 5, 12, 1, 2, QtCore.Qt.AlignCenter)    

    # Adding credits.
    self.powered_lbl = QtGui.QLabel("Powered by:")
    self.power_lbl = QtGui.QLabel("Python 2.7, PyQt4")
    self.grid.addWidget(self.powered_lbl, 8, 12, 1, 2, QtCore.Qt.AlignTop)
    self.grid.addWidget(self.power_lbl, 8, 12, 1, 2, QtCore.Qt.AlignVCenter)
    self.developed_by_lbl = QtGui.QLabel("Developed by:")
    self.grid.addWidget(self.developed_by_lbl, 9, 12, 1, 2, QtCore.Qt.AlignTop)
    self.devs_lbl = QtGui.QLabel("R.Laine, N.Paraschou")
    self.grid.addWidget(self.devs_lbl, 9, 12, 1, 2, QtCore.Qt.AlignVCenter)

    # Creating central widget with the grid and setting it to QMainWindow.
    cwidget = QtGui.QWidget()
    cwidget.setLayout(self.grid)
    self.setCentralWidget(cwidget)

    # Centering window on screen.
    self.center()

    self.statusBar().showMessage('Ready')
    self.setWindowTitle('Freedom Game')    
    self.show()

    # Disabling resizeability.
    self.setFixedSize(self.size());

  # playButton slot.
  def playButtonClicked(self):
    self.playbuttonworker = PlayButtonWorker(self.gameclient, self.hostEdit.text(), int(self.portEdit.text()))
    self.threadpool.append(self.playbuttonworker) # Qt needs a reference to all the threads. Otherwise, CRASH! "QThread: Destroyed while thread is still running"
    self.playbuttonworker.start()

  # boardButton slot.
  def boardButtonClicked(self):
    source = self.sender()
    self.boardbuttonworker = BoardButtonWorker(self.gameclient, source.getGameX(), source.getGameY())
    self.threadpool.append(self.boardbuttonworker) # Qt needs a reference to all the threads. Otherwise, CRASH! "QThread: Destroyed while thread is still running"
    logging.debug("test")
    self.boardbuttonworker.start()

  def updateStatusBar(self, text):
    self.statusBar().showMessage(text)

  def updateWhiteScore(self, ws):
    self.wh_score_lbl.setText("White: " + str(ws))
  
  def updateBlackScore(self, bs):
    self.bl_score_lbl.setText("Black: " + str(bs))

  def updateLastMove(self, text):
    if text != "None":
      t = str(text)
      coma = t.find(",")
      x = t[1:coma]
      y = t[coma+1:len(t)-1]
      if x == "1":
        lx = "A"
      elif x == "2":
        lx = "B"
      elif x == "3":
        lx = "C"
      elif x == "4":
        lx = "D"
      elif x == "5":
        lx = "E"
      elif x == "6":
        lx = "F"
      elif x == "7":
        lx = "G"
      elif x == "8":
        lx = "H"
      elif x == "9":
        lx = "I"
      elif x == "10":
        lx = "J"
      lastmove = "(" + lx + ", " + y + ")"
      self.last_move_lbl.setText("Last move: " + lastmove)
    else:
      self.last_move_lbl.setText("Last move: None")

  def moveMade(self, x, y, color):
    # x and y are game coordinates. Map them to grid coordinates to find which button to paint.
    for boardbutton in self.boardbuttons:
      if boardbutton.getGameX() == x and boardbutton.getGameY() == y:
        # Put (white or black) piece on the button instead of painting it.
        if color == "* { background-color: rgb(255,255,255) }":  # white
          self.grid.itemAtPosition(boardbutton.getGridX(), boardbutton.getGridY()).widget().setIcon(QtGui.QIcon("piece_white.png"))
          self.grid.itemAtPosition(boardbutton.getGridX(), boardbutton.getGridY()).widget().setIconSize(QtCore.QSize(30, 30));
        elif color == "* { background-color: rgb(0,0,0) }": # black
          self.grid.itemAtPosition(boardbutton.getGridX(), boardbutton.getGridY()).widget().setIcon(QtGui.QIcon("piece_black.png"))
          self.grid.itemAtPosition(boardbutton.getGridX(), boardbutton.getGridY()).widget().setIconSize(QtCore.QSize(30, 30));
        elif color == "* { background-color: rgb(232,192,134) }":  # board color
          self.grid.itemAtPosition(boardbutton.getGridX(), boardbutton.getGridY()).widget().setIcon(QtGui.QIcon()) # remove icon
        break

  def clearBoard(self, text):
    for button in self.boardbuttons:
      button.setIcon(QtGui.QIcon()) # remove icon

  # Centers window on screen.
  def center(self):
    qr = self.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

# boardButton is a QPushButton that knows its coordinates on the board.
class boardButton(QtGui.QPushButton):
  def __init__(self, gridx, gridy, gamex, gamey):
    super(boardButton, self).__init__()
    # Positions on the grid.
    self.gridx = gridx
    self.gridy = gridy
    # Positions on game board.
    self.gamex = gamex
    self.gamey = gamey

  def getGridX(self):
    return self.gridx
  
  def getGridY(self):
    return self.gridy
  
  def getGameX(self):
    return self.gamex
  
  def getGameY(self):
    return self.gamey

class PlayButtonWorker(QtCore.QThread):
  def __init__(self, gameclient, host, port):
    QtCore.QThread.__init__(self)
    logging.debug("PlayButtonWorker created.")
    self.gameclient = gameclient
    self.host = host
    self.port = port

  def run(self):
    logging.debug("PlayButtonWorker started.")
    self.gameclient.play(self.host, self.port)
    logging.debug("PlayButtonWorker died.")
    return

class BoardButtonWorker(QtCore.QThread):
  def __init__(self, gameclient, x, y):
    QtCore.QThread.__init__(self)
    logging.debug("BoardButtonWorker created.")
    self.gameclient = gameclient
    self.x = x
    self.y = y

  def run(self):
    logging.debug("BoardButtonWorker started.")
    self.gameclient.move(self.x, self.y)
    logging.debug("BoardButtonWorker died.")
    return
