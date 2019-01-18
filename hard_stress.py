#!/usr/bin/env python


# Developed by MVelichko

import os
import sys
import time
import errno
import datetime
import argparse
import subprocess
import SocketServer
from argparse import RawTextHelpFormatter
from multiprocessing import Manager, Pool, Process, cpu_count

manager = Manager()
flag = manager.dict()

def timestamp():
    print("["+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'+"]"))



def echo_server():
    HOST = "0.0.0.0"
    PORT = 12321

    try:
        class EchoServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
            pass

        class EchoRequestHandler(SocketServer.StreamRequestHandler):
            def handle(self):
                timestamp()
                print "\n%s was remotely connected" % self.client_address[0]
                while True:
                    line = self.rfile.readline()
                    if not line:
                        break
                    flag[line.rstrip()] = 0
                timestamp()    
                print "\nRemote client %s was disconnected" % self.client_address[0]
    
        server = EchoServer((HOST, PORT), EchoRequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        pass # Just a stub for nicer output of KeyboardInterrupt exception


def cpu_cons(x):
    try:
        while True:
            if 'kill' in flag:
                break
            else:
                x ** x
                x = x + 99999
        timestamp()
        print(" \nCpu consumption was remotely stopped.\nPlease use \'ctrl+c\' command to exit")
    except KeyboardInterrupt:
        pass


# CPU consumption tool doesn't work properly yet (need to make multicore CPU consumption stopping handle)
def cpu_eat(processes):
    try:
        timestamp()
        print('Running load on CPU\nUtilizing %d core out of %d' % (processes, cpu_count()))
        processes_pool = []
        for i in range(processes):
            processes_pool.append(Process(target=cpu_cons, args=(processes,)))
            processes_pool[i].start()
        p = Process(target=echo_server)
        p.start()
        p.join()
        processes_pool[i].join()

    except KeyboardInterrupt:
        timestamp()
        print(" \nProgram has been stopped")


def mem_cons():
    timestamp()
    print("Memory consumption is started...\nPlease use \'ctrl+c\' command to exit.")
    a = []
    idx = 0
    appender = a.append
    MEGA_STR = 'F' * (10 ** 4)
    try:
        while True:
            try:
                idx += 1
                if idx > 10000:
                    if 'kill' in flag:
                        timestamp()
                        print(" \nMemory consumption was remotely stopped.\nPlease use \'ctrl+c\' command to exit")
                        a = []
                        break
                    idx = 0
                appender(MEGA_STR)
            except MemoryError:
                timestamp()
                print("Program has been stopped due to reaching memory limit")
                time.sleep(60) # Adjust the time during which memory consumption will be at 100% constantly
                break
    except KeyboardInterrupt:
        timestamp()
        print(" \nProgram has been stopped")

def mem_eat():
    try:
        p = Process(target=echo_server)
        m = Process(target=mem_cons)
        p.start()
        m.start()
        p.join()
        m.join()
    except KeyboardInterrupt:
        pass


# When consumption is started a file named 'eater' is created in current directory and started to growing. After catching 'KeyboardInterrupt' 'eater' will be deleted.
def disc_eat():
    write_str = "Full_space"*2048*2048*50  # Consume amount
    try:
        timestamp()
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
                        timestamp()
                        print("Discspace consumption has been stopped due to reaching disc space limit.\nRemoving 'eater' file...")
                    else:
                        raise
    except KeyboardInterrupt:
        os.remove('eater')
        timestamp()
        print(" \nThe script has been stopped")
    except OSError:
        timestamp()
        print(" \nThe script has been stopped")

parser = argparse.ArgumentParser(
        description="Universal script for testing CPU, RAM and discspace consumption. \nPlease choose required optional argument.",
        epilog="",formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-c","--cpu", help="Consume all CPU. \nChoises are: \n    'a' - for all CPU cores consumption \n    'o' - for one CPU core consumption", choices=['a','o'])
parser.add_argument("-m","--memory", help="Consume all memory. \nMemory consumption will be at max level during 60s by default. It will cause freezes.", action="store_true")
parser.add_argument("-d","--disc", help="Consume all discspace by creating a file 'eater' in current directory. \nIt will be deleted automatically after the test.", action="store_true")
args = parser.parse_args()


if args.cpu == 'a':
    cpu_eat(cpu_count()) 
elif args.cpu == 'o':
    cpu_eat(1)
elif args.memory:
    mem_eat()
elif args.disc:
    disc_eat()

if len(sys.argv) == 1:
    parser.print_help()

