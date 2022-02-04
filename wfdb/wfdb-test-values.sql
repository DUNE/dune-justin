USE wfdb

DELETE FROM requests;
DELETE FROM stages;
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

# Create one request where files can only be processed from nearby sites
INSERT INTO requests SET state='running',name='test request 1',created=NOW(),submitted=NOW(),approved=NOW();
INSERT INTO stages SET request_id=1,stage_id=1,max_inputs=1,max_wall_seconds=86400,max_rss_bytes=8123123,min_processors=1,max_processors=1,any_location=FALSE;
INSERT INTO bootstraps SET request_id=1,stage_id=1;

##wfa_files_did_rse##';

INSERT INTO files SET request_id=1,stage_id=1,file_did='file.01.01';
INSERT INTO files SET request_id=1,stage_id=1,file_did='file.01.02';
INSERT INTO files SET request_id=1,stage_id=1,file_did='file.01.03';

# First file is everywhere; second file is at FNAL and RAL; third file is only at FNAL
INSERT INTO replicas SET file_id=1,rse_id=1;
INSERT INTO replicas SET file_id=1,rse_id=2;
INSERT INTO replicas SET file_id=1,rse_id=3;

INSERT INTO replicas SET file_id=2,rse_id=1;
INSERT INTO replicas SET file_id=2,rse_id=3;

INSERT INTO replicas SET file_id=3,rse_id=1;

# Create another request where files can be processed from any site
INSERT INTO requests SET state='running',name='test request 2',created=NOW(),submitted=NOW(),approved=NOW();
INSERT INTO stages SET request_id=2,stage_id=1,max_inputs=1,max_wall_seconds=86400,max_rss_bytes=8123123,min_processors=1,max_processors=1,any_location=TRUE;
INSERT INTO bootstraps SET request_id=2,stage_id=1;

INSERT INTO files SET request_id=2,stage_id=1,file_did='file.02.01';
INSERT INTO files SET request_id=2,stage_id=1,file_did='file.02.02';
INSERT INTO files SET request_id=2,stage_id=1,file_did='file.02.03';

# First file is everywhere; second file is at FNAL and RAL; third file is only at FNAL
INSERT INTO replicas SET file_id=4,rse_id=1;
INSERT INTO replicas SET file_id=4,rse_id=2;
INSERT INTO replicas SET file_id=4,rse_id=3;

INSERT INTO replicas SET file_id=5,rse_id=1;
INSERT INTO replicas SET file_id=5,rse_id=3;

INSERT INTO replicas SET file_id=6,rse_id=1;

# Use same script for all bootstraps

UPDATE bootstraps SET bootstrap="
cat <<EOF >files.txt
##wfa_files_did##
EOF

for i in `cat files.txt`
do
 echo Could process $i
done

echo 'Files JSON: ##wfa_files_json##'

echo 'Request = ##wfa_request_id## and Stage = ##wfa_stage_id##'

wfa_cookie='##wfa_cookie##'
echo The WFA Cookie is $wfa_cookie
";