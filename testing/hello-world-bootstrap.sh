#!/bin/sh

# Get an unprocessed file from this stage
did_pfn_rse=`$WFS_PATH/wfs-get-file`
did=`echo $did_pfn_rse | cut -f1 -d' '`
pfn=`echo $did_pfn_rse | cut -f2 -d' '`
rse=`echo $did_pfn_rse | cut -f3 -d' '`

# We say we processed whatever we were given
echo "$did" > wfs-processed-inputs.txt

# Nothing unprocessed
echo > wfs-unprocessed-inputs.txt

# Hello world
echo "Hello world $pfn"

exit 0
