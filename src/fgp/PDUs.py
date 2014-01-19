'''
Created on 21.2.2012

@author: f0392575
'''

from abc import ABCMeta, abstractmethod
import struct
from util.common import *
import logging

class MessagePDU(object):
  __metaclass__ = ABCMeta
  
  def __init__(self):
    self.msgtype = 0 # 0 is default value, means nothing.
    self.msgsize = 0
    
  def getMsgtype(self):
    return self.msgtype
    
  def getMsgsize(self):
    return self.msgsize
    
  @abstractmethod
  def encode(self):
    pass
    
  @abstractmethod
  def decode(self,buf):
    pass
    
class PlayPDU(MessagePDU):
  def __init__(self):
    super(PlayPDU,self).__init__()
    logging.debug("PlayPDU")
    self.msgtype = 1

  def name(self):
    return "PlayPDU"

  def encode(self):
    self.msgsize = struct.calcsize("HH")
    buf = str()
    buf += struct.pack("HH", self.msgtype, self.msgsize)
#    logging.debug(buf_debug(buf))
    return buf

  def decode(self,buf):
#    logging.debug(buf_debug(buf))
    offset = 0
    self.msgtype = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.msgsize = struct.unpack("H", buf[offset:offset + 2])[0]
    
class MovePDU(MessagePDU):
  def __init__(self):
    super(MovePDU,self).__init__()
    logging.debug("MovePDU")
    self.msgtype = 2
    self.x = 0
    self.y = 0

  def name(self):
    return "MovePDU"

  def getX(self):
    return self.x
  
  def getY(self):
    return self.y
  
  def setX(self, x):
    self.x = x
    
  def setY(self, y):
    self.y = y
  
  def encode(self):
    self.msgsize = struct.calcsize("HHHH")
    buf = str()
    buf += struct.pack("HHHH", self.msgtype, self.msgsize, self.x, self.y)
#    logging.debug(buf_debug(buf))
    return buf

  def decode(self,buf):
#    logging.debug(buf_debug(buf))
    offset = 0
    self.msgtype = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.msgsize = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.x = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.y = struct.unpack("H", buf[offset:offset + 2])[0]
    
class UpdatePDU(MessagePDU):
  def __init__(self):
    super(UpdatePDU,self).__init__()
    logging.debug("UpdatePDU")
    self.msgtype = 3
    self.x = 0
    self.y = 0
    self.whiteScore = 0
    self.blackScore = 0
    self.sslen = 0
    self.sendersays = ""

  def name(self):
    return "UpdatePDU"

  def getX(self):
    return self.x
  
  def getY(self):
    return self.y
  
  def getWhiteScore(self):
    return self.whiteScore
  
  def getBlackScore(self):
    return self.blackScore
  
  def getSSLen(self):
    return self.sslen
  
  def getSendersays(self):
    return self.sendersays
  
  def setX(self, x):
    self.x = x
    
  def setY(self, y):
    self.y = y
  
  def setWhiteScore(self, ws):
    self.whiteScore = ws
    
  def setBlackScore(self, bs):
    self.blackScore = bs
  
  def setSSLen(self, sslen):
    self.sslen = sslen
  
  def setSendersays(self, sendersays):
    self.sendersays = sendersays
  
  def encode(self):
    '''
      x and y are h (signed short) because they can also be negative (-1)
    '''
    self.sslen = len(self.sendersays) # sendersays length
    #logging.debug("sslen = " + str(self.sslen))
    fmt = "HHhhHHH" + str(self.sslen) + "s"
    self.msgsize = struct.calcsize(fmt)
    data = [self.msgtype, self.msgsize, self.x, self.y, self.whiteScore, self.blackScore, self.sslen, self.sendersays]
    buf = str()
    buf += struct.pack(fmt, *data)
    #logging.debug(buf_debug(buf))
    return buf

  def decode(self,buf):
    #logging.debug(buf_debug(buf))
    offset = 0
    self.msgtype = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.msgsize = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.x = struct.unpack("h", buf[offset:offset + 2])[0]
    offset += 2
    self.y = struct.unpack("h", buf[offset:offset + 2])[0]
    offset += 2
    self.whiteScore = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.blackScore = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.sslen = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.sendersays = struct.unpack(str(self.sslen) + "s", buf[offset:offset + self.sslen])[0]

class GameOverPDU(MessagePDU):
  def __init__(self):
    super(GameOverPDU,self).__init__()
    logging.debug("GameOverPDU")
    self.msgtype = 4
    self.x = 0
    self.y = 0
    self.whiteScore = 0
    self.blackScore = 0
    self.sslen = 0
    self.sendersays = ""

  def name(self):
    return "GameOverPDU"

  def getX(self):
    return self.x
  
  def getY(self):
    return self.y
  
  def getWhiteScore(self):
    return self.whiteScore
  
  def getBlackScore(self):
    return self.blackScore
  
  def getSSLen(self):
    return self.sslen
  
  def getSendersays(self):
    return self.sendersays
  
  def setX(self, x):
    self.x = x
    
  def setY(self, y):
    self.y = y
  
  def setWhiteScore(self, ws):
    self.whiteScore = ws
    
  def setBlackScore(self, bs):
    self.blackScore = bs
  
  def setSSLen(self, sslen):
    self.sslen = sslen
  
  def setSendersays(self, sendersays):
    self.sendersays = sendersays
  
  def encode(self):
    self.sslen = len(self.sendersays) # sendersays length
    #logging.debug("sslen = " + str(self.sslen))
    fmt = "HHHHHHH" + str(self.sslen) + "s"
    self.msgsize = struct.calcsize(fmt)
    data = [self.msgtype, self.msgsize, self.x, self.y, self.whiteScore, self.blackScore, self.sslen, self.sendersays]
    buf = str()
    buf += struct.pack(fmt, *data)
    #logging.debug(buf_debug(buf))
    return buf

  def decode(self,buf):
    #logging.debug(buf_debug(buf))
    offset = 0
    self.msgtype = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.msgsize = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.x = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.y = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.whiteScore = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.blackScore = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.sslen = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.sendersays = struct.unpack(str(self.sslen) + "s", buf[offset:offset + self.sslen])[0]

class DropPDU(MessagePDU):
  def __init__(self):
    super(DropPDU,self).__init__()
    logging.debug("DropPDU")
    self.msgtype = 5
    self.sslen = 0
    self.sendersays = ""

  def name(self):
    return "DropPDU"

  def getSSLen(self):
    return self.sslen
  
  def getSendersays(self):
    return self.sendersays
  
  def setSSLen(self, sslen):
    self.sslen = sslen
  
  def setSendersays(self, sendersays):
    self.sendersays = sendersays
  
  def encode(self):
    self.sslen = len(self.sendersays) # sendersays length
    #logging.debug("sslen = " + str(self.sslen))
    fmt = "HHH" + str(self.sslen) + "s"
    self.msgsize = struct.calcsize(fmt)
    data = [self.msgtype, self.msgsize, self.sslen, self.sendersays]
    buf = str()
    buf += struct.pack(fmt, *data)
    #logging.debug(buf_debug(buf))
    return buf

  def decode(self,buf):
    #logging.debug(buf_debug(buf))
    offset = 0
    self.msgtype = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.msgsize = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.sslen = struct.unpack("H", buf[offset:offset + 2])[0]
    offset += 2
    self.sendersays = struct.unpack(str(self.sslen) + "s", buf[offset:offset + self.sslen])[0]