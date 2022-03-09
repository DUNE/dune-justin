#!/bin/sh
#
# Temporary script to build requests by
# - finding files matching the MQL for requests in the finding state
#   from Rucio (not MetaCat yet)
# - finding the RSEs with replicas of files in the finding state
#
# This will be rewritten in Python as an agent with better error recovery etc
#

. /usr/lib/python3.6/site-packages/wfs/conf.py

# Process any requests in the finding state

mysql -u $mysqlUser -p$mysqlPassword -N -B \
 -e 'SELECT request_id,mql FROM requests WHERE state="finding"' wfdb | (
  while read request_id first second rest
  do
    # We're using Rucio to find the files in a dataset here rather than
    # sending the full MQL to MetaCat. This is a bit of a hack until MetaCat
    # is fully populated and usable.
    #
    # For now we can only handle MQLs of the form: from files scope:name
    # where scope:name is a Rucio dataset.
    
  
    if [ "$first" = 'files' -a "$second" = 'from' ] ; then
      dataset=`echo "$rest" | sed 's/[^a-z,A-Z,0-9,.,:,_,-]/_/g'`
  
      rucio list-files --csv "$dataset" | (
      
        while read line
        do
          filename=`echo "$line" | cut -f1 -d, | sed 's/[^a-z,A-Z,0-9,.,:,_,-]/_/g'`

          mysql -u $mysqlUser -p$mysqlPassword \
           -e "INSERT INTO files SET request_id=$request_id,stage_id=1,file_did='$filename'" wfdb
        done
      
      )
    elif [ "$first" = 'montecarlo' -a "$second" = 'limit' ] ; then
      # If this is a montecarlo request then we make counter files to
      # keep track of how many jobs should run MC for this request
      counter="$rest"
      
      while [ "$counter" -gt 0 ]
      do
        mysql -u $mysqlUser -p$mysqlPassword \
              -e "INSERT INTO files SET request_id=$request_id,stage_id=1,file_did='wfsmontecarlo:$request_id.$counter'" wfdb
        counter=`expr "$counter" - 1`
      done
    
    else
      echo "Cannot parse MQL '$mql'"
    fi

    # Bit of a leap of faith here: what if there was an error earlier???
    mysql -u $mysqlUser -p$mysqlPassword \
          -e "UPDATE requests SET state='running' WHERE request_id=$request_id" wfdb
    
  done
)

# Lookup replicas for any files still in the finding state

mysql -u $mysqlUser -p$mysqlPassword -N -B \
      -e 'SELECT file_id,file_did FROM files WHERE state="finding" ORDER BY file_id LIMIT 10' wfdb | (
  while read file_id file_did
  do
   scope=`echo $file_did | cut -f1 -d:`
   
   if [ "$scope" = "wfsmontecarlo" ] ; then
     # Special handling for Monte Carlo requests: all the replicas are
     # on the MONTECARLO RSE (in Monaco)
     mysql -u $mysqlUser -p$mysqlPassword \
           -e "INSERT INTO replicas SET file_id=$file_id,rse_id=(SELECT rse_id FROM storages WHERE rse_name='MONTECARLO')" wfdb
   else
     rucio list-file-replicas "$file_did" | tail -n +4 | grep '^|' | cut -d'|' -f6 | sed 's/:/ /' | (

     while read rse pfn
     do
       mysql -u $mysqlUser -p$mysqlPassword \
             -e "INSERT INTO replicas SET file_id=$file_id,pfn='$pfn',rse_id=(SELECT rse_id FROM storages WHERE rse_name='$rse')" wfdb
     done   
   
     )
   fi

   # Bit of a leap of faith here: what if there was an error earlier???
   mysql -u $mysqlUser -p$mysqlPassword \
         -e "UPDATE files SET state='unallocated' WHERE file_id=$file_id" wfdb    
  done
)
