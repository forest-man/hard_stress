#!/usr/bin/env python

# Developed by MVelichko

import os
import sys
import time
import errno
import argparse
import subprocess
from multiprocessing import Pool
from multiprocessing import cpu_count
from argparse import RawTextHelpFormatter

def f(x):
    while True:
        x * x

# CPU consumption tool doesn't work properly yet (need to make multi/one CPU core consumption thingy with nice proc stop mechanism)
def cpu_eat_all():
    if __name__ == '__main__':
        processes = cpu_count()
        print('-' * 20)
        print('Running load on CPU')
        print('Utilizing %d cores' % processes)
        print('-' * 20)
        pool = Pool(processes)
        pool.map(f, range(processes))

def cpu_eat_one():
    if __name__ == '__main__':
        processes = cpu_count()
        print('-' * 20)
        print('Running load on CPU')
        print('Utilizing %d cores' % processes)
        print('-' * 20)
        pool = Pool(processes)
        pool.map(f, range(processes))


def mem_eat():
    print("Memory consumption is started...\nPlease use \'ctrl+c\' command to exit.")
    a = []
    while True:
        try:
            a.append(' ' * 100)
        except MemoryError:
            time.sleep(0.01)

# When consumption is started a file named 'eater' is created in current directory and started to growing. After catching 'KeyboardInterrupt' 'eater' will be deleted.
def dame():
    write_str = "Full_space"*2048*2048*50  # Consume amount

    try:
        print("Discspace consumption is started...\nPlease use \'ctrl+c\' command to exit.")
        with open('eater', "w") as f:
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
    except KeyboardInterrupt:
        os.remove('eater')

parser = argparse.ArgumentParser(
        description="Universal script for testing CPU, RAM and discspace consumption. \nPlease choose required optional argument.",
        epilog="",formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-c","--cpu", help="Consume all CPU. \nChoises are: \n    'a' - for all CPU cores consumption \n    'o' - for one CPU core consumption", choices=['a','o'])
parser.add_argument("-m","--memory", help="Consume all memory.", action="store_true")
parser.add_argument("-d","--disc", help="Consume all discspace by creating a file 'eater' in current directory. \nIt will be deleted automatically after the test.", action="store_true")
args = parser.parse_args()

if len(sys.argv) <= 1:
    sys.argv.append('--help')

if args.cpu == 'a':
    cpu_eat_all()
elif args.cpu == 'o':
    cpu_eat_one()
elif args.memory:
    mem_eat()
elif args.disc:
    dame()




