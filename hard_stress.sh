#!/bin/bash


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
  echo -e "\e[33m[$(get_timestamp)]: $1\e[39m"
}

if [ $# != 1 ]
  then echo_green "Please choose required testcase: \n1 - CPU eat\n2 - Memory eat\n3 - Discspace eat"
  read start	  
fi

function cpu_eat {
  echo_green "###CPU_EAT###\nPlease select test case:\n1-ONE core 100% CPU consumption\n2-ALL cores 100% CPU consumption(Handle with care)"
  read cpu
  if [[ "$cpu" == "1" ]]; then
    taskset -c 1 ./cpu_eat.py
  elif [[ "$cpu" == "2" ]]; then
    echo "ALL cores"
  fi
}



function mem_eat {
  ./mem_eat.py

}

#function dame {
#

#}


function main {
  if [[ "$1" == "1" ]]; then
    cpu_eat 
  elif [[ "$1" == "2" ]]; then
    mem_eat
  elif [[ "$1" == "3" ]]; then
    echo "number three"
  fi
}

main $start

