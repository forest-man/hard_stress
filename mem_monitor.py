#!/usr/bin/env python


import os
import sys
import time
import resource

flag = []

#x=1
#while x < 10:
    #print x, end = '\r'
#    sys.stdout.write("\r%d" % x)
#    sys.stdout.flush()
#    x+=1
#    time.sleep(1)

def using(point=""):
    usage=resource.getrusage(resource.RUSAGE_SELF)
    return '''%s: usertime=%s systime=%s mem=%s mb
           '''%(point,usage[0],usage[1],
                (usage[2]*resource.getpagesize())/1000000.0 )


def mem_mon():
    while True:
        sys.stdout.write("\r", str(os.system('free -m')))
        sys.stdout.flush()
        time.sleep(1)


def mem_cons(_flag):
    x = 4
    print("Memory consumption is started...")
    a = []
    idx = 0
    appender = a.append
    MEGA_STR = 'F' * (10 ** 4 * x)
    try:
        while True:
            try:
                idx += 1
                if idx > 10000:
                    if 'kill' in _flag:
                        a = []
                        print("Memory was cleared")
                        break
                    idx = 0
                appender(MEGA_STR)
                using(mem_cons)
            except MemoryError:
                continue
    except KeyboardInterrupt:
        print("")
        print("Program has been stopped")
    except IOError:
        pass


#mem_cons(flag)
mem_mon()
