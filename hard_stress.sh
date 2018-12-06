#!/bin/bash

# Ultimate script for testing CPU, RAM and disc space consumption.


# Color echo functions
function echo_blue {
    echo -e "\e[34m $1\e[39m"
}

function echo_red {
  echo -e "\e[31m[$(get_timestamp)]: $1\e[39m"
}

function echo_green {
  echo -e "\e[32m $1\e[39m"
}

function echo_yellow {
  echo -e "\e[33m[$1\e[39m"
}





if [ $# != 1 ]
  then echo_green "Please choose required testcase: \n1 - CPU eat\n2 - Memory eat\n3 - Discspace eat"
  read start	  
fi


# For neat interrupting script execution
function control_c_dame {
    echo_yellow "\nThe test was stopped, all occupied discspace was cleared.\n"
    rm -rf eat/
    exit $?
}

function control_c_mem {
    echo_yellow "\nThe test was stopped, all occupied RAM was cleared.\n"
    exit $?
}


function cpu_eat {
  echo_green "### CPU eat ###\nPlease select test case:\n1-ONE core 100% CPU consumption (Cpu1)\n2-ALL cores 100% CPU consumption (Handle with care)"
  read cpu
  if [[ "$cpu" == "1" ]]; then
    `taskset -c 1 ./cpu_eat.py` > /dev>null & PREV_TOTAL=0
    PREV_IDLE=0

# Intended for nice percent consumption statistic
    while true; do
      # Get the total CPU statistics, discarding the 'cpu ' prefix.
      CPU=(`sed -n 's/^cpu1\s//p' /proc/stat`)
      IDLE=${CPU[3]} # Just the idle CPU time.

      # Calculate the total CPU time.
      TOTAL=0
      for VALUE in "${CPU[@]}"; do
        let "TOTAL=$TOTAL+$VALUE"
      done

      # Calculate the CPU usage since we last checked.
      let "DIFF_IDLE=$IDLE-$PREV_IDLE"
      let "DIFF_TOTAL=$TOTAL-$PREV_TOTAL"
      let "DIFF_USAGE=(1000*($DIFF_TOTAL-$DIFF_IDLE)/$DIFF_TOTAL+5)/10"
      echo -en "\rCpu1 percent of usage: $DIFF_USAGE%  \b\b"

      # Remember the total and idle CPU times for the next check.
      PREV_TOTAL="$TOTAL"
      PREV_IDLE="$IDLE"

      # Wait before checking again.
      sleep 1
    done

# Counting nums of CPUs to intend all - 1 CPUs capacity
  elif [[ "$cpu" == "2" ]]; then
    echo "ALL cores"
    nums=`grep -c cpu /proc/stat`
    cpus=`expr $nums - 2`
<<<<<<< HEAD
    n=`eval seq -s, 1 $cpus`
#    echo $n
#    count=`echo $(seq $cpus)`
    `taskset -c $n ./cpu_eat.py`  
=======
    echo $cpus 
#    count=`echo $(seq $cpus)`
    taskset -c "$cpus" ./cpu_eat.py
>>>>>>> master
  fi
}

# Eating memory sith stats
function mem_eat {
  echo_green "### Memory eat ###\nThe script will start to consume free RAM. \nPress Enter to commence the test...\nPress \"Ctrl+c\" to stop the test"
  read
  `./mem_eat.py` > /dev>null &  
  while trap control_c_mem SIGINT
    do
      free -m | awk 'NR==2{printf "Total: %s | Used: %s | Percent of usage: %.2f%%\t\t\r",$2, $3,  $3*100/$2 }'
      sleep 0.5
    done
}


# Dame execution with stats and removing 'eat' directory after execution
function dame {
  echo_green "### Discspace eat ###\nThe script will create directory named \"eat\" and start to consume discspace in intensive way by store in this directory files with constant growing size.\nPress Enter to commence the test...\nPress \"Ctrl+c\" to stop the test"
  read
  mkdir ./eat
  `./dame ed eat/` > /dev>null &
   while trap control_c_dame SIGINT 
    do
      df  | awk '$NF=="/"{printf "Filesystem: %s | Used: %s | Available: %s | Disc Usage: %s\r",$1,$3,$4,$5}'&
      sleep 0.5
    done
}

function main {
  if [[ "$1" == "1" ]]; then
    cpu_eat 
  elif [[ "$1" == "2" ]]; then
    mem_eat
  elif [[ "$1" == "3" ]]; then
    dame
    rm -rf eat/
  fi
}

main $start

