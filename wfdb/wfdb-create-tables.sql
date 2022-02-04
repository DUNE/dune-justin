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
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `files` (
  `file_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `request_id` mediumint(8) unsigned NOT NULL,
  `stage_id` tinyint(3) unsigned NOT NULL,
  `file_did` varchar(255) NOT NULL,
  `state` enum('finding','unallocated','allocated','processed') NOT NULL DEFAULT 'finding',
  `allocated_time` datetime NOT NULL,
  `allocator_id` varchar(255) NOT NULL,
  `executor_id` varchar(255) NOT NULL,
  PRIMARY KEY (`file_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `replicas`
--

DROP TABLE IF EXISTS `replicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `replicas` (
  `rse_id` smallint(5) unsigned NOT NULL,
  `file_id` int(10) unsigned NOT NULL
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
  `state` enum('draft','submitted','approved','finding','running','paused','checking','completed','deleted') NOT NULL,
  `name` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  `submitted` datetime DEFAULT NULL,
  `approved` datetime DEFAULT NULL,
  `checking` datetime DEFAULT NULL,
  `completed` datetime DEFAULT NULL,
  `submitter_id` smallint(5) unsigned NOT NULL DEFAULT '0',
  `cookie` varchar(255) NOT NULL,
  `mql` text NOT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sites_storages`
--

DROP TABLE IF EXISTS `sites_storages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sites_storages` (
  `site_name` varchar(255) NOT NULL,
  `rse_id` smallint(5) unsigned NOT NULL,
  `location` enum('samesite','nearby','accessible') NOT NULL DEFAULT 'samesite',
  UNIQUE KEY `rse_id` (`rse_id`,`site_name`)
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
  `stage_id` tinyint(3) unsigned NOT NULL,
  `max_inputs` tinyint(3) unsigned NOT NULL,
  `min_processors` tinyint(3) unsigned NOT NULL,
  `max_processors` tinyint(3) unsigned NOT NULL,
  `max_wall_seconds` mediumint(8) unsigned DEFAULT NULL,
  `max_rss_bytes` bigint(20) unsigned DEFAULT NULL,
  `any_location` tinyint(1) NOT NULL DEFAULT '0',
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
  `pattern` varchar(255) NOT NULL,
  `for_next_stage` tinyint(1) NOT NULL DEFAULT '0'
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
  `occupancy` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`rse_id`),
  UNIQUE KEY `rse_name` (`rse_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
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
  PRIMARY KEY (`user_id`)
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

-- Dump completed on 2021-11-15 13:41:40
