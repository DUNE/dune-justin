-- MySQL dump 10.14  Distrib 5.5.68-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: wfdb
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
-- Table structure for table `bootstraps`
--

DROP TABLE IF EXISTS `bootstraps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bootstraps` (
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `bootstrap` text NOT NULL,
  UNIQUE KEY `request_id` (`request_id`,`stage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs` (
  `wfs_job_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `factory_name` varchar(255) NOT NULL,
  `submitted_time` datetime NOT NULL,
  `jobsub_id` varchar(255) NOT NULL,
  `site_id` smallint(5) unsigned NOT NULL,
  `slot_size_id` smallint(5) unsigned NOT NULL,
  `jobsub_state` char(1) NOT NULL DEFAULT 'I',
  `allocation_state` enum('submitted','started','processing','finished') NOT NULL DEFAULT 'submitted',
  `allocation_time` datetime NOT NULL DEFAULT '1970-01-01',
  `allocator_name` varchar(255) NOT NULL DEFAULT '',
  `finished_time` datetime NOT NULL DEFAULT '1970-01-01',
  `request_id` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `stage_id` tinyint(3) unsigned NOT NULL DEFAULT 0,
  `hostname` varchar(255) NOT NULL DEFAULT '',
  `cpuinfo` varchar(255) NOT NULL DEFAULT '',
  `os_release` varchar(255) NOT NULL DEFAULT '',
  `rss_bytes` bigint unsigned NOT NULL DEFAULT 0,
  `processors` tinyint unsigned NOT NULL DEFAULT 0,
  `wall_seconds` mediumint unsigned NOT NULL DEFAULT 0,
  `cookie` varchar(255) NOT NULL DEFAULT '',
  `job_user_id` smallint(5) unsigned DEFAULT 0,
  PRIMARY KEY (`wfs_job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jobs_logs`
--

DROP TABLE IF EXISTS `jobs_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs_logs` (
  `wfs_job_id` int(10) unsigned NOT NULL,
  `bootstrap_log` text NOT NULL DEFAULT '',
  PRIMARY KEY (`wfs_job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  `state` enum('finding','unallocated','allocated','processed') NOT NULL DEFAULT 'finding',
  `finding_retry_time` datetime NOT NULL DEFAULT '1970-01-01',
  `last_allocation_id` int(10) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`file_id`),
  UNIQUE KEY `request_id` (`request_id`,`stage_id`,`file_did`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `allocations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `allocations` (
  `allocation_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `file_id` int(10) unsigned NOT NULL,
  `wfs_job_id` int(10) unsigned NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL,
  `allocation_time` datetime NOT NULL,
  `processed_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `processed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY(`allocation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `replicas`
--

DROP TABLE IF EXISTS `replicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `replicas` (
  `rse_id` smallint(5) unsigned NOT NULL,
  `file_id` int(10) unsigned NOT NULL,
  `pfn` varchar(255) NOT NULL,
  UNIQUE KEY `rse_id` (`rse_id`,`file_id`),
  UNIQUE KEY `pfn` (`pfn`,`file_id`)
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
  `state` enum('draft','submitted','running','paused','checking','completed','deleted') NOT NULL,
  `name` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  `submitted` datetime DEFAULT NULL,
  `started` datetime DEFAULT NULL,
  `checking` datetime DEFAULT NULL,
  `completed` datetime DEFAULT NULL,
  `refind_seconds` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `refind_end_time` datetime DEFAULT '1970-01-01 00:00:00',
  `find_last_time` datetime DEFAULT '1970-01-01 00:00:00',
  `submitter_id` smallint(5) unsigned NOT NULL DEFAULT '0',
  `mql` text NOT NULL,
  PRIMARY KEY (`request_id`)
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
  `enabled` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`site_id`),
  UNIQUE KEY `site_name` (`site_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `slot_sizes`
--

DROP TABLE IF EXISTS `slot_sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `slot_sizes` (
  `slot_size_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `site_id` smallint(5) unsigned NOT NULL,
  `max_processors` tinyint unsigned NOT NULL,
  `min_processors` tinyint unsigned NOT NULL DEFAULT 1,
  `min_rss_bytes` bigint unsigned NOT NULL,
  `max_rss_bytes` bigint unsigned NOT NULL,
  `max_wall_seconds` mediumint unsigned NOT NULL,
  `last_seen_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_submitted_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_no_match_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `last_allocation_time` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  PRIMARY KEY (`slot_size_id`),
  UNIQUE KEY `site_id` (`site_id`,`min_rss_bytes`,`max_rss_bytes`,
                        `max_processors`,`min_processors`,`max_wall_seconds`)
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
  `location` enum('samesite','nearby','accessible') NOT NULL DEFAULT 'accessible',
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
  `processors` tinyint(3) unsigned NOT NULL,
  `wall_seconds` mediumint(8) unsigned DEFAULT NULL,
  `rss_bytes` bigint(20) unsigned DEFAULT NULL,
  `any_location` tinyint(1) NOT NULL DEFAULT 0,
  `num_finding` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `num_unallocated` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `num_allocated` mediumint(8) unsigned NOT NULL DEFAULT 0,
  `num_processed` mediumint(8) unsigned NOT NULL DEFAUlT 0,
  UNIQUE KEY `request_id` (`request_id`,`stage_id`)
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
-- Table structure for table `storages`
--

DROP TABLE IF EXISTS `storages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storages` (
  `rse_name` varchar(255) NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `occupancy` float NOT NULL DEFAULT 0,
  `rse_write` tinyint(1) NOT NULL DEFAULT TRUE,
  `rse_read` tinyint(1) NOT NULL DEFAULT TRUE,
  `rse_delete` tinyint(1) NOT NULL DEFAULT TRUE,
  `ignore_for_output` tinyint(1) NOT NULL DEFAULT FALSE,
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
  `name` varchar(255) NOT NULL,
  `x509dn` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `x509dn` (`x509dn`)
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
