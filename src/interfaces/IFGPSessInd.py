'''
Created on 24.2.2012

@author: f0392575
'''

class IFGPSessInd(object):
  def move(self, msg):
    raise NotImplementedError()
  
  def drop(self, msg):
    raise NotImplementedError()