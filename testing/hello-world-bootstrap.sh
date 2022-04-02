#!/bin/sh

# Get an unprocessed file from this stage
did_pfn_rse=`$WFS_PATH/wfs-get-file`
did=`echo $did_pfn_rse | cut -f1 -d' '`

# We say we processed whatever we were given
echo "$did" > wfs-processed-inputs.txt

# Nothing unprocessed
echo > wfs-unprocessed-inputs.txt

# Hello world
echo "Hello world"

exit 0
