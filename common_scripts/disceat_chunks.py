#!/usr/bin/env python
import os
import sys
#os.pwd
a = os.path.getsize('test_arg.py')
print(a >> 30)
print (5368709120 >> 30 )

def disc_cons():
    x = 4
    idx = 0
    write_str = "Full_space"*2048*2048*5  # Consume amount
    try:
        print("Discspace consumption is started...\nPlease use \'ctrl+c\' command to exit.")

        for i in xrange(sys.maxint):
            with open('eater' + str(i), "w") as f:
                while True:
                    a = os.path.getsize('eater' + str(i))
                    try:
                        idx += 1
                        if idx > 1:
                            #print (a)
                            #if a > 108000000000: for 100gb
                            if a > 1080000000: #aprx. 1,4 Gb
                                print('Chunck ' + str(i) + " is done" )
                                #os.remove('eater')
                                break
                            idx = 0
                        f.write(write_str)
                        f.flush()
                    except IOError as err:
                        if err.errno == errno.ENOSPC:
                            write_str_len = len(write_str)
                            if write_str_len > x:
                                write_str = write_str[:write_str_len/2]
                            else:
                                continue
                        else:
                            break
    except (KeyboardInterrupt, OSError):
        os.remove('eater')
        print("")
        print("The script has been stopped")

disc_cons()
