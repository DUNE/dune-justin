date
input_file_did='##wfa_files_did##'
wfa_cookie='##wfa_cookie##'
request_id='##wfa_request_id##'
stage_id='##wfa_stage_id##'
echo 'Request = $request_id and Stage = $stage_id'
echo "Input file $input_file_did and cookie $wfa_cookie"

printenv
ls -ltR

export CLUSTER=${CLUSTER:-1}
export PROCESS=${PROCESS:-1}

. /cvmfs/fermilab.opensciencegrid.org/products/common/etc/setups
export FILETIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh
setup dunetpc v09_09_01 -q e19:prof
setup protoduneana v09_09_01 -q e19:prof
setup duneutil v09_09_01_01 -q e19:prof
setup dune_oslibs v1_0_0
setup sam_web_client

# We will do this with RUCIO lightweight client soon???
if [ "$GLIDEIN_DUNESite" == "CERN" ] ; then
  sam_location=cern-eos
elif [ "$GLIDEIN_DUNESite" == "US_FNAL" ] ; then
  sam_location=enstore
else
  sam_location=enstore
fi
input_file_url=`samweb get-file-access-url --schema=xroot --location=$sam_location $input_file_did`

echo "Found input file URL $input_file_url"

sed -e "s/\"DUNE_CERN_SEP2018\"/\"DUNE_CERN_SEP2018_ANALYSIS\"/" ${DUNETPC_DIR}/job/BeamEvent.fcl > ./BeamEvent.fcl

lar --nevts 3 \
    -c protoDUNE_SP_keepup_decoder_reco_stage1.fcl \
    -o %ifb_reco1_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}.root \
    $input_file_url

lar -c michelremoving.fcl -s *_reco1_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}.root

cp ${JSB_TMP}/JOBSUB_LOG_FILE ./PDSPProd2-goodruns6GeVc_slice_423582_stage_2000_${CLUSTER}_${PROCESS}.out
cp ${JSB_TMP}/JOBSUB_ERR_FILE ./PDSPProd2-goodruns6GeVc_slice_423582_stage_2000_${CLUSTER}_${PROCESS}.err

extractor_prod.py \
 --infile $(ls *reco1_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}.root) \
 --appfamily art --appname reco --appversion v09_09_01 \
 --campaign WFATest1 --no_crc --data_stream physics > $(ls *_reco1_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}.root).json

mv michelremoving.root $(ls *reco1_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}.root | sed -e "s/\.root/_michelremoving.root/")

mv Pandora_Events.pndr $(ls *reco1_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}.root | sed -e "s/\.root/_Pandora_Events\.pndr/")

mv $(ls hist_*reco.root) $(ls hist_*_reco.root | sed -e "s/\.root/_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}\.root/")

pandora_metadata.py \
 --infile $(ls *_Pandora_Events.pndr)  \
 --appfamily art --appname reco \
 --appversion v09_09_01 --campaign WFATest1 --no_crc --data_stream physics \
 --input_json $(ls *_reco1_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}.root.json) \
 > $(ls *_Pandora_Events.pndr).json

pandora_metadata.py \
 --infile $(ls *_michelremoving.root)  \
 --appfamily art --appname calana --appversion v09_09_01 --campaign WFATest1 \
 --no_crc --data_stream physics \
 --input_json $(ls *_reco1_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}.root.json) \
 --data_tier root-tuple --file_format rootntuple --strip_parents > $(ls *_michelremoving.root).json

sed -i -e "/file_name/ a     \"parents\": [\"$(ls *reco1_${CLUSTER}_${PROCESS}_${FILETIMESTAMP}.root)\"]," $(ls *_michelremoving.root).json

# Upload outputs

cat <<EOF >return_results.json
{ 
  "method": "return_results", 
  "cookie": "$wfa_cookie", 
  "executor_id": "$executor_id", 
  "inputs": [{"file_did": "$input_file_did", "state": "processed"}],
  "request_id": $request_id,
  "stage_id": $stage_id,
  "outputs": [
EOF

comma=''
for i in np04*_reco*Z.root *_Pandora_Events.pndr *_michelremoving.root
do
  echo "Would would upload $i to storage and register it in RUCIO with that file name"
  echo ${comma}'{"file_did": "$i", "metadata": ' >>return_results.json
  cat $i.json
  echo "}" >>return_results.json
  comma=','
done

cat <<EOF >> return_results.json
             ]
}
EOF

http_code=`curl \
--key $X509_USER_PROXY \
--cert $X509_USER_PROXY \
--cacert $X509_USER_PROXY \
--capath ${X509_CERTIFICATES:-/etc/grid-security/certificates/} \
--data @return_results.json \
--output return_results.txt \
--write-out "%{http_code}\n" \
https://vm20.blackett.manchester.ac.uk/`

echo "curl call to WFA returns code $http_code"
cat return_results.txt

#
for i in *.json
do
  echo "==== Start $i ===="
  cat $i
  echo "==== End $i ===="
done

ls -ltR
