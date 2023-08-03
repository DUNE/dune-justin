#!/bin/bash
#
# justin-get-classads.sh - script to be run before HTCondor jobs
#                          to get just-in-time classads from justIN
#
# This script was modelled on blocklist.sh from gco_scripts-master
#

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

for prodev in pro dev
do
  http_code=`curl --silent --insecure --data-binary "@${glidein_config}" \
    --output justin-get-classads-$prodev.txt \
    --write-out "%{http_code}\n" \
    --connect-timeout 10 \
    --max-time 20 \
    --retry 5 \
    http://justin-allocator-$prodev.dune.hep.ac.uk/api/get-classads \
    2>/dev/null`

  if [ "$http_code" = 200 -a -r justin-get-classads-$prodev.txt ]
  then
    cat justin-get-classads-$prodev.txt | (
      while read line
      do
        advertise $line "S"
      done 
    )
  fi
done
exit 0
