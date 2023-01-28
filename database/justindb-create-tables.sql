-- MySQL dump 10.14  Distrib 5.5.68-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: justindb
-- ------------------------------------------------------
-- Server version	5.5.68-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `stages_jobscripts`
--

DROP TABLE IF EXISTS `stages_jobscripts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stages_jobscripts` (
  `request_id` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `jobscript` text NOT NULL,
  UNIQUE KEY `request_id` (`request_id`,`stage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jobscripts_library`
--

DROP TABLE IF EXISTS `jobscripts_library`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobscripts_library` (
  `jobscript_id` mediumint(8) unsigned AUTO_INCREMENT,
  `scope_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `user_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `created_time` datetime NOT NULL DEFAULT '1970-01-01',
  `jobscript_name` varchar(255) NOT NULL DEFAULT '',
  `jobscript` text NOT NULL,
  PRIMARY KEY `jobscript_id` (`jobscript_id`),
  UNIQUE KEY `uniqueness` (`jobscript_name`,`scope_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scopes`
--

DROP TABLE IF EXISTS `scopes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scopes` (
  `scope_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `scope_name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY `scope_id` (`scope_id`),
  UNIQUE KEY `scope_name` (`scope_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs` (
  `justin_job_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `factory_name` varchar(255) NOT NULL,
  `jobsub_id` varchar(255) NOT NULL,
  `site_job_id` varchar(255) NOT NULL DEFAULT '',
  `site_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `jobsub_state` char(1) NOT NULL DEFAULT 'I',
  `allocation_state` enum('submitted','started','processing','outputting',
                  'finished','notused','aborted','stalled','jobscript_error') 
                  NOT NULL DEFAULT 'submitted',
  `allocator_name` varchar(255) NOT NULL DEFAULT '',
  `allocation_error` varchar(255) NOT NULL DEFAULT '',
  `allocation_count` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `submitted_time` datetime NOT NULL,
  `allocation_time` datetime NOT NULL DEFAULT '1970-01-01',
  `outputting_time` datetime NOT NULL DEFAULT '1970-01-01',
  `finished_time` datetime NOT NULL DEFAULT '1970-01-01',
  `heartbeat_time` datetime NOT NULL DEFAULT '1970-01-01',
  `request_id` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `hostname` varchar(255) NOT NULL DEFAULT '',
  `cpuinfo` varchar(255) NOT NULL DEFAULT '',
  `os_release` varchar(255) NOT NULL DEFAULT '',
  `rss_bytes` bigint unsigned NOT NULL DEFAULT 0,
  `min_rss_bytes` bigint unsigned NOT NULL DEFAULT 0,
  `max_rss_bytes` bigint unsigned NOT NULL DEFAULT 0,
  `processors` tinyint unsigned NOT NULL DEFAULT 0,
  `min_processors` tinyint unsigned NOT NULL DEFAULT 0,
  `max_processors` tinyint unsigned NOT NULL DEFAULT 0,
  `wall_seconds` mediumint unsigned NOT NULL DEFAULT 0,
  `max_wall_seconds` mediumint unsigned NOT NULL DEFAULT 0,
  `cookie` varchar(255) NOT NULL DEFAULT '',
  `need_to_fetch_jobsub_log` tinyint(1) NOT NULL DEFAULT '0',
  `for_awt` tinyint(1) NOT NULL DEFAULT '0',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jobs_logs`
--

DROP TABLE IF EXISTS `jobs_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs_logs` (
  `justin_job_id` int(10) unsigned NOT NULL,
  `jobscript_log` text NOT NULL DEFAULT '',
  PRIMARY KEY (`justin_job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
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
  INDEX `request_id` (`request_id`,`stage_id`,`event_type_id`,`rse_id`),
  INDEX `file_id` (`file_id`,`event_id`),
  INDEX `justin_job_id` (`justin_job_id`,`event_id`),
  INDEX `site_id` (`site_id`,`event_id`),
  INDEX `rse_id` (`rse_id`,`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `files` (
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
  INDEX `creator_justin_job_id` (`creator_justin_job_id`),
  INDEX `request_stage_state_processed_site` (`request_id`,`stage_id`,`state`,`processed_hour`,`processed_site_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `replicas`
--

DROP TABLE IF EXISTS `replicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `replicas` (
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `replicas_pins`
--

DROP TABLE IF EXISTS `replicas_pins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `replicas_pins` (
  `replica_id` int(10) unsigned NOT NULL,
  `pin_expire_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `pin_ref` varchar(255) NOT NULL DEFAULT '',
  `pin_retry_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `pin_recheck_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  PRIMARY KEY(`replica_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `requests`
--

DROP TABLE IF EXISTS `requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `requests` (
  `request_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `state` enum('draft','submitted','approved','running','paused','checking','finished','deleted') NOT NULL DEFAULT 'finished',
  `name` varchar(255) NOT NULL,
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
  PRIMARY KEY (`request_id`),
  INDEX `state` (`state`,`refind_last_time`,`refind_seconds`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sites`
--

DROP TABLE IF EXISTS `sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sites` (
  `site_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `site_name` varchar(255) NOT NULL,
  `jobsub_site_name` varchar(255) NOT NULL,
  `wlcg_site_name` varchar(255) NOT NULL,
  `max_processors` tinyint unsigned NOT NULL DEFAULT 1,
  `max_rss_bytes` bigint unsigned NOT NULL DEFAULT 2147483648,
  `max_wall_seconds` mediumint unsigned NOT NULL DEFAULT 162450,
  `enabled` tinyint(1) NOT NULL DEFAULT '0',
  `max_jobs` smallint(5) unsigned NOT NULL DEFAULT 100,
  `submitted_jobs` smallint(5) unsigned NOT NULL DEFAULT 0,
  `running_jobs` smallint(5) unsigned NOT NULL DEFAULT 0,
  `last_seen_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_submitted_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_get_stage_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_awt_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  PRIMARY KEY (`site_id`),
  UNIQUE KEY `site_name` (`site_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sites_storages`
--

DROP TABLE IF EXISTS `sites_storages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sites_storages` (
  `site_id` smallint(5) unsigned NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL,
  `distance` float NOT NULL DEFAULT 100.0,
  `read_result` tinyint(1) unsigned NOT NULL DEFAULT 255,
  `write_result` tinyint(1) unsigned NOT NULL DEFAULT 255,
  `justin_job_id` int(10) unsigned NOT NULL DEFAULT 0,
  UNIQUE KEY `rse_id` (`rse_id`,`site_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stages`
--

DROP TABLE IF EXISTS `stages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stages` (
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 1,
  `stage_rank` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `processors` tinyint(3) unsigned NOT NULL,
  `jobscript_id` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `wall_seconds` mediumint(8) unsigned DEFAULT NULL,
  `rss_bytes` bigint(20) unsigned DEFAULT NULL,
  `max_distance` float NOT NULL DEFAULT 0.0,
  `max_files_per_job` tinyint(3) unsigned NOT NULL DEFAULT 1,
  UNIQUE KEY `request_stage_id` (`request_id`,`stage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stages_outputs`
--

DROP TABLE IF EXISTS `stages_outputs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stages_outputs` (
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `lifetime_seconds` int(10) unsigned NOT NULL DEFAULT 86400,
  `file_pattern` varchar(255) NOT NULL,
  `file_scope` varchar(255) NOT NULL,
  `dataset` varchar(255) NOT NULL,
  `for_next_stage` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stages_outputs`
--

DROP TABLE IF EXISTS `stages_output_storages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stages_output_storages` (
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stages_environment`
--

DROP TABLE IF EXISTS `stages_environment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stages_environment` (
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `env_name` varchar(255) NOT NULL,
  `env_value` text NOT NULL DEFAULT '',
  UNIQUE KEY `multiple` (`request_id`,`stage_id`,`env_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `get_stage_cache`
--

DROP TABLE IF EXISTS `get_stage_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `get_stage_cache` (
  `site_id` smallint(5) unsigned NOT NULL,
  `min_processors` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `max_processors` tinyint(3) unsigned NOT NULL DEFAULT 1,
  `min_rss_bytes` bigint(20) unsigned NOT NULL DEFAULT 0,
  `max_rss_bytes` bigint(20) unsigned NOT NULL DEFAULT 2147483648,
  `max_wall_seconds` mediumint(8) unsigned NOT NULL DEFAULT 86400,
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `cache_time` datetime NOT NULL,
  UNIQUE KEY `multiple` (`site_id`,
   `min_processors`,`max_processors`,`min_rss_bytes`,`max_rss_bytes`,
   `max_wall_seconds`,`cache_time`,`request_id`,`stage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `get_stage_cache`
--

DROP TABLE IF EXISTS `find_file_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `find_file_cache` (
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `storages`
--

DROP TABLE IF EXISTS `storages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storages` (
  `rse_name` varchar(255) NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `occupancy` float NOT NULL DEFAULT 0,
  `rucio_write` tinyint(1) NOT NULL DEFAULT TRUE,
  `rucio_read` tinyint(1) NOT NULL DEFAULT TRUE,
  `justin_write` tinyint(1) NOT NULL DEFAULT TRUE,
  `justin_read` tinyint(1) NOT NULL DEFAULT TRUE,
  `use_for_output` tinyint(1) NOT NULL DEFAULT TRUE,
  `needs_pin` tinyint(1) NOT NULL DEFAULT FALSE,
  `deterministic_rse` tinyint(1) NOT NULL DEFAULT TRUE,
  `write_protocol` varchar(255) NOT NULL DEFAULT 'root',
  PRIMARY KEY (`rse_id`),
  UNIQUE KEY `rse_name` (`rse_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `generic_jobs` tinyint(1) NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

--
-- Table structure for table `x509`
--

DROP TABLE IF EXISTS `x509`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `x509` (
  `x509dn` varchar(255) NOT NULL,
  `user_id` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`x509dn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-09 20:26:10
