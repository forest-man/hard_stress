#!/usr/bin/env python

import sys
import time
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


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


parser_cpu_eat = subparsers.add_parser('c', help='Consume CPU')
parser_cpu_eat.set_defaults(func=cpu_eat)

if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()

# Run the appropriate function (in this case showtop20 or listapps)
options.func()

