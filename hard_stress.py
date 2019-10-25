#!/usr/bin/env python

# Developed by MVelichko

import re
import os
import sys
import time
import errno
import socket
import datetime
import optparse
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
            current_connection, _ = connection.accept()
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
                            if a > 107000000000: #aprx. 10 Gb
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

def main():
    options = optparse.OptionParser(usage='%prog [options]', description='Universal script for testing CPU, RAM and discspace consumption')
    options.add_option('-m', '--memory', action="store_true", default=False, help='consume all free RAM on the server')
    options.add_option('-d', '--disc', action="store_true", default=False, help='consume all free disc space on mount')
    options.add_option('-c', '--cpu', type='int', default=-1, help='consume 100% CPU for specified number of cores(please set it to 0, to consume all available cores)')

    opts, _ = options.parse_args()
    proc_cnt = 1
    if opts.cpu>=0:
        if opts.cpu == 0:
            proc_cnt = cpu_count()
        else:
            proc_cnt = opts.cpu
        target_func = cpu_cons
    elif opts.memory:
        target_func = mem_cons
    elif opts.disc:
        target_func = disc_cons
    else:
        print("Unsupported mode ...")
        sys.exit()
    multiproc(proc_cnt, target_func)

if __name__ == '__main__':
    sys.exit(main())
