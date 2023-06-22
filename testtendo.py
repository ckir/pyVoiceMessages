#! /usr/bin/env python
import sys
import time
from tendo import singleton
try:
    me = singleton.SingleInstance()
except singleton.SingleInstanceException as e:
    sys.exit(-1)

while True:
    time.sleep(5)