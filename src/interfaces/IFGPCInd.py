'''
Created on 24.2.2012

@author: f0392575
'''

class IFGPCInd(object):
  def update(self, msg):
    raise NotImplementedError()
  
  def gameover(self, msg):
    raise NotImplementedError()
  
  def drop(self, msg):
    raise NotImplementedError()