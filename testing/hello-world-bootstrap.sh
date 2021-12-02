#!/bin/sh

input_file_did='##wfa_files_did##'

FILETIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)

echo "hello world $input_file_did" > $FILETIMESTAMP.helloworld.dat

echo "$input_file_did" > wfa-processed-inputs.txt

exit 0
