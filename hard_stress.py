#!/usr/bin/env python

import sys
import time
import errno
import argparse
import subprocess
from multiprocessing import Pool
from multiprocessing import cpu_count


def f(x):
    while True:
        x * x


def cpu_eat():
    if __name__ == '__main__':
        processes = cpu_count()
        print('-' * 20)
        print('Running load on CPU')
        print('Utilizing %d cores' % processes)
        print('-' * 20)
        pool = Pool(processes)
        pool.map(f, range(processes))


def mem_eat():
    a = []
    while True:
        try:
            a.append(' ' * 100)
        except MemoryError:
            time.sleep(0.01)

# When consuming is started a file named 'd' is created in . directory and started to growing.
def dame():
    write_str = "Full_space"*2048*2048*50  # Consume amount

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


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


parser_dame = subparsers.add_parser('d', help='Consume Disc space')
parser_dame.set_defaults(func=dame)

if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()

# Run the appropriate function (in this case dame)
options.func()

