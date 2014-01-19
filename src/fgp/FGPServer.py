'''
Created on 21.2.2012

@author: f0392575
'''

import socket
import struct
from collections import deque
from fgp.PDUs import PlayPDU
from util.common import *
import logging

class FGPServer():
  def __init__(self, gameserver, host, port):
    logging.debug("FGPServer")
    self.gameserver = gameserver
    self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.local_socket.bind( (host, port) )
    self.sendersqueue = deque([], 2) # no need to empty it, rotates automatically

  def getSendersQueue(self):
    return self.sendersqueue
  
  '''
    baseDecode is used to read the type of the received message.
    It creates a new MessagePDU of that type and calls decode on
    that message passing in the buf (each PDU knows how to decode itself).
  '''
  def baseDecode(self,buf):
    logging.debug(buf_debug(buf))
    offset = 0
    self.msgtype = struct.unpack("H", buf[offset:offset + 2])[0]
    if self.msgtype == 1:
      logging.debug("FGPServer received PlayPDU")
      self.playpdu = PlayPDU()
      self.playpdu.decode(buf)
      self.gameserver.play()
    else:
      logging.debug("Dude, I did not expect that msg!")

  def listen(self):
    logging.debug("FGPServer listening...")
    buf, sender = self.local_socket.recvfrom(4096)
    self.sendersqueue.append(sender)
    logging.debug("Appending sender : " + str(sender))
    self.baseDecode(buf)
