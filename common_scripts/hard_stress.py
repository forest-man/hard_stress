#!/usr/bin/env python

# Developed by MVelichko

import re
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
    mem_st = int(os.popen("free -g | awk 'FNR == 2 {print $7}'").read())
    gb_count = 512
    timestamp()
    print("Memory consumption is started...")
    a=[]
    try:
        while True:
            try:
                if 'kill' in _flag:
                    break
                else:
                    GB = gb_count*gb_count*gb_count
                    b = "a" * (1 * GB)
                    time.sleep(0)
                    a.append(b)
            except (MemoryError, OSError):
                time.sleep(2)
                continue
    except (MemoryError, OSError):
        pass
        #time.sleep(0.1)
    except IOError:
        pass
    except KeyboardInterrupt:
        print("")
        timestamp()
        print("Program has been stopped")


# When consumption is started a file named 'eater' is created in current directory and started to growing. After catching 'KeyboardInterrupt' or remote 'kill' command 'eater' will be deleted.
def disc_cons(_flag):
    x = 4
    idx = 0
    write_str = "Full_space_with_me"*(2048+2048+2048)*480  # Consume amount
    try:
        timestamp()
        print("Discspace consumption is started...\nPlease use \'ctrl+c\' command to exit.")
        for i in xrange(sys.maxint):
            with open('eater' + str(i), "w") as f:
                while True:
                    a = os.path.getsize('eater' + str(i))
                    try:
                        idx += 1
                        if idx > 1:
                            if a > 1080000000: #aprx. 1,4 Gb
                                print('Chunck ' + str(i) + " is done" )
                                break
                            if 'kill' in _flag:
                                os.system('rm -rf eater*')
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
        timestamp()
        print("The script has been stopped. Deleting eater file(s)...")
        os.system('rm -rf eater*')
        print("")

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
