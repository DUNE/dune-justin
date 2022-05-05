#!/bin/sh
#
# Example bootstrap script that makes sha1sum checksums of all the files
# referred to by the MQL expression give on the workflow command line.
#
# Submit with something like this:
#
# ./workflow quick-request \
#  --mql "files from protodune-sp:np04_raw_run_number_5769" \
#  --output-pattern 'sha1sum-*.txt' \
#  --upload-file simple-bootstrap.sh 
#
# Then monitor with dashboard or ./workflow show-jobs --request-id ID
# where ID is the value printed by the first command
#

# Get an unprocessed file from this stage
did_pfn_rse=`$WFS_PATH/wfs-get-file`
did=`echo $did_pfn_rse | cut -f1 -d' '`
pfn=`echo $did_pfn_rse | cut -f2 -d' '`
rse=`echo $did_pfn_rse | cut -f3 -d' '`

# These files are found by the generic job using the --output-pattern
# form given on the workflow command line (see above).
xrdcp --silent $pfn - | sha1sum >sha1sum-$(date -u +%Y%m%dT%H%M%SZ).txt

# We say we processed whatever we were given
echo "$did" > wfs-processed-inputs.txt

# Nothing unprocessed
echo > wfs-unprocessed-inputs.txt

# Log what we did
echo "Processed $did at $pfn for Request $WFS_REQUEST_ID, Stage $WFS_STAGE_ID"

exit 0
