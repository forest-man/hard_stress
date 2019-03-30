#!/usr/bin/env python

# Developed by MVelichko

import os
import sys
import time
import errno
import socket
import datetime
import argparse
from multiprocessing import Manager, Pool, Process, cpu_count

name = sys.argv[0]

class bcolors:
    OKGREEN = '\033[92m'
    INFOYEL = '\033[93m'
    ENDC = '\033[0m'

def timestamp():
    print(bcolors.OKGREEN+"["+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'+"]")+bcolors.ENDC),

def echo_server(flag):
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
                if data.strip() == 'kill':
                    current_connection.shutdown(1)
                    current_connection.close()
                    flag['kill'] = 0
                    timestamp()
                    print("The script was remotely killed")
                    return 
                elif data:
                    current_connection.send(data)
                    print data
    except KeyboardInterrupt:
        pass

def cpu_cons(_flag):
    x=4
    try:
        while True:
            if 'kill' in _flag:
                break
            else:
                x ** x
                x = x + 99999
    except (KeyboardInterrupt, IOError):
        pass

def mem_cons(_flag):
    mem_st = int(os.popen("free -g | awk 'FNR == 2 {print $2}'").read())
    timestamp()
    print("Aggressive memory consumption is started...")
    print('Total memory size: ' + str(mem_st)+'GB')

    list=[]
    try:
        while mem_st > 2:
            if 'kill' in _flag:
                break
            else:
                GB = 1024*1024*1024
                b = "a" * (mem_st + GB)
                time.sleep(5)
                list.append(b)
                mem_st = mem_st/2
                print('Memory left: ' + str(mem_st)+'GB')
    except KeyboardInterrupt:
        print("")
        timestamp()
        print("Program has been stopped")
    timestamp()
    print("Delicate memory consumption is started...")
    x = 4
    a = []
    idx = 0
    appender = a.append
    MEGA_STR = 'F' * (10 ** 4 * x)
    try:
        while True:
            try:
                idx += 1
                if idx > 10000:
                    if 'kill' in _flag:
                        a = []
                        timestamp()
                        print("Memory was cleared")
                        break
                    idx = 0
                appender(MEGA_STR)
            except MemoryError:
                continue
                time.sleep(2)
    except KeyboardInterrupt:
        print("")
        timestamp()
        print("Program has been stopped")
    except IOError:
        pass

# When consumption is started a file named 'eater' is created in current directory and started to growing. After catching 'KeyboardInterrupt' or remote 'kill' command 'eater' will be deleted.
def disc_cons(_flag):
    x = 4
    idx = 0
    write_str = "Full_space"*2048*2048*50  # Consume amount
    try:
        timestamp()
        print("Discspace consumption is started...\nPlease use \'ctrl+c\' command to exit.")
        with open('eater', "w") as f:
            while True:
                try:
                    idx += 1
                    if idx > 1:
                        if 'kill' in _flag:
                            timestamp()
                            print("Removing 'eater' file...")
                            os.remove('eater')
                            break
                        idx = 0
                    f.write(write_str)
                    f.flush()
                except IOError as err:
                    if err.errno == errno.ENOSPC:
                        write_str_len = len(write_str)
                        if write_str_len > x:
                            write_str = write_str[:write_str_len/2]
                        else:
                            continue 
                    else:
                        break 
    except (KeyboardInterrupt, OSError):
        os.remove('eater')
        print("")
        timestamp()
        print("The script has been stopped")

def multiproc(processes, key):
    internal_flag = Manager().dict()
    if key == cpu_cons:
        timestamp()
        print('CPU consumption is started...')
        print(bcolors.INFOYEL + 'Utilizing %d core(s) out of %d'% (processes, cpu_count()) + bcolors.ENDC)
    try:
        processes_pool = []
        for i in range(processes):
            processes_pool.append(Process(target=key, args=(internal_flag,)))
            processes_pool[i].start()
        echo_server(internal_flag)
        for i in range(processes):
            processes_pool[i].join()
        timestamp()
        print "All child processes are stopped"
    except KeyboardInterrupt:
        print("")
        timestamp()
        print("Program has been stopped")

parser = argparse.ArgumentParser(
        description="""Universal script for testing CPU, RAM and discspace consumption. 
        \nPlease choose required mode:
        '-m cpu'  - consume 100% CPU of ALL cores
        '-m cpu1' - consume 100% CPU of ONE core
        '-m mem'  - consume all free RAM on the server
        '-m disc' - consume all free disc space on mount""",
            epilog="",formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-m","--mode", help="Select mode (cpu/cpu1/mem/disc)", type=str, default=None)
args = parser.parse_args()

if args.mode not in ['cpu', 'cpu1', 'mem', 'disc']:
    parser.print_help()
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
