DELETE FROM storages;
DELETE FROM sites_storages;

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
