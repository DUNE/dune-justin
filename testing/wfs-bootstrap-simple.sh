#!/bin/sh

date
echo "Request: $WFS_REQUEST_ID  Stage: $WFS_STAGE_ID"
echo "Job ID: $WFS_JOB_ID  Cookie: $WFS_COOKIE"

input_file=`$WFS_PATH/get-file`
if [ $? != 0 ] ; then
  echo 'get-file did not return an input file!'
  exit 0
fi

echo "Input file $input_file_did"
input_file_did=`echo "$input_file" | cut -f1 -d' '`
input_file_pfn=`echo "$input_file" | cut -f2 -d' '`
input_file_rse=`echo "$input_file" | cut -f3 -d' '`

export FILETIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
printenv
ls -ltR

# Record that we processed the input file ok 
echo "$input_file_did" > wfs-processed-inputs.txt
echo -n > wfs-unprocessed-inputs.txt

# Fake output files
echo 123 > np04${FILETIMESTAMP}_reco_Z.root 
echo 123 > ${FILETIMESTAMP}_Pandora_Events.pndr 
echo 123 > ${FILETIMESTAMP}_michelremoving.root

# For debugging
for i in *.json
do
  echo "==== Start $i ===="
  cat $i
  echo "==== End $i ===="
done

ls -ltR

exit 0
