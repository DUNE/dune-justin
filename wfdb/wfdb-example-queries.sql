# Run with:
# mysql --table --verbose < wfdb-example-queries.sql

USE wfdb
describe requests;
describe stages;
describe bootstraps;
describe files;
describe replicas;
describe storages;
describe sites_storages;

SELECT site_name,storages.rse_id,storages.rse_name,sites_storages.location FROM sites_storages 
 LEFT JOIN storages ON sites_storages.rse_id=storages.rse_id WHERE site_name='UK_Manchester';

SELECT requests.request_id,stages.stage_id,requests.name,stages.any_location FROM requests 
 LEFT JOIN stages ON requests.request_id=stages.request_id ORDER BY requests.request_id,stages.stage_id;

SELECT files.file_id,files.did,storages.rse_name,files.request_id,stages.stage_id FROM files 
 LEFT JOIN stages ON files.request_id=stages.request_id AND files.stage_id=stages.stage_id 
 LEFT JOIN replicas ON files.file_id=replicas.file_id
 LEFT JOIN storages ON replicas.rse_id=storages.rse_id
 WHERE files.state='unallocated' AND ((replicas.rse_id=1 AND stages.any_location) OR replicas.rse_id=2 OR replicas.rse_id=3)
 ORDER BY (replicas.rse_id=2)*3 + (replicas.rse_id=3)*2 + (replicas.rse_id=1) DESC,files.request_id,files.file_id;

 