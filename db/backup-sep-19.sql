-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: django
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add dast',7,'add_dast'),(26,'Can change dast',7,'change_dast'),(27,'Can delete dast',7,'delete_dast'),(28,'Can view dast',7,'view_dast'),(29,'Can add sast',8,'add_sast'),(30,'Can change sast',8,'change_sast'),(31,'Can delete sast',8,'delete_sast'),(32,'Can view sast',8,'view_sast'),(33,'Can add Message',9,'add_message'),(34,'Can change Message',9,'change_message'),(35,'Can delete Message',9,'delete_message'),(36,'Can view Message',9,'view_message'),(37,'Can add DAST Scan Report',10,'add_dastscan'),(38,'Can change DAST Scan Report',10,'change_dastscan'),(39,'Can delete DAST Scan Report',10,'delete_dastscan'),(40,'Can view DAST Scan Report',10,'view_dastscan'),(41,'Can view own DAST scans only',10,'view_own_dastscan'),(42,'Can view all DAST scans',10,'view_all_dastscan');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$ReS0StVpnm3ttdq73vrEIS$Xi/pmxgOWaGIlHF9zqNFYvm/tf9+oAvWWGvwJp2sAq8=','2025-09-18 08:26:11.987378',1,'root','','','minumsusuyuk@gmail.com',1,1,'2025-08-26 11:27:56.219757'),(2,'pbkdf2_sha256$1000000$jDtRV6I5wd2bqe7bICdla3$0ASmV3y9DoSTgrkn94AbQlNimnGOTweYLVnsVuPoFbg=','2025-09-19 02:50:31.645352',0,'dinda','','','',1,1,'2025-09-15 08:53:35.000000'),(3,'pbkdf2_sha256$1000000$WCYGORiLl9qEClIVOoqTeX$j4GipokjHdx74e9O/HRbDNLvVqM1anFx0KkU3+4JBo0=','2025-09-19 02:51:00.596252',0,'yoyo','','','',1,1,'2025-09-15 09:03:19.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (2,2,37),(4,2,39),(8,2,40),(1,2,41),(6,3,37),(7,3,39),(9,3,40),(5,3,41);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_dast`
--

DROP TABLE IF EXISTS `dashboard_dast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_dast` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `nama_website` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_dast`
--

LOCK TABLES `dashboard_dast` WRITE;
/*!40000 ALTER TABLE `dashboard_dast` DISABLE KEYS */;
INSERT INTO `dashboard_dast` VALUES (1,'ffff','2025-09-02 03:16:28.504925','sentinel.investrpo.id/dast/hasil');
/*!40000 ALTER TABLE `dashboard_dast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_sast`
--

DROP TABLE IF EXISTS `dashboard_sast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_sast` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nama_aplikasi` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `versi_aplikasi` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `hasil_scan` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tanggal_scan` datetime(6) NOT NULL,
  `link_hasil_scan` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_sast`
--

LOCK TABLES `dashboard_sast` WRITE;
/*!40000 ALTER TABLE `dashboard_sast` DISABLE KEYS */;
INSERT INTO `dashboard_sast` VALUES (1,'wqfd','V1-344','asf','2025-09-02 03:16:45.176186','af');
/*!40000 ALTER TABLE `dashboard_sast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dast_reports_dastscan`
--

DROP TABLE IF EXISTS `dast_reports_dastscan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dast_reports_dastscan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `target_url` varchar(500) NOT NULL,
  `scan_type` varchar(20) NOT NULL,
  `scan_date` datetime(6) NOT NULL,
  `completed_date` datetime(6) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `results` json DEFAULT NULL,
  `vulnerabilities_found` int NOT NULL,
  `high_vulnerabilities` int NOT NULL,
  `medium_vulnerabilities` int NOT NULL,
  `low_vulnerabilities` int NOT NULL,
  `informational_vulnerabilities` int NOT NULL,
  `scan_duration` bigint DEFAULT NULL,
  `pages_crawled` int NOT NULL,
  `requests_made` int NOT NULL,
  `scan_config` json DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `scheduled` tinyint(1) NOT NULL,
  `jenkins_build_number` int DEFAULT NULL,
  `json_report_path` varchar(500) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `owner_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `jenkins_build_number` (`jenkins_build_number`),
  KEY `dast_reports_dastscan_owner_id_c9a86be4_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `dast_reports_dastscan_owner_id_c9a86be4_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dast_reports_dastscan`
--

LOCK TABLES `dast_reports_dastscan` WRITE;
/*!40000 ALTER TABLE `dast_reports_dastscan` DISABLE KEYS */;
INSERT INTO `dast_reports_dastscan` VALUES (7,'test-yoyo','https://inpension.opsitech.id','full','2025-09-17 07:30:05.568480','2025-09-17 07:33:21.648964','completed',NULL,14,0,2,8,4,177000000,0,0,'{\"jenkins\": {\"base_url\": \"http://sentinel.investpro.id:8080\", \"job_name\": \"DAST-Automasi\", \"username\": \"admin\", \"api_token\": \"11c405e35f3f22adeaa1473199d9bad0c9\", \"job_token\": \"opsitechsec2020\"}, \"scan_parameters\": {\"scan_type\": \"full\", \"target_url\": \"https://inpension.opsitech.id\", \"configured_at\": \"2025-09-16T10:22:45.531338+00:00\", \"auto_configured\": true}}',1,0,215,'/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-215.json','2025-09-16 10:22:45.531615','2025-09-17 07:33:21.649081',3),(8,'danamon.ofor.id','https://danamon.oforu.id','full','2025-09-17 10:54:28.149320','2025-09-17 10:57:31.711707','completed',NULL,20,0,4,9,7,167000000,0,0,'{\"jenkins\": {\"base_url\": \"http://sentinel.investpro.id:8080\", \"job_name\": \"DAST-Automasi\", \"username\": \"admin\", \"api_token\": \"11c405e35f3f22adeaa1473199d9bad0c9\", \"job_token\": \"opsitechsec2020\"}, \"scan_parameters\": {\"scan_type\": \"full\", \"target_url\": \"https://danamon.oforu.id\", \"configured_at\": \"2025-09-17T10:04:14.498991+00:00\", \"auto_configured\": true}}',1,0,218,'/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-218.json','2025-09-17 10:04:14.499249','2025-09-17 10:57:31.711800',2),(11,'test-baru','https://sentinel.opsitech.id','full','2025-09-19 02:51:09.474172','2025-09-19 02:54:09.827193','completed',NULL,0,0,0,0,0,165000000,0,0,'{\"jenkins\": {\"base_url\": \"http://sentinel.investpro.id:8080\", \"job_name\": \"DAST-Automasi\", \"username\": \"admin\", \"api_token\": \"11c405e35f3f22adeaa1473199d9bad0c9\", \"job_token\": \"opsitechsec2020\"}, \"scan_parameters\": {\"scan_type\": \"full\", \"target_url\": \"https://sentinel.opsitech.id\", \"configured_at\": \"2025-09-18T05:29:14.023075+00:00\", \"auto_configured\": true}}',1,0,225,'/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-225.json','2025-09-18 05:29:14.023340','2025-09-19 02:54:09.827295',3),(12,'DAST Scan','https://apps.investpro.id','full','2025-09-18 05:31:06.920658','2025-09-18 05:34:08.002517','completed',NULL,7,0,1,3,3,167000000,0,0,'{\"jenkins\": {\"base_url\": \"http://sentinel.investpro.id:8080\", \"job_name\": \"DAST-Automasi\", \"username\": \"admin\", \"api_token\": \"11c405e35f3f22adeaa1473199d9bad0c9\", \"job_token\": \"opsitechsec2020\"}, \"scan_parameters\": {\"scan_type\": \"full\", \"target_url\": \"https://apps.investpro.id\", \"configured_at\": \"2025-09-18T05:30:57.533424+00:00\", \"auto_configured\": true}}',1,0,222,'/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-222.json','2025-09-18 05:30:57.533904','2025-09-18 05:34:08.002615',2),(13,'DAST Scan','http://stmikprofesional.ac.id','full','2025-09-18 06:23:13.629781','2025-09-18 09:08:03.370024','completed',NULL,0,0,0,0,0,9864000000,0,0,'{\"jenkins\": {\"base_url\": \"http://sentinel.investpro.id:8080\", \"job_name\": \"DAST-Automasi\", \"username\": \"admin\", \"api_token\": \"11c405e35f3f22adeaa1473199d9bad0c9\", \"job_token\": \"opsitechsec2020\"}, \"scan_parameters\": {\"scan_type\": \"full\", \"target_url\": \"http://stmikprofesional.ac.id\", \"configured_at\": \"2025-09-18T06:23:07.330779+00:00\", \"auto_configured\": true}}',1,0,223,'/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-223.json','2025-09-18 06:23:07.331055','2025-09-18 09:08:03.370155',2),(14,'https://sikembang.web.id/','https://sikembang.web.id','full','2025-09-18 09:07:29.463057','2025-09-18 09:11:00.642901','completed',NULL,20,0,5,9,6,174000000,0,0,'{\"jenkins\": {\"base_url\": \"http://sentinel.investpro.id:8080\", \"job_name\": \"DAST-Automasi\", \"username\": \"admin\", \"api_token\": \"11c405e35f3f22adeaa1473199d9bad0c9\", \"job_token\": \"opsitechsec2020\"}, \"scan_parameters\": {\"scan_type\": \"full\", \"target_url\": \"https://sikembang.web.id\", \"configured_at\": \"2025-09-18T09:07:16.285919+00:00\", \"auto_configured\": true}}',1,0,224,'/var/lib/jenkins/workspace/DAST-Automasi@2/zap-reports/zap-report-224.json','2025-09-18 09:07:16.286181','2025-09-18 09:11:00.643001',2);
/*!40000 ALTER TABLE `dast_reports_dastscan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-08-27 04:14:37.737899','3','DAST Scan investrpo - http://investpro.id',1,'[{\"added\": {}}]',10,1),(2,'2025-08-27 04:15:14.914639','3','DAST Scan investrpo - http://investpro.id',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',10,1),(3,'2025-08-27 04:16:02.046994','3','DAST Scan investrpo2 - http://investpro.id',2,'[{\"changed\": {\"fields\": [\"Name\", \"Scan type\", \"High Risk\", \"Medium Risk\", \"Low Risk\", \"Informational\"]}}]',10,1),(4,'2025-08-27 04:16:34.024923','3','DAST Scan investrpo2 - http://investpro.id',2,'[{\"changed\": {\"fields\": [\"Scan type\"]}}]',10,1),(5,'2025-08-27 04:23:28.278597','2','Test Scan - http://investpro.id',2,'[{\"changed\": {\"fields\": [\"Target URL\"]}}]',10,1),(6,'2025-08-28 13:32:09.066685','1','DAST Scan - https://danamon.oforu.id',2,'[{\"changed\": {\"fields\": [\"Target URL\"]}}]',10,1),(7,'2025-08-29 01:45:33.553335','2','Test Scan - http://investpro.id',2,'[]',10,1),(8,'2025-08-29 01:46:21.836099','2','Test Scan - http://investpro.id',3,'',10,1),(9,'2025-09-02 03:16:28.511395','1','sentinel.investrpo.id/dast/hasil',1,'[{\"added\": {}}]',7,1),(10,'2025-09-02 03:16:45.177400','1','wqfd',1,'[{\"added\": {}}]',8,1),(11,'2025-09-02 04:38:58.983890','4','scanmirasentinel.com - https://mirasentinel.com',1,'[{\"added\": {}}]',10,1),(12,'2025-09-03 02:46:36.569333','5','inpension - https://inpension.opsitech.id/',1,'[{\"added\": {}}]',10,1),(13,'2025-09-03 02:50:08.156106','6','test sayursehat - https://sayursehat.com',1,'[{\"added\": {}}]',10,1),(14,'2025-09-03 03:31:18.605951','5','inpension - https://inpension.opsitech.id/',3,'',10,1),(15,'2025-09-03 03:31:18.605986','4','scanmirasentinel.com - https://mirasentinel.com',3,'',10,1),(16,'2025-09-03 03:31:18.605999','3','DAST Scan investrpo2 - http://investpro.id',3,'',10,1),(17,'2025-09-03 03:31:18.606008','1','DAST Scan - https://danamon.oforu.id',3,'',10,1),(18,'2025-09-03 03:31:29.137544','6','test sayursehat - https://sayursehat.com',3,'',10,1),(19,'2025-09-03 03:32:02.095030','7','danamon - https://danamon.oforu.id',1,'[{\"added\": {}}]',10,1),(20,'2025-09-03 04:02:38.302361','8','http://testphp.vulnweb.com - http://testphp.vulnweb.com',1,'[{\"added\": {}}]',10,1),(21,'2025-09-03 09:17:48.372094','9','blueray.id - https://blueraycargo.id/',1,'[{\"added\": {}}]',10,1),(22,'2025-09-04 08:47:13.303067','9','blueray.id - https://blueraycargo.id/',3,'',10,1),(23,'2025-09-08 02:37:23.605861','10','DAST Scan - https://unifa.ac.id',1,'[{\"added\": {}}]',10,1),(24,'2025-09-08 04:09:10.198923','11','siska.unifa.ac.id - https://siska.unifa.ac.id',1,'[{\"added\": {}}]',10,1),(25,'2025-09-09 00:38:18.250185','12','https://infosulawesi.com/DAST Scan - https://infosulawesi.com/',1,'[{\"added\": {}}]',10,1),(26,'2025-09-09 10:34:45.076354','14','investpro.id - https://investpro.id/',1,'[{\"added\": {}}]',10,1),(27,'2025-09-09 10:46:40.367809','16','stmik profesionbla - https://stmikprofesional.ac.id',1,'[{\"added\": {}}]',10,1),(28,'2025-09-10 01:58:18.941792','15','investpro.id - https://investpro.id',3,'',10,1),(29,'2025-09-10 08:12:57.397352','18','blueray.id - https://blueraycargo.id/',1,'[{\"added\": {}}]',10,1),(30,'2025-09-11 02:02:53.801048','18','blueray.id - https://blueraycargo.id/',3,'',10,1),(31,'2025-09-11 02:03:12.515277','12','https://infosulawesi.com/DAST Scan - https://infosulawesi.com/',3,'',10,1),(32,'2025-09-11 02:04:02.386661','14','investpro.id - https://investpro.id/',3,'',10,1),(33,'2025-09-11 03:08:20.181159','22','Production Scan - https://target-application.com',3,'',10,1),(34,'2025-09-11 03:08:32.379355','21','Test with Config - http://test.com',3,'',10,1),(35,'2025-09-11 03:08:32.379387','20','Complete Test - http://example.com',3,'',10,1),(36,'2025-09-11 04:05:33.249696','23','Test Auto-Config - http://test.com',3,'',10,1),(37,'2025-09-11 07:00:37.571144','24','Scan Blueray Cargo - https://blueray-cargo.com',3,'',10,1),(38,'2025-09-11 07:01:45.945165','25','testunikokm - https://unikom.ac.id',1,'[{\"added\": {}}]',10,1),(39,'2025-09-11 07:01:59.897373','25','testunikokm - https://unikom.ac.id',3,'',10,1),(40,'2025-09-11 07:02:33.980142','26','add unikom - https://unikom.ac.id',1,'[{\"added\": {}}]',10,1),(41,'2025-09-11 11:30:09.021906','27','dast-sayursehat.com - https://sayursehat.com',1,'[{\"added\": {}}]',10,1),(42,'2025-09-12 04:07:01.183381','27','dast-sayursehat.com - https://sayursehat.com',3,'',10,1),(43,'2025-09-12 04:07:13.164493','28','dast-sayursehat.com - https://sayursehat.com',3,'',10,1),(44,'2025-09-12 04:09:29.518767','29','www.jamkrindo.co.id/ - https://www.jamkrindo.co.id/',1,'[{\"added\": {}}]',10,1),(45,'2025-09-12 04:53:47.513915','30','www.jamkrindo.co.id/ - https://www.jamkrindo.co.id',3,'',10,1),(46,'2025-09-12 04:53:47.513948','29','www.jamkrindo.co.id/ - https://www.jamkrindo.co.id/',3,'',10,1),(47,'2025-09-12 04:54:35.997380','31','https://inpension.opsitech.id/ - https://inpension.opsitech.id/',1,'[{\"added\": {}}]',10,1),(48,'2025-09-12 06:28:36.543247','31','https://inpension.opsitech.id/ - https://inpension.opsitech.id/',3,'',10,1),(49,'2025-09-12 06:32:33.368480','19','blueray.id - https://blueraycargo.id',3,'',10,1),(50,'2025-09-12 06:32:33.368513','17','investpro.id - https://investpro.id',3,'',10,1),(51,'2025-09-12 06:32:33.368522','16','stmik profesionbla - https://stmikprofesional.ac.id',3,'',10,1),(52,'2025-09-12 06:32:33.368530','13','https://infosulawesi.com/DAST Scan - https://infosulawesi.com',3,'',10,1),(53,'2025-09-12 06:32:33.368556','11','siska.unifa.ac.id - https://siska.unifa.ac.id',3,'',10,1),(54,'2025-09-12 06:32:33.368565','10','DAST Scan - https://unifa.ac.id',3,'',10,1),(55,'2025-09-12 06:32:33.368573','8','http://testphp.vulnweb.com - http://testphp.vulnweb.com',3,'',10,1),(56,'2025-09-12 06:32:33.368581','7','danamon - https://danamon.oforu.id',3,'',10,1),(57,'2025-09-12 07:16:22.961972','33','danamon.oforu.id - https://danamon.oforu.id',1,'[{\"added\": {}}]',10,1),(58,'2025-09-15 01:46:33.043327','33','danamon.oforu.id - https://danamon.oforu.id',3,'',10,1),(59,'2025-09-15 01:46:33.043361','32','https://inpension.opsitech.id/ - https://inpension.opsitech.id',3,'',10,1),(60,'2025-09-15 01:46:33.043371','26','add unikom - https://unikom.ac.id',3,'',10,1),(61,'2025-09-15 01:47:06.281060','34','danamon.oforu - https://danamon.oforu.id',1,'[{\"added\": {}}]',10,1),(62,'2025-09-15 01:52:43.418888','35','inpension - https://inpension.opsitech.id/',1,'[{\"added\": {}}]',10,1),(63,'2025-09-15 04:29:21.421047','36','inpension - https://inpension.opsitech.id',3,'',10,1),(64,'2025-09-15 04:29:21.421077','35','inpension - https://inpension.opsitech.id/',3,'',10,1),(65,'2025-09-15 04:29:34.410638','37','unifa - https://unifa.ac.id',1,'[{\"added\": {}}]',10,1),(66,'2025-09-15 04:41:47.605155','38','sayursehat.com - https://sayursehat.com',1,'[{\"added\": {}}]',10,1),(67,'2025-09-15 06:10:38.434101','37','unifa - https://unifa.ac.id',3,'',10,1),(68,'2025-09-15 06:10:38.434135','34','danamon.oforu - https://danamon.oforu.id',3,'',10,1),(69,'2025-09-15 06:10:52.514622','39','unifa - https://unifa.ac.id',1,'[{\"added\": {}}]',10,1),(70,'2025-09-15 08:51:53.374955','1','DAST Scan investrpo - https://investpro.id (System)',1,'[{\"added\": {}}]',10,1),(71,'2025-09-15 08:53:35.982462','2','dinda',1,'[{\"added\": {}}]',4,1),(72,'2025-09-15 08:54:37.573983','2','dinda',2,'[{\"changed\": {\"fields\": [\"Staff status\", \"User permissions\"]}}]',4,1),(73,'2025-09-15 09:03:20.161731','3','yoyo',1,'[{\"added\": {}}]',4,1),(74,'2025-09-15 09:03:58.793965','3','yoyo',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(75,'2025-09-15 09:04:16.372902','2','dinda',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(76,'2025-09-15 09:05:21.309106','3','yoyo',2,'[]',4,1),(77,'2025-09-15 09:05:39.916883','3','yoyo',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',4,1),(78,'2025-09-15 09:06:10.907665','2','DAST Scanblueay - https://blueraycargo.id (System)',1,'[{\"added\": {}}]',10,3),(79,'2025-09-15 09:07:35.867104','3','yoyo',2,'[]',4,1),(80,'2025-09-15 09:08:06.951988','3','DAST Scan unikom - https://unikom.ac.id (System)',1,'[{\"added\": {}}]',10,2),(81,'2025-09-15 09:09:07.646156','2','dinda',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(82,'2025-09-15 09:09:20.089136','3','yoyo',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(83,'2025-09-16 02:33:52.284468','4','test-yoyo - https://danamon.oforu.id (yoyo)',1,'[{\"added\": {}}]',10,3),(84,'2025-09-16 02:34:26.146789','5','DAST Scan-dinda - https://pinusi.com (dinda)',1,'[{\"added\": {}}]',10,2),(85,'2025-09-16 07:54:20.952771','4','test-yoyo - https://danamon.oforu.id (yoyo)',3,'',10,1),(86,'2025-09-16 07:54:20.952797','5','DAST Scan-dinda - https://pinusi.com (dinda)',3,'',10,1),(87,'2025-09-16 07:59:43.357707','6','DAST Scan - https://sayursehat.com (dinda)',1,'[{\"added\": {}}]',10,2),(88,'2025-09-16 10:20:50.583687','3','DAST Scan unikom - https://unikom.ac.id (System)',3,'',10,1),(89,'2025-09-16 10:20:59.842211','2','DAST Scanblueay - https://blueraycargo.id (System)',3,'',10,1),(90,'2025-09-16 10:20:59.842241','1','DAST Scan investrpo - https://investpro.id (System)',3,'',10,1),(91,'2025-09-16 10:22:45.532228','7','test-yoyo - https://inpension.opsitech.id (yoyo)',1,'[{\"added\": {}}]',10,3),(92,'2025-09-17 10:04:14.499884','8','danamon.ofor.id - https://danamon.oforu.id (dinda)',1,'[{\"added\": {}}]',10,2),(93,'2025-09-18 05:16:01.373312','6','DAST Scan - https://sayursehat.com (dinda)',3,'',10,2),(94,'2025-09-18 05:17:12.532423','9','DAST Scan - http://stmikprofesional.ac.id (yoyo)',1,'[{\"added\": {}}]',10,3),(95,'2025-09-18 05:19:03.840595','10','DAST Scan - http://stmikprofesional.ac.id (dinda)',1,'[{\"added\": {}}]',10,2),(96,'2025-09-18 05:23:00.562859','9','DAST Scan - http://stmikprofesional.ac.id (yoyo)',3,'',10,3),(97,'2025-09-18 05:29:14.023985','11','test-baru - https://sentinel.opsitech.id (yoyo)',1,'[{\"added\": {}}]',10,3),(98,'2025-09-18 05:30:57.534405','12','DAST Scan - https://apps.investpro.id (dinda)',1,'[{\"added\": {}}]',10,2),(99,'2025-09-18 06:22:55.342896','10','DAST Scan - http://stmikprofesional.ac.id (dinda)',3,'',10,2),(100,'2025-09-18 06:23:07.332313','13','DAST Scan - http://stmikprofesional.ac.id (dinda)',1,'[{\"added\": {}}]',10,2),(101,'2025-09-18 09:07:16.287980','14','https://sikembang.web.id/ - https://sikembang.web.id (dinda)',1,'[{\"added\": {}}]',10,2);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'dashboard','dast'),(8,'dashboard','sast'),(10,'dast_reports','dastscan'),(9,'message','message'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-09-15 06:31:43.999736'),(2,'auth','0001_initial','2025-09-15 06:31:44.007616'),(3,'admin','0001_initial','2025-09-15 06:31:44.014301'),(4,'admin','0002_logentry_remove_auto_add','2025-09-15 06:31:44.019432'),(5,'admin','0003_logentry_add_action_flag_choices','2025-09-15 06:31:44.025541'),(8,'dast_reports','0001_initial','2025-09-15 07:34:06.656814'),(9,'dast_reports','0001_initial','2025-09-15 14:47:25.000000'),(10,'dast_reports','0002_set_owner_data','2025-09-15 07:49:15.047766'),(11,'dast_reports','0002_add_owner_field','2025-09-15 15:49:15.000000'),(12,'dast_reports','0003_update_model_owner','2025-09-15 15:50:46.000000'),(13,'contenttypes','0002_remove_content_type_name','2025-09-19 04:52:26.246817');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('a1h3ajk2nkhk522bswofapravl26m4ba','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1ur5lX:MGduzzQNecFa-kze15x6i1Z8mkOeUk78rlANgHo-KSU','2025-09-10 02:19:59.128784'),('bykwobp77tuqgtz2oj0p7dk079jpmnsn','.eJxVjEEOwiAQRe_C2hBoBwou3fcMZAozUjWQlHZlvLtt0oVu33v_v0XAbc1ha7SEOYmr6MTll00Yn1QOkR5Y7lXGWtZlnuSRyNM2OdZEr9vZ_h1kbHlfmwTGEg6MSIMyjhg56tj5fkcOLXsDDKC8RQekB1AaWFs3eVa96Ul8vvw1N-Y:1uz73c:nGO8zDWgGLx8PkT6Jd0vsUlUziKWfRe6ZbwNhBbthzg','2025-10-02 05:19:48.474445'),('cexwhkocrfkqi87t74kvnyexmq647ng6','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uqwZw:_bjtmFNs8Xs6k6zBQraMxOZqBxMaIsJsx3j1hTUs-0E','2025-09-09 16:31:24.017755'),('imui9b0m3lwic3qnhsdddmhk851vk7nb','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uqrqR:JDwzIuZLpCafNjXQi9Q2qH3UyrhaZHjDdL9YVKb9DgE','2025-09-09 11:28:07.668772'),('oglbucoowddj7urlm7ddsvqj8y4hef4t','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uyVWC:H37iqvLJwxwxzJEACG1tKypdir9zHdMF527hQLcK9yI','2025-09-30 13:14:48.254713'),('pzi0gxv9cygax9ecmwfcy6a42stt9417','.eJxVjE0OwiAYBe_C2hCwQMGl-56B8P0gVQNJaVfGu2uTLnT7Zua9REzbWuLWeYkziYsYxOl3g4QPrjuge6q3JrHVdZlB7oo8aJdTI35eD_fvoKRevrWHIXhEl60L5PUZecAMIyRtw5hRASoKBsCwyZwDkVchMTnNYB1ZEu8PDgU5aw:1uzRDA:bDTn14kfVeKzMjj7PUdRyxTI-VrNkShs3wtAWoEVplM','2025-10-03 02:51:00.600005'),('tybwsh8krw5st6pecj44nhdh74w4s5rz','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uxybf:B4cNQ3GqKku9JH1MYy15KG8p9pL8VvByzC0kHcNZaPM','2025-09-29 02:06:15.728345'),('w0m0zcb0n9a7uxt35f2pdsl73ne6egtt','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uvl7P:3Yh6rPsT-f-H6_SCgDfDFyOQZahFjx4FdDZjjDEk6KE','2025-09-22 23:17:51.287814');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message_message`
--

DROP TABLE IF EXISTS `message_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `company` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `subject` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `service` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `priority` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `message_mes_status_03314b_idx` (`status`,`created_at`),
  KEY `message_mes_priorit_ca2ec8_idx` (`priority`,`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message_message`
--

LOCK TABLES `message_message` WRITE;
/*!40000 ALTER TABLE `message_message` DISABLE KEYS */;
INSERT INTO `message_message` VALUES (1,'yati','yahyamatoristmik@gmail.com','+6281543185791','jjj','fxgxfg','RedTeam','zxgxzg','unread','normal','2025-08-28 09:13:26.389415','2025-08-28 09:13:26.389459'),(2,'Tttt','yahyamatoristmik@gmail.com','+6281543185791','Hjhjj','Rtrt','SOC','Gjgj','unread','normal','2025-08-30 18:49:21.873259','2025-08-30 18:49:21.873293');
/*!40000 ALTER TABLE `message_message` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-19 11:54:11
