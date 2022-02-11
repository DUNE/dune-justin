#!/bin/sh
#
# Generic Job script which will get a stage bootstrap script from the
# Workflow Allocator
#

echo '====Start of genericjob.sh===='

date
printenv
pwd
ls -lR

# Used by bootstrap script to find files from this generic job
export WFS_PATH=`pwd`

# Assemble values we will need 
export job_name="$JOBSUBJOBID"
export dune_site=${GLIDEIN_DUNESite:-XX_UNKNOWN}
export cpuinfo=`grep '^model name' /proc/cpuinfo | head -1 | cut -c14-`
export os_release=`head -1 /etc/redhat-release`
export hostname=`hostname`

# These are probably wrong: we should get them from the HTCondor job ad?
export rss_bytes=`expr ${GLIDEIN_MaxMemMBs:-4096} \* 1024 \* 1024`
export processors=${GLIDEIN_CPUs:-1}
export wall_seconds=${GLIDEIN_Max_Walltime:-86400}

# Check requirements are present

if [ ! -r "$X509_USER_PROXY" ] ; then
 echo "Cannot read X509_USER_PROXY file = $X509_USER_PROXY"
 exit
fi

curl --version
if [ $? -ne 0 ] ; then
 echo Failed running curl
 exit
fi

cp -f $CONDOR_DIR_INPUT/get-file $WFS_PATH

if [ ! -f $WFS_PATH/get-file -o ! -x $WFS_PATH/get-file ] ; then
 echo "$WFS_PATH/get-file missing or not executable"
 exit
fi

# Create the JSON to send to the allocator
cat <<EOF >wfs-get-stage.json
{
  "method"      : "get_stage",
  "job_name"    : "$job_name",
  "dune_site"   : "$dune_site",
  "cpuinfo"     : "$cpuinfo",
  "os_release"  : "$os_release",
  "hostname"    : "$hostname",
  "rss_bytes"   : $rss_bytes,
  "processors"  : $processors,
  "wall_seconds": $wall_seconds
}
EOF

echo '====start wfs-get-stage.json===='
cat wfs-get-stage.json
echo '====end wfs-get-stage.json===='

# Make the call to the Workflow Allocator
http_code=`curl \
--header "X-Jobid: $jobname" \
--key $X509_USER_PROXY \
--cert $X509_USER_PROXY \
--cacert $X509_USER_PROXY \
--capath ${X509_CERTIFICATES:-/etc/grid-security/certificates/} \
--data @wfs-get-stage.json \
--output wfs-files.tar \
--write-out "%{http_code}\n" \
https://wfs-dev.dune.hep.ac.uk/wfa-cgi`

if [ "$http_code" != "200" ] ; then
  echo "curl call to WFA fails with code $http_code"
  cat wfs-files.tar
  exit
fi

tar xvf wfs-files.tar

if [ -r wfs-env.sh ] ; then
  . ./wfs-env.sh
fi

# Run the bootstrap script
if [ -f wfs-bootstrap.sh ] ; then
  chmod +x wfs-bootstrap.sh

  echo '====Start wfs-bootstrap.sh===='
  cat wfs-bootstrap.sh
  echo '====End wfs-bootstrap.sh===='

  mkdir workspace
  ( cd workspace ; $WFA_PATH/wfs-bootstrap.sh )
  retval=$?
else
  # How can this happen???
  echo No wfs-bootstrap.sh found
  retval=1
fi

# Make the lists of output files and files for the next stage
echo -n > wfs-outputs.txt
echo -n > wfs-next-stage-outputs.txt

cat wfs-output-patterns.txt | (
while read for_next_stage pattern
do  
  (
    cd workspace
    # $pattern is wildcard-expanded here - so a list of files
    for fn in $pattern
    do
      if [ -r "$fn" ] ; then
        echo "$fn" >> $WFS_PATH/wfs-outputs.txt
        if [ "$for_next_stage" = "True" ] ; then
          echo "$fn" >> $WFS_PATH/wfs-next-stage-outputs.txt    
        fi
      fi
    done
  )
done
)

next_stage_outputs=`echo \`sed 's/.*/"&"/' wfs-next-stage-outputs.txt\`|sed 's/ /,/g'`

# Just try the first RSE for now
rse=`echo $rse_list | cut -f1 -d' '`

for fn in `cat wfs-outputs.txt`
do
  echo "Would do rucio upload of $fn to $rse"
  echo "Metadata too? $fn.json"
  echo
done

# wfs-bootstrap.sh should produce a list of successfully processed input files
# and a list of files which still need to be processed by another job
processed_inputs=`echo \`sed 's/.*/"&"/' workspace/wfs-processed-inputs.txt\`|sed 's/ /,/g'`
unprocessed_inputs=`echo \`sed 's/.*/"&"/' workspace/wfs-unprocessed-inputs.txt\`|sed 's/ /,/g'`

cat <<EOF >wfs-return-results.json
{
  "method": "return_results",
  "wfs_job_id": "$WFS_JOB_ID",
  "cookie": "$WFS_COOKIE",
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
--data @wfs-return-results.json \
--output return-results.txt \
--write-out "%{http_code}\n" \
https://wfs-dev.dune.hep.ac.uk/wfa-cgi`

echo '====End of genericjob.sh===='
