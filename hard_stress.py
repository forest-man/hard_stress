#!/usr/bin/env python

import time
import argparse
import subprocess
from multiprocessing import Pool
from multiprocessing import cpu_count


def help():
    print("Please choose desired test")
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


try:
    x = input("Choose desired test:\n 1 - CPU eat \n 2 - Memory eat \n 3 - Discspace consumption\n")
except SyntaxError:
    x = None


if x == 1:
    print("CPU_eat")

elif x == 2:
    print("mem_eat")
elif x == 3:
    print("disk_eat")
elif x is None:
    help()
    #cpu_eat()

