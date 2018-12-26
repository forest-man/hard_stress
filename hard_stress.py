#!/usr/bin/env python

# Developed by MVelichko

import os
import sys
import time
import errno
import argparse
import subprocess
import multiprocessing as mp
from multiprocessing import Pool
from multiprocessing import cpu_count
from argparse import RawTextHelpFormatter

MEGA = 10 ** 6
MEGA_STR = ' ' * MEGA

def f(x):
    try:
        while True:
            x ** x
            x = x + 99999
    except KeyboardInterrupt:
        print("")



# CPU consumption tool doesn't work properly yet (need to make multi/one CPU core consumption thingy with nice proc stop mechanism)

def cpu_eat(x):
    try:
        if x == 1:
            processes = 1
        elif x == 3:
            processes = cpu_count()

        print('Running load on CPU')
        print('Utilizing %d core out of %d' % (processes, cpu_count()))
        map_parameters = range(processes)
        pool = Pool(processes)
        pool.map(f, map_parameters)

    except KeyboardInterrupt:
        print("Programm has been stoped")


def mem_eat():
    print("Memory consumption is started...\nPlease use \'ctrl+c\' command to exit.")
    a = []
    while True:
        try:
            a.append(MEGA_STR)
        except MemoryError:
            time.sleep(60) # Adjust the time during which memory consumption will be at 100% constantly
            break
#            time.sleep(0.01)

# When consumption is started a file named 'eater' is created in current directory and started to growing. After catching 'KeyboardInterrupt' 'eater' will be deleted.
def disc_eat():
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
                        time.sleep(60)
                        os.remove('eater')
                    else:
                        raise
    except KeyboardInterrupt:
        os.remove('eater')
        print("The script has been stopped")
    except OSError:
        print("The script has been stopped")

parser = argparse.ArgumentParser(
        description="Universal script for testing CPU, RAM and discspace consumption. \nPlease choose required optional argument.",
        epilog="",formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-c","--cpu", help="Consume all CPU. \nChoises are: \n    'a' - for all CPU cores consumption \n    'o' - for one CPU core consumption", choices=['a','o'])
parser.add_argument("-m","--memory", help="Consume all memory. \nMemory consumption will be at max level during 60s by default. It will cause freezes.", action="store_true")
parser.add_argument("-d","--disc", help="Consume all discspace by creating a file 'eater' in current directory. \nIt will be deleted automatically after the test.", action="store_true")
args = parser.parse_args()

if len(sys.argv) < 1:
    sys.argv.append('--help')

if args.cpu == 'a':
    cpu_eat(3)
elif args.cpu == 'o':
    cpu_eat(1)
elif args.memory:
    mem_eat()
elif args.disc:
    disc_eat()




