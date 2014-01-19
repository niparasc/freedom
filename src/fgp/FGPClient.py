'''
Created on 21.2.2012

@author: f0392575
'''

import socket
import struct
from fgp.PDUs import PlayPDU, MovePDU, UpdatePDU, GameOverPDU, DropPDU
from util.common import *
import logging

host = ""
port = 0 # Let the OS decide.

class FGPClient(object):
  def __init__(self, gameclient):
    logging.debug("FGPClient")
    self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.local_socket.bind( (host, port) )
    self.gameclient = gameclient
  
  def setServHost(self,serv_host):
    self.serv_host = serv_host
  
  def setServPort(self,serv_port):
    self.serv_port = serv_port

  def baseDecode(self,buf):
    logging.debug(buf_debug(buf))
    offset = 0
    self.msgtype = struct.unpack("H", buf[offset:offset + 2])[0]
    if self.msgtype == 3:
      logging.debug("FGPClient received UpdatePDU")
      self.updatepdu = UpdatePDU()
      self.updatepdu.decode(buf)
      self.gameclient.update(self.updatepdu)
    elif self.msgtype == 4:
      logging.debug("FGPClient received GameOverPDU")
      self.gameoverpdu = GameOverPDU()
      self.gameoverpdu.decode(buf)
      self.gameclient.gameover(self.gameoverpdu)
    elif self.msgtype == 5:
      logging.debug("FGPClient received DropPDU")
      self.droppdu = DropPDU()
      self.droppdu.decode(buf)
      self.gameclient.drop(self.droppdu)
    else:
      logging.debug("Dude, I did not expect that!")

  def send(self,msg):
    buf = msg.encode()
    logging.debug("FGPClient transmitting " + msg.name())
    self.local_socket.sendto(buf, (self.serv_host, self.serv_port))

  def listen(self):
    logging.debug("FGPClient listening...")
    buf, sender = self.local_socket.recvfrom(4096)
    self.setServHost(sender[0])
    self.setServPort(sender[1])
    self.baseDecode(buf)