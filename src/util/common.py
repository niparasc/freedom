#!/usr/bin/env python
## -*- coding: utf-8 -*-
"""
Common utilities.
"""

##############################################################################
## Uses
import logging
log = logging.getLogger(__name__)

__all__ = list() # python module export list

#############################################################################
## utilities

def buftohex(buf):
  hexseq = str()
  i = 1
  for octet in buf:
    hexseq += "%02x" % ord(str(octet))
    if i % 4 == 0:
      hexseq += " "
    i += 1
  return hexseq
__all__.append("buftohex")

def buftohexstr(buf):
  r = buftohex(buf)
  r += " "
  for octet in buf:
    if ord(octet) >= 0x20 and ord(octet) < 0x7f: # ascii char
      r += octet
    else:
      r += "." 
  return r 
__all__.append("buftohexstr")

def buf_debug(buf):
  r = "DATA(%d) {" % len(buf)
  r += buftohexstr(buf)
  r += "}"
  return r
__all__.append("buf_debug")

#############################################################################
## Testing

import unittest

class Test_utilities(unittest.TestCase):

  def test_buftohex_01(self):
    assert buftohex("testing testing") == "74657374 696e6720 74657374 696e67"

  def test_buftohexstr_01(self):
    #print  buftohexstr("testing testing")
    assert buftohexstr("testing testing") == "74657374 696e6720 74657374 696e67 testing testing"

  def test_buf_debug(self):
    print buf_debug("testing testing")

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)  
  unittest.main()