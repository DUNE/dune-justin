#!/bin/sh
#
# Generic Job script which will get a stage bootstrap script from the
# Workflow Allocator
#

echo '====Start of genericjob.sh===='

# Assemble values we will need 
export executor_id=`hostname`.`date +'%s'`
export dunesite=${GLIDEIN_DUNESite:-XX_UNKNOWN}
export rss_bytes=`expr ${GLIDEIN_MaxMemMBs:-4096} \* 1024 \* 1024`
export processors=${GLIDEIN_CPUs:-1}
export wall_seconds=${GLIDEIN_Max_Walltime:-86400}

if [ ! -r "$X509_USER_PROXY" ] ; then
 echo "Cannot read X509_USER_PROXY file = $X509_USER_PROXY"
 exit
fi

# Create the JSON to send to the allocator
cat <<EOF >wfa-get-stage.json
{
  "method"      : "get_stage",
  "dunesite"    : "$dunesite",
  "rss_bytes"   : $rss_bytes,
  "processors"  : $processors,
  "wall_seconds": $wall_seconds,
  "executor_id" : "$executor_id"
}
EOF

curl --version
if [ $? -ne 0 ] ; then
 echo Failed running curl
 exit
fi

echo '====start wfa-get-stage.json===='
cat wfa-get-stage.json
echo '====end wfa-get-stage.json===='

# Make the call to the Workflow Allocator
http_code=`curl \
--header "X-Jobid: $JOBSUBJOBID" \
--key $X509_USER_PROXY \
--cert $X509_USER_PROXY \
--cacert $X509_USER_PROXY \
--capath ${X509_CERTIFICATES:-/etc/grid-security/certificates/} \
--data @wfa-get-stage.json \
--output wfa-files.tar \
--write-out "%{http_code}\n" \
https://vm20.blackett.manchester.ac.uk/`

if [ "$http_code" != "200" ] ; then
  echo "curl call to WFA fails with code $http_code"
  cat wfa-files.tar
  exit
fi

tar xvf wfa-files.tar

if [ -r wfa-env.sh ] ; then
  . ./wfa-env.sh
fi

# Run the bootstrap script
if [ -r wfa-bootstrap.sh ] ; then
  chmod +x wfa-bootstrap.sh

  echo '====Start wfa-bootstrap.sh===='
  cat wfa-bootstrap.sh
  echo '====End wfa-bootstrap.sh===='

  ./wfa-bootstrap.sh
  retval=$?
else
  # How can this happen???
  echo No wfa-bootstrap.sh found
  retval=1
fi

# Make the lists of output files and files for the next stage
echo -n > wfa-outputs.txt
echo -n > wfa-next-stage-outputs.txt

cat wfa-output-patterns.txt | (
while read for_next_stage pattern
do  
  # $pattern is wildcard-expanded here - so a list of files
  for fn in $pattern
  do
    if [ -r "$fn" ] ; then
      echo "$fn" >> wfa-outputs.txt
      if [ "$for_next_stage" = "True" ] ; then
        echo "$fn" >> wfa-next-stage-outputs.txt    
      fi
    fi
  done
done
)

# This is based on wildcard expansion of the patterns in the stage definition
next_stage_outputs=`echo \`sed 's/.*/"&"/' wfa-next-stage-outputs.txt\`|sed 's/ /,/g'`

# Just try the first one for now
rse=`echo $rse_list | cut -f1 -d' '`

for fn in `cat wfa-outputs.txt`
do
  echo "Would do rucio upload of $fn to $rse"
  echo "Metadata too? $fn.json"
done

# wfa-bootstrap.sh should produce a list of successfully processed input files
# and a list of files which still need to be processed by another job
processed_inputs=`echo \`sed 's/.*/"&"/' wfa-processed-inputs.txt\`|sed 's/ /,/g'`
unprocessed_inputs=`echo \`sed 's/.*/"&"/' wfa-unprocessed-inputs.txt\`|sed 's/ /,/g'`

cat <<EOF >wfa-return-results.json
{
  "method": "return_results",
  "request_id": $request_id,
  "stage_id": $stage_id,
  "cookie": "$cookie",
  "executor_id": "$executor_id",
  "processed_inputs": [$processed_inputs],
  "unprocessed_inputs": [$unprocessed_inputs],
  "next_stage_outputs": [$next_stage_outputs]
}
EOF

http_code=`curl \
--key $X509_USER_PROXY \
--cert $X509_USER_PROXY \
--cacert $X509_USER_PROXY \
--capath ${X509_CERTIFICATES:-/etc/grid-security/certificates/} \
--data @wfa-return-results.json \
--output return-results.txt \
--write-out "%{http_code}\n" \
https://vm20.blackett.manchester.ac.uk/`

echo '====End of genericjob.sh===='
