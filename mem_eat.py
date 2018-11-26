#!/usr/bin/env python

import time
a = []
while True:
    try:
        a.append(' ' * 100)
    except MemoryError:
        time.sleep(0.01)
