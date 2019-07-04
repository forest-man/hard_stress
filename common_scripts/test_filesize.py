#!/usr/bin/env python

import os
#os.pwd
a = os.path.getsize('test_arg.py')
print(a >> 30)
print (5368709120 >> 30 )

def disc_cons():
    x = 4
    idx = 0
    write_str = "Full_space"*20*20*5  # Consume amount
    try:
        print("Discspace consumption is started...\nPlease use \'ctrl+c\' command to exit.")
        for i in range(1,5):
            with open('eater' + str(i), "w") as f:
                while True:
                    a = os.path.getsize('eater' + str(i))
                    print(a)
                    try:
                        idx += 1
                        if idx > 1:
                            #if a > 108000000000: for 100gb
                            if a > 1080000000:
                                print("Removing 'eater' file...")
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
