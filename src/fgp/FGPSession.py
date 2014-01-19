'''
Created on 25.2.2012

@author: f0392575
'''

import socket
import struct
from fgp.PDUs import MovePDU, DropPDU
from util.common import *
import logging

host = ""
port = 0

class FGPSession():
  def __init__(self, gamesession, sendersqueue):
    logging.debug("FGPSession")
    self.gamesession = gamesession
    self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.local_socket.bind( (host, port) )
    self.sendersqueue = sendersqueue
    self.lastsender = None

  def getSendersQueue(self):
    return self.sendersqueue
  
  def getLastSender(self):
    return self.lastsender

  '''
    baseDecode is used to read the type of the received message.
    It creates a new MessagePDU of that type and calls decode on
    that message passing in the buf (each PDU knows how to decode itself).
  '''
  def baseDecode(self,buf):
    logging.debug(buf_debug(buf))
    offset = 0
    self.msgtype = struct.unpack("H", buf[offset:offset + 2])[0]
    if self.msgtype == 2:
      logging.debug("FGPSession received MovePDU")
      self.movepdu = MovePDU()
      self.movepdu.decode(buf)
      self.gamesession.move(self.movepdu)
    elif self.msgtype == 5:
      logging.debug("FGPSession received DropPDU")
      self.droppdu = DropPDU()
      self.droppdu.decode(buf)
      self.gamesession.drop(self.droppdu)
    else:
      logging.debug("Dude, I did not expect that msg!")
      #self.queue.pop() # TODO: Needs testing.

  def send(self, msg, player):
    buf = msg.encode()
    destination = self.sendersqueue[player]
    host = destination[0]
    port = destination[1]
    logging.debug("FGPSession transmitting " + msg.name() + " to " + str(host) + ":" + str(port))
    self.local_socket.sendto(buf, (host, port))

  def listen(self):
    logging.debug("FGPSession listening...")
    buf, sender = self.local_socket.recvfrom(4096)
    self.lastsender = sender
    self.baseDecode(buf)
