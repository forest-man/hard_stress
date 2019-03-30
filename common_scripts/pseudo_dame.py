#!/usr/bin/python

import sys
import errno

write_str = "!"*2048*2048*50  # Consume amount

output_path = sys.argv[1]

with open(output_path, "w") as f:
    while True:
        try:
            f.write(write_str)
            f.flush()
        except IOError as err:
            if err.errno == errno.ENOSPC:
                write_str_len = len(write_str)
                if write_str_len > 1:
                    write_str = write_str[:write_str_len/2]
                else:
                    break
            else:
                raise
