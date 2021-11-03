#!/bin/sh

cat <<EOF
DELETE FROM requests;
DELETE FROM stages;
DELETE FROM stages_outputs;
DELETE FROM bootstraps;
DELETE FROM files;
DELETE FROM replicas;
DELETE FROM storages;
DELETE FROM sites_storages;

ALTER TABLE requests AUTO_INCREMENT=1;
ALTER TABLE files AUTO_INCREMENT=1;
ALTER TABLE storages AUTO_INCREMENT=1;

# Set up four sites: Manchester and RAL-Tier1 nearby each other, FNAL and CERN just accessible
INSERT INTO storages SET rse_name='FNAL_DCACHE';
INSERT INTO storages SET rse_name='MANCHESTER';
INSERT INTO storages SET rse_name='RAL_ECHO';
INSERT INTO storages SET rse_name='CERN_PDUNE_EOS';

# FNAL_DCACHE
INSERT INTO sites_storages SET rse_id=1,site_name='US_FNAL',location='samesite';
INSERT INTO sites_storages SET rse_id=1,site_name='UK_RAL-Tier1',location='accessible';
INSERT INTO sites_storages SET rse_id=1,site_name='UK_Manchester',location='accessible';
INSERT INTO sites_storages SET rse_id=1,site_name='CERN',location='accessible';

# MANCHESTER
INSERT INTO sites_storages SET rse_id=2,site_name='US_FNAL',location='accessible';
INSERT INTO sites_storages SET rse_id=2,site_name='UK_RAL-Tier1',location='nearby';
INSERT INTO sites_storages SET rse_id=2,site_name='UK_Manchester',location='samesite';
INSERT INTO sites_storages SET rse_id=2,site_name='CERN',location='accessible';

# RAL_ECHO
INSERT INTO sites_storages SET rse_id=3,site_name='US_FNAL',location='accessible';
INSERT INTO sites_storages SET rse_id=3,site_name='UK_RAL-Tier1',location='samesite';
INSERT INTO sites_storages SET rse_id=3,site_name='UK_Manchester',location='nearby';
INSERT INTO sites_storages SET rse_id=3,site_name='CERN',location='accessible';

# CERN_PDUNE_EOS
INSERT INTO sites_storages SET rse_id=4,site_name='US_FNAL',location='accessible';
INSERT INTO sites_storages SET rse_id=4,site_name='UK_RAL-Tier1',location='accessible';
INSERT INTO sites_storages SET rse_id=4,site_name='UK_Manchester',location='accessible';
INSERT INTO sites_storages SET rse_id=4,site_name='CERN',location='samesite';

# One request with one stage
INSERT INTO requests SET state='running',name='WFATest1',created=NOW(),submitted=NOW(),approved=NOW();
INSERT INTO stages SET request_id=1,stage_id=1,max_inputs=1,max_wall_seconds=10000,max_rss_bytes=4900000000,min_processors=1,max_processors=1,any_location=FALSE;
INSERT INTO stages_outputs SET request_id=1,stage_id=1,pattern="np04*_reco*Z.root",for_next_stage=FALSE;
INSERT INTO stages_outputs SET request_id=1,stage_id=1,pattern="*_Pandora_Events.pndr",for_next_stage=FALSE;
INSERT INTO stages_outputs SET request_id=1,stage_id=1,pattern="*_michelremoving.root",for_next_stage=FALSE;
INSERT INTO bootstraps SET request_id=1,stage_id=1,bootstrap="
EOF

if [ -r wfa-bootstrap.sh ] ; then
  sed 's:\\:\\\\:g' wfa-bootstrap.sh | sed 's/"/\\\"/g' 
else
  echo 'FATAL ERROR! wfa-bootstrap.sh MUST BE IN THE CURRENT DIRECTORY!'
  exit 1
fi

echo '";'

# The replicas of this dataset are at FNAL and CERN
samweb list-definition-files PDSPProd2-goodruns6GeVc_slice_423582_stage_2000 | (

file_id=1

while read file_did
do
  fnal_url=`samweb get-file-access-url --schema=xroot --location enstore $file_did`
  cern_url=`samweb get-file-access-url --schema=xroot --location cern-eos $file_did`

  # Only insert if at CERN and FNAL (they all should be)
  if [ "$fnal_url" != "" -a "$cern_url" != "" ] ; then
    echo "INSERT INTO files SET request_id=1,stage_id=1,file_did=\"$file_did\",state=\"unallocated\";"

    # Record that replicas are at FNAL/CERN/Both with 1:1:1 ratio
    remainder=`expr $file_id % 3`

    if [ "$fnal_url" != "" -a $remainder -ne 1 ] ; then
      echo "INSERT INTO replicas SET file_id=$file_id,rse_id=1;"
    fi

    if [ "$cern_url" != "" -a $remainder -ne 2 ] ; then
      echo "INSERT INTO replicas SET file_id=$file_id,rse_id=4;"
    fi

    file_id=`expr $file_id + 1`
    if [ $file_id -gt 20 ] ; then
     break
    fi
  fi
done

)
