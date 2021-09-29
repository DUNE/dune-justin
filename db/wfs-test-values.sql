USE wfs

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

# Set up three sites: Manchester and RAL-Tier1 nearby each other, FNAL across the Atlantic

INSERT INTO storages SET rse_name='FNAL_DCACHE';
INSERT INTO storages SET rse_name='MANCHESTER';
INSERT INTO storages SET rse_name='RAL_ECHO';

INSERT INTO sites_storages SET rse_id=1,site_name='US_FNAL',location='samesite';
INSERT INTO sites_storages SET rse_id=1,site_name='UK_RAL-Tier1',location='accessible';
INSERT INTO sites_storages SET rse_id=1,site_name='UK_Manchester',location='accessible';

INSERT INTO sites_storages SET rse_id=2,site_name='UK_RAL-Tier1',location='nearby';
INSERT INTO sites_storages SET rse_id=2,site_name='UK_Manchester',location='samesite';

INSERT INTO sites_storages SET rse_id=3,site_name='UK_RAL-Tier1',location='samesite';
INSERT INTO sites_storages SET rse_id=3,site_name='UK_Manchester',location='nearby';

# Create one request where files can only be processed from nearby sites
INSERT INTO requests SET state='running',name='test request 1',created=NOW(),submitted=NOW(),approved=NOW();
INSERT INTO stages SET request_id=1,stage_id=1,min_inputs=1,max_inputs=1,max_wall_seconds=86400,max_rss_bytes=8123123,any_location=FALSE;
INSERT INTO bootstraps SET request_id=1,stage_id=1,bootstrap='##wfa_files_json##\n##wfa_files_did_rse##';

INSERT INTO files SET request_id=1,stage_id=1,file_did='file.01.01';
INSERT INTO files SET request_id=1,stage_id=1,file_did='file.01.02';
INSERT INTO files SET request_id=1,stage_id=1,file_did='file.01.03';

INSERT INTO replicas SET file_id=1,rse_id=1;
INSERT INTO replicas SET file_id=1,rse_id=2;
INSERT INTO replicas SET file_id=1,rse_id=3;

INSERT INTO replicas SET file_id=2,rse_id=2;

INSERT INTO replicas SET file_id=3,rse_id=2;
INSERT INTO replicas SET file_id=3,rse_id=3;

# Create another request where files can be processed from any site
INSERT INTO requests SET state='running',name='test request 2',created=NOW(),submitted=NOW(),approved=NOW();
INSERT INTO stages SET request_id=2,stage_id=1,min_inputs=1,max_inputs=1,max_wall_seconds=86400,max_rss_bytes=8123123,any_location=TRUE;
INSERT INTO bootstraps SET request_id=2,stage_id=1,bootstrap='##wfa_files_json##\n##wfa_files_did_rse##';

INSERT INTO files SET request_id=2,stage_id=1,file_did='file.02.01';
INSERT INTO files SET request_id=2,stage_id=1,file_did='file.02.02';
INSERT INTO files SET request_id=2,stage_id=1,file_did='file.02.03';

INSERT INTO replicas SET file_id=4,rse_id=1;
INSERT INTO replicas SET file_id=4,rse_id=2;
INSERT INTO replicas SET file_id=4,rse_id=3;

INSERT INTO replicas SET file_id=5,rse_id=2;

INSERT INTO replicas SET file_id=6,rse_id=2;
INSERT INTO replicas SET file_id=6,rse_id=3;

