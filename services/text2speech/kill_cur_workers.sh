#!/bin/bash

log_file="process_id.log"
cat $log_file | while read line 
do
#    echo "Slaughtering process $line"
   kill $line 
done