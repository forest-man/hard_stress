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
name = sys.argv[0]

class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

def timestamp():
    print(bcolors.OKGREEN+"["+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'+"]")+bcolors.ENDC),


def echo_server():
    HOST = "0.0.0.0"
    PORT = 12321
    try:
        class EchoServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
            pass
        class EchoRequestHandler(SocketServer.StreamRequestHandler):
            def handle(self):
                print("")
                timestamp()
                print "%s was remotely connected" % self.client_address[0]
                while True:
                    line = self.rfile.readline()
                    if not line:
                        break
                    flag[line.rstrip()] = 0
                print("")
                timestamp()    
                print "Remote client %s was disconnected" % self.client_address[0]
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
        print("")
        timestamp()
        #subprocess.call(["pkill", "-f", str(name)])
        print("Cpu consumption was remotely stopped.\nPlease use \'ctrl+c\' command to exit")
    except KeyboardInterrupt:
        pass


def mem_cons(x):
    timestamp()
    print("Memory consumption is started...\nPlease use \'ctrl+c\' command to exit.")
    a = []
    idx = 0
    appender = a.append
    MEGA_STR = 'F' * (10 ** 4 * x)
    try:
        while True:
            try:
                idx += 1
                if idx > 10000:
                    if 'kill' in flag:
                        print("")
                        timestamp()
                        print("Memory consumption was remotely stopped.\nPlease use \'ctrl+c\' command to exit")
                        a = []
                        timestamp()
                        print("Memory was cleared")
                        break
                        #subprocess.call(["pkill", "-f", str(name)]) to use termination coment break
                    idx = 0
                appender(MEGA_STR)
            except MemoryError:
                timestamp()
                print("Program is sleeping due to reaching memory limit")
                time.sleep(0.5)
                if 'kill' in flag:
                    print("")
                    timestamp()
                    print("Memory consumption was remotely stopped.\nPlease use \'ctrl+c\' command to exit")
                    a = []
                    timestamp()
                    print("Memory was cleared")
                    break
                    #subprocess.call(["pkill", "-f", str(name)]) to use termination coment break
                #timestamp()
                #print("Program has been stopped due to reaching memory limit")
                #a = []
                #break
    except KeyboardInterrupt:
        print("")
        timestamp()
        print("Program has been stopped")


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
        print("")
        timestamp()
        print("The script has been stopped")
    except OSError:
        print("")
        timestamp()
        print("The script has been stopped")


def multiproc(processes, key):
        try:
            timestamp()
            print('Running load on CPU\nUtilizing %d core out of %d' % (processes, cpu_count()))
            processes_pool = []
            for i in range(processes):
                processes_pool.append(Process(target=key, args=(processes,)))
                processes_pool[i].start()
            p = Process(target=echo_server)
            p.start()
            p.join()
            processes_pool[i].join()
        except KeyboardInterrupt:
            print("")
            timestamp()
            print("Program has been stopped")


parser = argparse.ArgumentParser(
        description="Universal script for testing CPU, RAM and discspace consumption. \nPlease choose required optional argument.",
        epilog="",formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-c","--cpu", help="Consume all CPU. \nChoises are: \n    'a' - for all CPU cores consumption \n    'o' - for one CPU core consumption", choices=['a','o'])
parser.add_argument("-m","--memory", help="Consume all memory. \nMemory consumption will be at max level until you stop it remotely. It will cause freezes.", action="store_true")
parser.add_argument("-d","--disc", help="Consume all discspace by creating a file 'eater' in current directory. \nIt will be deleted automatically after the test.", action="store_true")
args = parser.parse_args()


if args.cpu == 'a':
    multiproc(cpu_count(), cpu_cons) 
elif args.cpu == 'o':
    multiproc(1, cpu_cons)
elif args.memory:
    multiproc(1, mem_cons)
elif args.disc:
    disc_eat()

if len(sys.argv) == 1:
    parser.print_help()

