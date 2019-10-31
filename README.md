# Hard Stress tool

### Description
Hard Stress tool (HS) is intended to perform High rate resource utilization (CPU, Memory, Disk) tests.

### Usage

```
Usage: hard_stress.py [options]

Universal script for testing CPU, RAM and discspace consumption

Options:
  -h, --help         show this help message and exit
  -m, --memory       consume all free RAM on the server
  -d, --disc         consume all free disc space on mount
  -c CPU, --cpu=CPU  consume 100% CPU for specified number of cores(please set
                     it to 0, to consume all available cores)
  -a, --all          ComboMode - run all modes simultaneously
```


### Monitoring
There is no monitoring interface yet in HS, but here are some ways to do it.  
For monitoring RAM consumption or CPU usage in separate terminal session it is handy to use **top** command with pressing **1** in its interface to show each core consumption:

    %Cpu0  :  3.4 us,  1.0 sy,  0.0 ni, 95.6 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
    %Cpu1  : 12.3 us,  0.7 sy,  0.0 ni, 87.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
    %Cpu2  :  2.4 us,  1.0 sy,  0.0 ni, 96.2 id,  0.0 wa,  0.0 hi,  0.3 si,  0.0 st
    %Cpu3  :  8.8 us,  0.7 sy,  0.0 ni, 90.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
    KiB Mem :  9038336 total,  7340472 free,  1112816 used,   585048 buff/cache
    KiB Swap:  1249236 total,   580324 free,   668912 used.  7638148 avail Mem

Disc space consumption can be monitored in real time in separate terminal session using **watch -d df** or **watch -d df -h** commands.

### Stop the HS
Anytime during HS running (if the machine is accessible) you can stop all consuming scripts and main HS using **ctrl+c** command.

### Remote termination handle
While running high rate resource utilization tests machine could be inaccessible.  
In this case HS tool has embedded remote termination handle for receiving termination command from remote host.  
To use remote termination handle you need to connect to server via telnet using its ip and default HS port (12321).  
For instance if server has ip address: 192.168.56.101 you can connect to it using next syntax from remote host:

    telnet 192.168.56.101 12321

After the connection was established proper info message will appear in HS interface: 

    [YYYY-MM-DD HH:MM:SS] Remote connection is established

Then you can send **kill** command from remote host to instantly stop all consuming scripts and main HS. 

### Troubleshooting tips
If you encounter with issue like: 

    ImportError: No module named site
    
You can perform **unset PYTHONHOME** command.

--------------------------------------------------------------------
Due to HS's beta status any feedback or notes will be welcomed. :+1:
