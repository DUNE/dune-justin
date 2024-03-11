CREATE TABLE IF NOT EXISTS `stages_jobscripts` (
  `request_id` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `jobscript` text NOT NULL,
  UNIQUE KEY `request_id` (`request_id`,`stage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `jobscripts_library` (
  `jobscript_id` mediumint(8) unsigned AUTO_INCREMENT,
  `scope_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `user_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `author_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `created_time` datetime NOT NULL DEFAULT '1970-01-01',
  `jobscript_name` varchar(255) NOT NULL DEFAULT '',
  `description` varchar(255) NOT NULL DEFAULT '',
  `jobscript` text NOT NULL,
  PRIMARY KEY `jobscript_id` (`jobscript_id`),
  UNIQUE KEY `uniqueness` (`jobscript_name`,`scope_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `scopes` (
  `scope_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `scope_name` varchar(255) NOT NULL DEFAULT '',
  `wlcg_group_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `accounting_group_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY `scope_id` (`scope_id`),
  UNIQUE KEY `scope_name` (`scope_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `wlcg_groups` (
  `wlcg_group_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `wlcg_group_name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY `wlcg_group_id` (`wlcg_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `accounting_groups` (
  `accounting_group_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `accounting_group_name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY `accounting_group_id` (`accounting_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `jobs` (
  `justin_job_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `factory_name` varchar(255) NOT NULL,
  `jobsub_id` varchar(255) NOT NULL,
  `site_job_id` varchar(255) NOT NULL DEFAULT '',
  `site_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `jobsub_state` char(1) NOT NULL DEFAULT 'I',
  `allocation_state` enum('submitted','started','processing','outputting',
                  'finished','notused','aborted','stalled','jobscript_error',
                  'outputting_failed') 
                  NOT NULL DEFAULT 'submitted',
  `allocator_name` varchar(255) NOT NULL DEFAULT '',
  `allocation_error` varchar(255) NOT NULL DEFAULT '',
  `submitted_time` datetime NOT NULL,
  `allocation_time` datetime NOT NULL DEFAULT '1970-01-01',
  `outputting_time` datetime NOT NULL DEFAULT '1970-01-01',
  `finished_time` datetime NOT NULL DEFAULT '1970-01-01',
  `heartbeat_time` datetime NOT NULL DEFAULT '1970-01-01',
  `request_id` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `hostname` varchar(255) NOT NULL DEFAULT '',
  `cpuinfo` varchar(255) NOT NULL DEFAULT '',
  `has_inner_apptainer` tinyint(1) NOT NULL DEFAULT 0,
  `os_release` varchar(255) NOT NULL DEFAULT '',
  `rss_bytes` bigint unsigned NOT NULL DEFAULT 0,
  `min_rss_bytes` bigint unsigned NOT NULL DEFAULT 0,
  `max_rss_bytes` bigint unsigned NOT NULL DEFAULT 0,
  `processors` tinyint unsigned NOT NULL DEFAULT 0,
  `min_processors` tinyint unsigned NOT NULL DEFAULT 0,
  `max_processors` tinyint unsigned NOT NULL DEFAULT 0,
  `wall_seconds` mediumint unsigned NOT NULL DEFAULT 0,
  `max_wall_seconds` mediumint unsigned NOT NULL DEFAULT 0,
  `justin_job_secret` varchar(255) NOT NULL DEFAULT '',
  `jobscript_secret` varchar(255) NOT NULL DEFAULT '',
  `need_to_fetch_jobsub_log` tinyint(1) NOT NULL DEFAULT '0',
  `for_awt` tinyint(1) NOT NULL DEFAULT '0',
  `jobscript_real_seconds` mediumint unsigned NOT NULL DEFAULT 0,
  `jobscript_cpu_seconds` mediumint unsigned NOT NULL DEFAULT 0,
  `jobscript_max_rss_bytes` bigint unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`justin_job_id`),
  KEY `jobsub_id` (`jobsub_id`),
  INDEX `jobsub_state` (`jobsub_state`,
    `allocation_state`,`site_id`),
  INDEX `site_id_allocation_state` (`site_id`,`allocation_state`,
    `submitted_time`),
  INDEX `allocation_state_site_id` (`allocation_state`,`site_id`,
    `submitted_time`),
  INDEX `request_stage_allocation` (`request_id`,`stage_id`,`allocation_state`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `jobs_logs` (
  `justin_job_id` int(10) unsigned NOT NULL,
  `jobscript_log` text NOT NULL DEFAULT '',
  PRIMARY KEY (`justin_job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `events` (
  `event_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event_type_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `request_id` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `file_id` int(10) unsigned NOT NULL DEFAULT 0,
  `justin_job_id` int(10) unsigned NOT NULL DEFAULT 0,
  `site_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `rse_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `event_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `milliseconds` mediumint(8) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`event_id`),
  INDEX `awt` (`event_type_id`,`rse_id`,`site_id`,`event_time`),
  INDEX `request_id` (`request_id`,`stage_id`,`event_type_id`,`rse_id`),
  INDEX `file_id` (`file_id`,`event_id`),
  INDEX `justin_job_id` (`justin_job_id`,`event_id`),
  INDEX `site_id` (`site_id`,`event_id`),
  INDEX `rse_id` (`rse_id`,`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `files` (
  `file_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 1,
  `file_did` varchar(255) NOT NULL,
  `state` enum('finding','unallocated','allocated',
               'outputting','processed','notfound','failed',
               'recorded', 'output') NOT NULL DEFAULT 'finding',
  `justin_job_id` int(10) unsigned NOT NULL DEFAULT 0,
  `processed_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `processed_hour` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `processed_site_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `creator_justin_job_id` int(10) unsigned NOT NULL DEFAULT 0,
  `allocations` tinyint(1) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`file_id`),
  UNIQUE KEY `request_id` (`request_id`,`stage_id`,`file_did`),
  INDEX `justin_job_id` (`justin_job_id`,`request_id`,`stage_id`),
  KEY `state_file_id` (`state`,`file_id`),
  INDEX `request_stage_state_file` (`request_id`,`stage_id`,`state`,`file_id`),
  INDEX `request_stage_file_id` (`request_id`,`stage_id`,`file_id`),
  INDEX `creator_justin_job_id` (`creator_justin_job_id`),
  INDEX `request_stage_state_processed_site` (`request_id`,`stage_id`,`state`,`processed_hour`,`processed_site_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `replicas` (
  `replica_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rse_id` smallint(5) unsigned NOT NULL,
  `file_id` int(10) unsigned NOT NULL,
  `wan_pfn` varchar(255) NOT NULL,
  `lan_pfn` varchar(255) NOT NULL,
  `accessible_until` datetime NOT NULL DEFAULT '9999-12-31 00:00:00',
  `request_id` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY(`replica_id`),
  UNIQUE KEY `rse_id` (`rse_id`,`file_id`),
  UNIQUE KEY `pfn` (`wan_pfn`,`file_id`),
  INDEX `file_id` (`file_id`),
  INDEX `request_stage_rse` (`request_id`,`stage_id`,`rse_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `replicas_pins` (
  `replica_id` int(10) unsigned NOT NULL,
  `pin_expire_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `pin_ref` varchar(255) NOT NULL DEFAULT '',
  `pin_retry_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `pin_recheck_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  PRIMARY KEY(`replica_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `archived_workflows` (
  `workflow_id` mediumint(8) unsigned NOT NULL,
  `description` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`workflow_id`),
  INDEX `user_name` (`user_name`),
  INDEX `created` (`created`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `archived_workflows_rows` (
  `workflow_id` mediumint(8) unsigned NOT NULL,
  `row_id` smallint unsigned NOT NULL,
  `row_name` varchar(255) NOT NULL,
  `row_value` text NOT NULL,
  UNIQUE KEY `row_id` (`workflow_id`,`row_id`),
  INDEX `row_name` (`row_name`,`workflow_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `requests` (
  `request_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `state` enum('draft','submitted','approved','running','paused','checking','finished','deleted') NOT NULL DEFAULT 'finished',
  `name` varchar(255) NOT NULL,
  `scope_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `description` varchar(255) NOT NULL,
  `created` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `submitted` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `started` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `checking` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `finished` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `refind_start_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `refind_end_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `refind_last_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `refind_seconds` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `user_id` smallint(5) unsigned NOT NULL DEFAULT '0',
  `mql` text NOT NULL,
  `archived` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`request_id`),
  INDEX `state` (`state`,`refind_last_time`,`refind_seconds`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `sites` (
  `site_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `site_name` varchar(255) NOT NULL,
  `jobsub_site_name` varchar(255) NOT NULL,
  `wlcg_site_name` varchar(255) NOT NULL,
  `max_processors` tinyint unsigned NOT NULL DEFAULT 1,
  `max_rss_bytes` bigint unsigned NOT NULL DEFAULT 2147483648,
  `max_wall_seconds` mediumint unsigned NOT NULL DEFAULT 162450,
  `enabled` tinyint(1) NOT NULL DEFAULT '0',
  `has_inner_apptainer` tinyint(1) NOT NULL DEFAULT '1',
  `max_jobs` smallint(5) unsigned NOT NULL DEFAULT 100,
  `submitted_jobs` smallint(5) unsigned NOT NULL DEFAULT 0,
  `running_jobs` smallint(5) unsigned NOT NULL DEFAULT 0,
  `last_seen_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_submitted_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_get_stage_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_awt_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_awt_job_id` int(10) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`site_id`),
  UNIQUE KEY `site_name` (`site_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `sites_storages` (
  `site_id` smallint(5) unsigned NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL,
  `distance` float NOT NULL DEFAULT 100.0,
  `read_result` tinyint(1) unsigned NOT NULL DEFAULT 255,
  `write_result` tinyint(1) unsigned NOT NULL DEFAULT 255,
  `justin_job_id` int(10) unsigned NOT NULL DEFAULT 0,
  UNIQUE KEY `rse_id` (`rse_id`,`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `stages` (
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 1,
  `stage_rank` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `processors` tinyint(3) unsigned NOT NULL,
  `jobscript_id` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `wall_seconds` mediumint(8) unsigned DEFAULT NULL,
  `rss_bytes` bigint(20) unsigned DEFAULT NULL,
  `max_distance` float NOT NULL DEFAULT 0.0,
  UNIQUE KEY `request_stage_id` (`request_id`,`stage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `stages_outputs` (
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `lifetime_seconds` int(10) unsigned NOT NULL DEFAULT 86400,
  `file_pattern` varchar(255) NOT NULL,
  `destination` varchar(512) NOT NULL,
  `for_next_stage` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `stages_output_storages` (
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `stages_environment` (
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `env_name` varchar(255) NOT NULL,
  `env_value` text NOT NULL DEFAULT '',
  UNIQUE KEY `multiple` (`request_id`,`stage_id`,`env_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `get_stage_cache` (
  `site_id` smallint(5) unsigned NOT NULL,
  `min_processors` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `max_processors` tinyint(3) unsigned NOT NULL DEFAULT 1,
  `min_rss_bytes` bigint(20) unsigned NOT NULL DEFAULT 0,
  `max_rss_bytes` bigint(20) unsigned NOT NULL DEFAULT 2147483648,
  `max_wall_seconds` mediumint(8) unsigned NOT NULL DEFAULT 86400,
  `job_had_inner_apptainer` tinyint(1) NOT NULL DEFAULT 1,
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `cache_time` datetime NOT NULL,
  UNIQUE KEY `multiple` (`site_id`,
   `min_processors`,`max_processors`,`min_rss_bytes`,`max_rss_bytes`,
   `max_wall_seconds`,`job_had_inner_apptainer`,`request_id`,`stage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `find_file_cache` (
  `site_id` smallint(5) unsigned NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL,
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `replica_id` int(10) unsigned NOT NULL,
  `file_id` int(10) unsigned NOT NULL DEFAULT 0,
  `distance` float NOT NULL DEFAULT 100.0,
  `cache_time` datetime NOT NULL,
  INDEX `multiple` (`site_id`, `request_id`, `stage_id`,
                    `cache_time`, `distance`, `file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `storages` (
  `rse_name` varchar(255) NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `decommissioned` tinyint(1) NOT NULL DEFAULT FALSE,
  `occupancy` float NOT NULL DEFAULT 0,
  `rse_region` varchar(255) NOT NULL DEFAULT '',
  `rse_country` varchar(255) NOT NULL DEFAULT '',
  `rse_site` varchar(255) NOT NULL DEFAULT '',
  `rucio_write` tinyint(1) NOT NULL DEFAULT TRUE,
  `rucio_read` tinyint(1) NOT NULL DEFAULT TRUE,
  `justin_write` tinyint(1) NOT NULL DEFAULT TRUE,
  `justin_read` tinyint(1) NOT NULL DEFAULT TRUE,
  `needs_pin` tinyint(1) NOT NULL DEFAULT FALSE,
  `lan_write_scheme` varchar(255) NOT NULL DEFAULT 'root',
  `wan_write_scheme` varchar(255) NOT NULL DEFAULT 'root',
  PRIMARY KEY (`rse_id`),
  UNIQUE KEY `rse_name` (`rse_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `jwt_keys` (
  `jwks_n` text NOT NULL,
  `jwks_e` varchar(255) NOT NULL,
  `jwks_alg` varchar(255) NOT NULL,
  `jwks_kid` varchar(255) NOT NULL,
  `jwks_use` varchar(255) NOT NULL,
  `jwks_kty` varchar(255) NOT NULL,
  PRIMARY KEY (`jwks_kid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `main_pn_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `access_token` text NOT NULL DEFAULT '',
  `access_token_created` datetime NOT NULL DEFAULT '1970-01-01',
  `access_token_expires` datetime NOT NULL DEFAULT '1970-01-01',
  `refresh_token` text NOT NULL DEFAULT '',
  PRIMARY KEY (`user_id`),
  INDEX `access_token_expires_created` (`access_token_expires`,`access_token_created`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `principal_names` (
  `pn_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `principal_name` varchar(255) NOT NULL,
  `user_id` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`pn_id`),
  UNIQUE KEY `principal_name` (`principal_name`),
  INDEX `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `sessions` (
  `session_id` mediumint(5) unsigned NOT NULL AUTO_INCREMENT,
  `session_type` enum('web','command') NOT NULL DEFAULT 'web',
  `user_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `created_time` datetime NOT NULL DEFAULT '1970-01-01',
  `expires_time` datetime NOT NULL DEFAULT '1970-01-01',
  `linked_session_id` mediumint(5) unsigned NOT NULL DEFAULT 0,
  `justin_session` varchar(255) NOT NULL,
  `justin_secret` varchar(255) NOT NULL,
  `justin_code` varchar(255) NOT NULL,
  `wlcg_groups` text NOT NULL DEFAULT '',
  `saved_uri` varchar(255) NOT NULL DEFAULT '',
  `user_agent` varchar(255) NOT NULL DEFAULT '',
  `os_version` varchar(255) NOT NULL DEFAULT '',
  `ip` varchar(255) NOT NULL DEFAULT '',
  `hostname` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`session_id`),
  UNIQUE KEY `justin_session` (`justin_session`),
  UNIQUE KEY `justin_code` (`justin_code`),
  INDEX `linked_session_id` (`linked_session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

