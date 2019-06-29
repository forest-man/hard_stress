#!/usr/bin/env python

import os
#os.pwd
a = os.path.getsize('test_arg.py')
print(a >> 30)
print (5368709120 >> 30 )

def disc_cons(_flag):
    x = 4
    idx = 0
    write_str = "Full_space"*2048*2048*50  # Consume amount
    try:
        timestamp()
        print("Discspace consumption is started...\nPlease use \'ctrl+c\' command to exit.")
        with open('eater', "w") as f:
            while True:
                try:
                    idx += 1
                    if idx > 1:
                        if 'kill' in _flag:
                            timestamp()
                            print("Removing 'eater' file...")
                            os.remove('eater')
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
        timestamp()
        print("The script has been stopped")
