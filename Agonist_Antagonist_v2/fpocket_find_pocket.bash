#!/bin/bash
file="test_dpocket_1.txt"
while IFS= read -r line
do
	fpocket -f  "${line:0:-1}"
	echo "${line:0:-1}"
done <"$file"
echo "over"