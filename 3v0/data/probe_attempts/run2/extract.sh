#!/usr/bin/env bash
awk -F, 'NR>1{if($2>max[$1])max[$1]=$2}END{for(n in max)print n","max[n]}' data.csv | sort
