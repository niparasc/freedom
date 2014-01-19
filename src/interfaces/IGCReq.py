'''
Created on 24.2.2012

@author: f0392575
'''

class IGCReq(object):
  def play(self, host, port):
    raise NotImplementedError()
  
  def move(self, x, y):
    raise NotImplementedError()
  
  def quit_freedom(self):
    raise NotImplementedError()