#!/bin/bash

while getopts ":hn:" opt; do
  case ${opt} in
    h )
      echo "Usage: setup_workers [OPTION] [ARGUMENT]"
      echo -e "\nOptions available:"
      echo "-n, the number of worker processes you want to start"
      ;;
    n )
      # check if argument is number
      re='^[0-9]+$'
      if ! [[ $OPTARG =~ $re ]] ; then
        echo "Error: number of workers should be a number" >&2; exit 1
      fi

      # check if n in range [1,8]
      if [[ $OPTARG -le 0 ]] || [[ $OPTARG -gt 8 ]] ; then
        echo "Number of worker processes should be in range [1,8]" 
      fi

      # Create n worker processes running on port numbers 17000,17001...
      port=17000
      endport=`expr $port+$OPTARG`
      i=0

      # The log file maintains a list of PIDs of all worker processes this script starts.
      # Just to make it easier to kill all of them automatically using the kill_current_workers script
      log_file="process_id.log"

      # Clears the file
      echo -n "" > $log_file 
      while [[ port -lt endport ]] ; do
        gunicorn --bind 0.0.0.0:$port worker:app &
        echo $! >> $log_file
        if  [$? -eq 1 ]; then
          echo "Something already running on port $port. Skipping.."; 
        else
          echo "Started process at port $port"
        fi
        port=`expr $port + 1`
      done
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
      ;;
  esac
done
shift $((OPTIND -1))
