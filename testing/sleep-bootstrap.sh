#!/bin/sh
#
# Submit with something like this:
#
# ./workflow quick-request --monte-carlo 1 \
# --file sleep-bootstrap.sh 
#
# Then monitor with dashboard or ./workflow show-jobs --request-id ID
# where ID is the value printed by the first command
#

date
sleep 1800
date

# Get an unprocessed file from this stage
did_pfn_rse=`$WFS_PATH/wfs-get-file`
did=`echo $did_pfn_rse | cut -f1 -d' '`
pfn=`echo $did_pfn_rse | cut -f2 -d' '`
rse=`echo $did_pfn_rse | cut -f3 -d' '`

# We say we processed whatever we were given
echo "$did" > wfs-processed-dids.txt

# Nothing unprocessed
echo > wfs-unprocessed-dids.txt

exit 0
