#!/usr/bin/env python

# Developed by MVelichko

import os
import sys
import time
import errno
import socket
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
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind(('0.0.0.0', 12321))
        connection.listen(10)
        while True:
            current_connection, address = connection.accept()
            timestamp()
            print("Remote connection is established")
            while True:
                data = current_connection.recv(2048)

                if data == 'kill\r\n':
                    current_connection.shutdown(1)
                    current_connection.close()
                    flag[data] = 0
                    timestamp()
                    print("The script was remotely killed")
                    exit()

                elif data:
                    current_connection.send(data)
                    print data
    except KeyboardInterrupt:
        pass


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
        print("Cpu consumption was remotely stopped.\nPlease use \'ctrl+c\' command to exit")
    except KeyboardInterrupt:
        pass
    except IOError:
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
    except KeyboardInterrupt:
        print("")
        timestamp()
        print("Program has been stopped")
    except IOError:
        pass


# When consumption is started a file named 'eater' is created in current directory and started to growing. After catching 'KeyboardInterrupt' 'eater' will be deleted.
def disc_cons(x):
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
                        if write_str_len > x:
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
    if key == cpu_cons:
        timestamp()
        print('Running load on CPU\nUtilizing %d core out of %d' % (processes, cpu_count()))
    try:
        processes_pool = []
        for i in range(processes):
            processes_pool.append(Process(target=key, args=(processes,)))
            processes_pool[i].start()
        echo_server()
        for i in range(processes):
            processes_pool[i].join()
    except KeyboardInterrupt:
        print("")
        timestamp()
        print("Program has been stopped")


parser = argparse.ArgumentParser(
        description="Universal script for testing CPU, RAM and discspace consumption. \nPlease choose required optional argument.",
        epilog="",formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-m","--mode", help="Select mode (cpu/cpu1/mem/disc)", type=str, default=None)
args = parser.parse_args()

if args.mode not in ['cpu', 'cpu1', 'mem', 'disc']:
    print "Unsupported mode:", args.mode
    exit(1)

target_func = {
    'mem': mem_cons,
    'cpu': cpu_cons,
    'cpu1': cpu_cons,
    'disc': disc_cons
    }[args.mode]
proc_cnt = 1
if args.mode == 'cpu':
    proc_cnt = cpu_count()

multiproc(proc_cnt, target_func)

if len(sys.argv) == 1:
    parser.print_help()

