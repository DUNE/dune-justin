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
cat <<EOF >get_stage.json
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

echo '====start get_stage.json===='
cat get_stage.json
echo '====end get_stage.json===='

# Make the call to the Workflow Allocator
http_code=`curl \
--header "X-Jobid: $JOBSUBJOBID" \
--key $X509_USER_PROXY \
--cert $X509_USER_PROXY \
--cacert $X509_USER_PROXY \
--capath ${X509_CERTIFICATES:-/etc/grid-security/certificates/} \
--data @get_stage.json \
--output allocated.tar \
--write-out "%{http_code}\n" \
https://vm20.blackett.manchester.ac.uk/`

if [ "$http_code" != "200" ] ; then
  echo "curl call to WFA fails with code $http_code"
  cat allocated.tar
  exit
fi

tar xvf allocated.tar

# Run the bootstrap script
if [ -r bootstrap.sh ] ; then
  chmod +x bootstrap.sh

  echo '====Start bootstrap.sh===='
  cat bootstrap.sh
  echo '====End bootstrap.sh===='

  ./bootstrap.sh
  retval=$?
else
  # How can this happen???
  echo No bootstrap.sh found
  retval=1
fi

if [ $retval -eq 0 ] ; then

  cat output_patterns.txt
  cat rse_list.txt 
# Use output patterns and RSE list to upload output files
# Insert metadata .json file for each output file

fi

echo '====End of genericjob.sh===='
