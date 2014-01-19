'''
Created on 21.2.2012

@author: f0392575
'''

'''
Created on 30.1.2012

@author: f0392575
'''

import unittest
import time
from fgp.FGPClient import *
from fgp.FGPServer import *
from fgp.PDUs import *
import logging
log = logging.getLogger(__name__)

class Test(unittest.TestCase):

  """  def testPlayPDU(self):
    fgp_client = FGPClient()
    fgp_server = FGPServer()
    fgp_server.start()
    
    fgp_client.setServHost("localhost")
    fgp_client.setServPort(5555)
    playpdu = PlayPDU()
    fgp_client.send(playpdu)
    ## checking
    time.sleep(0.5)
    log.debug(str(playpdu.getMsgtype()))
    log.debug(str(fgp_server.getPlayPDU().getMsgtype()))
    log.debug(str(playpdu.getMsgsize()))
    log.debug(str(fgp_server.getPlayPDU().getMsgsize()))
    assert playpdu.getMsgtype() == fgp_server.getPlayPDU().getMsgtype()
    assert playpdu.getMsgsize() == fgp_server.getPlayPDU().getMsgsize()
  """    
  """def testMovePDU(self):
    fgp_client = FGPClient()
    fgp_server = FGPServer()
    fgp_server.start()
    
    fgp_client.setServHost("localhost")
    fgp_client.setServPort(5555)
    movepdu = MovePDU()
    movepdu.setX(3)
    movepdu.setY(5)
    fgp_client.send(movepdu)
    ## checking
    time.sleep(0.5)
    log.debug(str(movepdu.getMsgtype()))
    log.debug(str(fgp_server.getMovePDU().getMsgtype()))
    log.debug(str(movepdu.getMsgsize()))
    log.debug(str(fgp_server.getMovePDU().getMsgsize()))
    log.debug(str(movepdu.getX()))
    log.debug(str(fgp_server.getMovePDU().getX()))
    log.debug(str(movepdu.getY()))
    log.debug(str(fgp_server.getMovePDU().getY()))
    assert movepdu.getMsgtype() == fgp_server.getMovePDU().getMsgtype()
    assert movepdu.getMsgsize() == fgp_server.getMovePDU().getMsgsize()
  """
  """def testUpdatePDU(self):
    fgp_client = FGPClient()
    fgp_server = FGPServer()
    fgp_server.start()
    
    fgp_client.setServHost("localhost")
    fgp_client.setServPort(5555)
    updatepdu = UpdatePDU()
    updatepdu.setX(-1)
    updatepdu.setY(-1)
    fgp_client.send(updatepdu)
    ## checking
    time.sleep(0.5)
    log.debug(str(updatepdu.getMsgtype()))
    log.debug(str(fgp_server.getUpdatePDU().getMsgtype()))
    log.debug(str(updatepdu.getMsgsize()))
    log.debug(str(fgp_server.getUpdatePDU().getMsgsize()))
    log.debug(str(updatepdu.getX()))
    log.debug(str(fgp_server.getUpdatePDU().getX()))
    log.debug(str(updatepdu.getY()))
    log.debug(str(fgp_server.getUpdatePDU().getY()))
    assert updatepdu.getMsgtype() == fgp_server.getUpdatePDU().getMsgtype()
    assert updatepdu.getMsgsize() == fgp_server.getUpdatePDU().getMsgsize()
  """
  
  def testUpdatePDU(self):
    updatepdu = UpdatePDU()
    updatepdu.setX(-1)
    updatepdu.setY(-1)
    updatepdu.setWhiteScore(24)
    updatepdu.setBlackScore(22)
    updatepdu.setSendersays("Hello World!")
    updatepdu2 = UpdatePDU()

    buf = updatepdu.encode()
    updatepdu2.decode(buf)

    ## checking
    log.debug(str(updatepdu.getMsgtype()))
    log.debug(str(updatepdu2.getMsgtype()))
    log.debug(str(updatepdu.getMsgsize()))
    log.debug(str(updatepdu2.getMsgsize()))
    log.debug(str(updatepdu.getX()))
    log.debug(str(updatepdu2.getX()))
    log.debug(str(updatepdu.getY()))
    log.debug(str(updatepdu2.getY()))
    log.debug(str(updatepdu.getWhiteScore()))
    log.debug(str(updatepdu2.getWhiteScore()))
    log.debug(str(updatepdu.getBlackScore()))
    log.debug(str(updatepdu2.getBlackScore()))
    log.debug(str(updatepdu.getSSLen()))
    log.debug(str(updatepdu2.getSSLen()))
    log.debug(str(updatepdu.getSendersays()))
    log.debug(str(updatepdu2.getSendersays()))
    assert updatepdu.getMsgtype() == updatepdu2.getMsgtype()
    assert updatepdu.getMsgsize() == updatepdu2.getMsgsize()


  def testGameOverPDU(self):
    gameoverpdu = GameOverPDU()
    gameoverpdu.setX(3)
    gameoverpdu.setY(3)
    gameoverpdu.setWhiteScore(22)
    gameoverpdu.setBlackScore(20)
    gameoverpdu.setSendersays("Game is over!")
    gameoverpdu2 = GameOverPDU()

    buf = gameoverpdu.encode()
    gameoverpdu2.decode(buf)

    ## checking
    log.debug(str(gameoverpdu.getMsgtype()))
    log.debug(str(gameoverpdu2.getMsgtype()))
    log.debug(str(gameoverpdu.getMsgsize()))
    log.debug(str(gameoverpdu2.getMsgsize()))
    log.debug(str(gameoverpdu.getX()))
    log.debug(str(gameoverpdu2.getX()))
    log.debug(str(gameoverpdu.getY()))
    log.debug(str(gameoverpdu2.getY()))
    log.debug(str(gameoverpdu.getWhiteScore()))
    log.debug(str(gameoverpdu2.getWhiteScore()))
    log.debug(str(gameoverpdu.getBlackScore()))
    log.debug(str(gameoverpdu2.getBlackScore()))
    log.debug(str(gameoverpdu.getSSLen()))
    log.debug(str(gameoverpdu2.getSSLen()))
    log.debug(str(gameoverpdu.getSendersays()))
    log.debug(str(gameoverpdu2.getSendersays()))
    assert gameoverpdu.getMsgtype() == gameoverpdu2.getMsgtype()
    assert gameoverpdu.getMsgsize() == gameoverpdu2.getMsgsize()
    
  """def testDropPDU(self):
    droppdu = DropPDU()
    droppdu.setSendersays("DROP!")
    droppdu2 = DropPDU()

    buf = droppdu.encode()
    droppdu2.decode(buf)

    ## checking
    log.debug(str(droppdu.getMsgtype()))
    log.debug(str(droppdu2.getMsgtype()))
    log.debug(str(droppdu.getMsgsize()))
    log.debug(str(droppdu2.getMsgsize()))
    log.debug(str(droppdu.getSSLen()))
    log.debug(str(droppdu2.getSSLen()))
    log.debug(str(droppdu.getSendersays()))
    log.debug(str(droppdu2.getSendersays()))
    assert droppdu.getMsgtype() == droppdu2.getMsgtype()
    assert droppdu.getMsgsize() == droppdu2.getMsgsize()
  """
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()