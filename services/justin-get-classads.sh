#!/bin/bash
:<<'EOF'

justin-get-classads.sh - script to be run before HTCondor jobs
                         to get just-in-time classads from justIN

This script was modelled on blocklist.sh from gco_scripts-master

Test with

cat <<'EOFEOF' >/tmp/justin-get-classads.glidein_config.txt
function add_config_line { echo add_config_line $* 
}
function add_condor_vars_line { echo add_condor_vars_line $* 
}
:<<'EEOOFF'
ADD_CONFIG_LINE_SOURCE /tmp/justin-get-classads.glidein_config.txt
CONDOR_VARS_FILE /tmp/justin-get-classads.glidein_config.txt
ERROR_GEN_PATH /tmp/justin-get-classads.glidein_config.txt
EEOOFF
EOFEOF

./justin-get-classads.sh /tmp/justin-get-classads.glidein_config.txt

EOF

glidein_config="$1"

function info { 
    echo "$@" 1>&2
}

function advertise {
    # atype is the type of the value as defined by GlideinWMS:
    #   I - integer
    #   S - quoted string
    #   C - unquoted string (i.e. Condor keyword or expression)
    local key="$1"
    local value="$2"
    local atype="$3"

    if [ "$glidein_config" != "NONE" ]; then
        add_config_line $key "$value"
        add_condor_vars_line $key "$atype" "-" "+" "Y" "Y" "+" 
    fi  

    if [ "$atype" = "S" ]; then
        echo "$key = \"$value\""
    else
        echo "$key = $value"
    fi  
}

# import add_config_line and add_condor_vars_line functions 

add_config_line_source=`grep '^ADD_CONFIG_LINE_SOURCE ' "${glidein_config}" | awk '{print $2}'`
condor_vars_file=`grep -i '^CONDOR_VARS_FILE ' "${glidein_config}" | awk '{print $2}'` 
error_gen=`grep '^ERROR_GEN_PATH ' "${glidein_config}" | awk '{print $2}'`

source ${add_config_line_source} 

#----------MAIN SCRIPT----------#

export HAS_INNER_APPTAINER=False
if [ -x /cvmfs/oasis.opensciencegrid.org/mis/apptainer/current/bin/apptainer ]
then
  /cvmfs/oasis.opensciencegrid.org/mis/apptainer/current/bin/apptainer \
  shell --shell /usr/bin/hostname \
  /cvmfs/singularity.opensciencegrid.org/fermilab/fnal-wn-sl7:osg3.6  
  if [ $? = 0 ] ; then
    export HAS_INNER_APPTAINER=True
  fi
fi

( echo '==== justin-get-classads glidein_config ===='
  cat "${glidein_config}" 
  echo '==== justin-get-classads printenv ===='
  printenv ) > justin-get-classads-posted.txt

for prodev in pro dev
do
  http_code=`curl --silent --insecure \
    --data-binary @justin-get-classads-posted.txt \
    --output justin-get-classads-$prodev.txt \
    --write-out "%{http_code}\n" \
    --connect-timeout 10 \
    --max-time 60 \
    --retry 5 \
    http://justin-allocator-$prodev.dune.hep.ac.uk/api/get-classads \
    2>/dev/null`

  if [ "$http_code" = 200 -a -r justin-get-classads-$prodev.txt ] ; then
    cat justin-get-classads-$prodev.txt | (
      while read line
      do
        advertise $line "S"
      done
    )
  fi
done
exit 0
