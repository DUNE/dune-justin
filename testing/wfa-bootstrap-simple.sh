#!/bin/sh

date
input_file_did='##wfa_files_did##'
output_rse=`echo ##wfa_rse_list##|cut -f1 -d' '`
wfa_cookie='##wfa_cookie##'
request_id='##wfa_request_id##'
stage_id='##wfa_stage_id##'
echo 'Request = $request_id and Stage = $stage_id'
echo "Input file $input_file_did and cookie $wfa_cookie"

export FILETIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)

printenv
ls -ltR

# Record that we processed the input file ok 
echo "$input_file_did" >> wfa-processed-inputs.txt
touch wfa-unprocessed-inputs.txt

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
