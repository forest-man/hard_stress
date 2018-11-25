#!/usr/bin/env python

import time
from multiprocessing import Pool
from multiprocessing import cpu_count

def cpu_eat():

  def f(x):
      while True:
          x*x


  if __name__ == '__main__':
      processes = cpu_count()
      print '-' * 20
      print 'Running load on CPU'
      print 'Utilizing %d cores' % processes
      print '-' * 20
      pool = Pool(processes)
      pool.map(f, range(processes))


def mem_eat():
  a = []
  while True:
    try:
      a.append(' ' * 100)
    except MemoryError:
      time.sleep(0.01)

cpu_eat()