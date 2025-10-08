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
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add dast',7,'add_dast'),(26,'Can change dast',7,'change_dast'),(27,'Can delete dast',7,'delete_dast'),(28,'Can view dast',7,'view_dast'),(29,'Can add sast',8,'add_sast'),(30,'Can change sast',8,'change_sast'),(31,'Can delete sast',8,'delete_sast'),(32,'Can view sast',8,'view_sast'),(33,'Can add Message',9,'add_message'),(34,'Can change Message',9,'change_message'),(35,'Can delete Message',9,'delete_message'),(36,'Can view Message',9,'view_message'),(37,'Can add DAST Scan Report',10,'add_dastscan'),(38,'Can change DAST Scan Report',10,'change_dastscan'),(39,'Can delete DAST Scan Report',10,'delete_dastscan'),(40,'Can view DAST Scan Report',10,'view_dastscan');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$ReS0StVpnm3ttdq73vrEIS$Xi/pmxgOWaGIlHF9zqNFYvm/tf9+oAvWWGvwJp2sAq8=','2025-09-15 02:06:15.725640',1,'root','','','minumsusuyuk@gmail.com',1,1,'2025-08-26 11:27:56.219757');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
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
  `target_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `scan_date` datetime(6) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `results` json DEFAULT NULL,
  `vulnerabilities_found` int NOT NULL,
  `scan_duration` bigint DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  `completed_date` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `high_vulnerabilities` int NOT NULL,
  `informational_vulnerabilities` int NOT NULL,
  `low_vulnerabilities` int NOT NULL,
  `medium_vulnerabilities` int NOT NULL,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `pages_crawled` int NOT NULL,
  `requests_made` int NOT NULL,
  `scan_config` json DEFAULT NULL,
  `scan_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `scheduled` tinyint(1) DEFAULT '0',
  `updated_at` datetime(6) NOT NULL,
  `jenkins_build_number` int DEFAULT NULL,
  `json_report_path` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `jenkins_build_number` (`jenkins_build_number`),
  KEY `dast_report_status_b59c34_idx` (`status`,`scan_date`),
  KEY `dast_report_target__960872_idx` (`target_url`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dast_reports_dastscan`
--

LOCK TABLES `dast_reports_dastscan` WRITE;
/*!40000 ALTER TABLE `dast_reports_dastscan` DISABLE KEYS */;
INSERT INTO `dast_reports_dastscan` VALUES (34,'https://danamon.oforu.id','2025-09-15 01:47:06.262362','completed',NULL,20,168000000,1,'2025-09-15 01:50:17.033148','2025-09-15 01:47:06.280038',0,7,9,4,'danamon.oforu',0,0,'{\"jenkins\": {\"base_url\": \"http://sentinel.investpro.id:8080\", \"job_name\": \"DAST-Automasi\", \"username\": \"admin\", \"api_token\": \"11c405e35f3f22adeaa1473199d9bad0c9\", \"job_token\": \"opsitechsec2020\"}, \"scan_parameters\": {\"scan_type\": \"full\", \"target_url\": \"https://danamon.oforu.id\", \"configured_at\": \"2025-09-15T01:47:06.279740+00:00\", \"auto_configured\": true}}','full',0,'2025-09-15 01:50:17.033251',205,'/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-205.json'),(37,'https://unifa.ac.id','2025-09-15 04:29:34.409617','completed',NULL,9,167000000,1,'2025-09-15 04:32:42.103463','2025-09-15 04:29:34.410205',0,4,4,1,'unifa',0,0,'{\"jenkins\": {\"base_url\": \"http://sentinel.investpro.id:8080\", \"job_name\": \"DAST-Automasi\", \"username\": \"admin\", \"api_token\": \"11c405e35f3f22adeaa1473199d9bad0c9\", \"job_token\": \"opsitechsec2020\"}, \"scan_parameters\": {\"scan_type\": \"full\", \"target_url\": \"https://unifa.ac.id\", \"configured_at\": \"2025-09-15T04:29:34.410004+00:00\", \"auto_configured\": true}}','full',0,'2025-09-15 04:32:42.103541',207,'/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-207.json'),(38,'https://sayursehat.com','2025-09-15 04:41:47.604141','completed',NULL,20,199000000,1,'2025-09-15 04:45:22.031238','2025-09-15 04:41:47.604708',0,10,6,4,'sayursehat.com',0,0,'{\"jenkins\": {\"base_url\": \"http://sentinel.investpro.id:8080\", \"job_name\": \"DAST-Automasi\", \"username\": \"admin\", \"api_token\": \"11c405e35f3f22adeaa1473199d9bad0c9\", \"job_token\": \"opsitechsec2020\"}, \"scan_parameters\": {\"scan_type\": \"full\", \"target_url\": \"https://sayursehat.com\", \"configured_at\": \"2025-09-15T04:41:47.604511+00:00\", \"auto_configured\": true}}','full',0,'2025-09-15 04:45:22.031315',208,'/var/lib/jenkins/workspace/DAST-Automasi/zap-reports/zap-report-208.json');
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
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-08-27 04:14:37.737899','3','DAST Scan investrpo - http://investpro.id',1,'[{\"added\": {}}]',10,1),(2,'2025-08-27 04:15:14.914639','3','DAST Scan investrpo - http://investpro.id',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',10,1),(3,'2025-08-27 04:16:02.046994','3','DAST Scan investrpo2 - http://investpro.id',2,'[{\"changed\": {\"fields\": [\"Name\", \"Scan type\", \"High Risk\", \"Medium Risk\", \"Low Risk\", \"Informational\"]}}]',10,1),(4,'2025-08-27 04:16:34.024923','3','DAST Scan investrpo2 - http://investpro.id',2,'[{\"changed\": {\"fields\": [\"Scan type\"]}}]',10,1),(5,'2025-08-27 04:23:28.278597','2','Test Scan - http://investpro.id',2,'[{\"changed\": {\"fields\": [\"Target URL\"]}}]',10,1),(6,'2025-08-28 13:32:09.066685','1','DAST Scan - https://danamon.oforu.id',2,'[{\"changed\": {\"fields\": [\"Target URL\"]}}]',10,1),(7,'2025-08-29 01:45:33.553335','2','Test Scan - http://investpro.id',2,'[]',10,1),(8,'2025-08-29 01:46:21.836099','2','Test Scan - http://investpro.id',3,'',10,1),(9,'2025-09-02 03:16:28.511395','1','sentinel.investrpo.id/dast/hasil',1,'[{\"added\": {}}]',7,1),(10,'2025-09-02 03:16:45.177400','1','wqfd',1,'[{\"added\": {}}]',8,1),(11,'2025-09-02 04:38:58.983890','4','scanmirasentinel.com - https://mirasentinel.com',1,'[{\"added\": {}}]',10,1),(12,'2025-09-03 02:46:36.569333','5','inpension - https://inpension.opsitech.id/',1,'[{\"added\": {}}]',10,1),(13,'2025-09-03 02:50:08.156106','6','test sayursehat - https://sayursehat.com',1,'[{\"added\": {}}]',10,1),(14,'2025-09-03 03:31:18.605951','5','inpension - https://inpension.opsitech.id/',3,'',10,1),(15,'2025-09-03 03:31:18.605986','4','scanmirasentinel.com - https://mirasentinel.com',3,'',10,1),(16,'2025-09-03 03:31:18.605999','3','DAST Scan investrpo2 - http://investpro.id',3,'',10,1),(17,'2025-09-03 03:31:18.606008','1','DAST Scan - https://danamon.oforu.id',3,'',10,1),(18,'2025-09-03 03:31:29.137544','6','test sayursehat - https://sayursehat.com',3,'',10,1),(19,'2025-09-03 03:32:02.095030','7','danamon - https://danamon.oforu.id',1,'[{\"added\": {}}]',10,1),(20,'2025-09-03 04:02:38.302361','8','http://testphp.vulnweb.com - http://testphp.vulnweb.com',1,'[{\"added\": {}}]',10,1),(21,'2025-09-03 09:17:48.372094','9','blueray.id - https://blueraycargo.id/',1,'[{\"added\": {}}]',10,1),(22,'2025-09-04 08:47:13.303067','9','blueray.id - https://blueraycargo.id/',3,'',10,1),(23,'2025-09-08 02:37:23.605861','10','DAST Scan - https://unifa.ac.id',1,'[{\"added\": {}}]',10,1),(24,'2025-09-08 04:09:10.198923','11','siska.unifa.ac.id - https://siska.unifa.ac.id',1,'[{\"added\": {}}]',10,1),(25,'2025-09-09 00:38:18.250185','12','https://infosulawesi.com/DAST Scan - https://infosulawesi.com/',1,'[{\"added\": {}}]',10,1),(26,'2025-09-09 10:34:45.076354','14','investpro.id - https://investpro.id/',1,'[{\"added\": {}}]',10,1),(27,'2025-09-09 10:46:40.367809','16','stmik profesionbla - https://stmikprofesional.ac.id',1,'[{\"added\": {}}]',10,1),(28,'2025-09-10 01:58:18.941792','15','investpro.id - https://investpro.id',3,'',10,1),(29,'2025-09-10 08:12:57.397352','18','blueray.id - https://blueraycargo.id/',1,'[{\"added\": {}}]',10,1),(30,'2025-09-11 02:02:53.801048','18','blueray.id - https://blueraycargo.id/',3,'',10,1),(31,'2025-09-11 02:03:12.515277','12','https://infosulawesi.com/DAST Scan - https://infosulawesi.com/',3,'',10,1),(32,'2025-09-11 02:04:02.386661','14','investpro.id - https://investpro.id/',3,'',10,1),(33,'2025-09-11 03:08:20.181159','22','Production Scan - https://target-application.com',3,'',10,1),(34,'2025-09-11 03:08:32.379355','21','Test with Config - http://test.com',3,'',10,1),(35,'2025-09-11 03:08:32.379387','20','Complete Test - http://example.com',3,'',10,1),(36,'2025-09-11 04:05:33.249696','23','Test Auto-Config - http://test.com',3,'',10,1),(37,'2025-09-11 07:00:37.571144','24','Scan Blueray Cargo - https://blueray-cargo.com',3,'',10,1),(38,'2025-09-11 07:01:45.945165','25','testunikokm - https://unikom.ac.id',1,'[{\"added\": {}}]',10,1),(39,'2025-09-11 07:01:59.897373','25','testunikokm - https://unikom.ac.id',3,'',10,1),(40,'2025-09-11 07:02:33.980142','26','add unikom - https://unikom.ac.id',1,'[{\"added\": {}}]',10,1),(41,'2025-09-11 11:30:09.021906','27','dast-sayursehat.com - https://sayursehat.com',1,'[{\"added\": {}}]',10,1),(42,'2025-09-12 04:07:01.183381','27','dast-sayursehat.com - https://sayursehat.com',3,'',10,1),(43,'2025-09-12 04:07:13.164493','28','dast-sayursehat.com - https://sayursehat.com',3,'',10,1),(44,'2025-09-12 04:09:29.518767','29','www.jamkrindo.co.id/ - https://www.jamkrindo.co.id/',1,'[{\"added\": {}}]',10,1),(45,'2025-09-12 04:53:47.513915','30','www.jamkrindo.co.id/ - https://www.jamkrindo.co.id',3,'',10,1),(46,'2025-09-12 04:53:47.513948','29','www.jamkrindo.co.id/ - https://www.jamkrindo.co.id/',3,'',10,1),(47,'2025-09-12 04:54:35.997380','31','https://inpension.opsitech.id/ - https://inpension.opsitech.id/',1,'[{\"added\": {}}]',10,1),(48,'2025-09-12 06:28:36.543247','31','https://inpension.opsitech.id/ - https://inpension.opsitech.id/',3,'',10,1),(49,'2025-09-12 06:32:33.368480','19','blueray.id - https://blueraycargo.id',3,'',10,1),(50,'2025-09-12 06:32:33.368513','17','investpro.id - https://investpro.id',3,'',10,1),(51,'2025-09-12 06:32:33.368522','16','stmik profesionbla - https://stmikprofesional.ac.id',3,'',10,1),(52,'2025-09-12 06:32:33.368530','13','https://infosulawesi.com/DAST Scan - https://infosulawesi.com',3,'',10,1),(53,'2025-09-12 06:32:33.368556','11','siska.unifa.ac.id - https://siska.unifa.ac.id',3,'',10,1),(54,'2025-09-12 06:32:33.368565','10','DAST Scan - https://unifa.ac.id',3,'',10,1),(55,'2025-09-12 06:32:33.368573','8','http://testphp.vulnweb.com - http://testphp.vulnweb.com',3,'',10,1),(56,'2025-09-12 06:32:33.368581','7','danamon - https://danamon.oforu.id',3,'',10,1),(57,'2025-09-12 07:16:22.961972','33','danamon.oforu.id - https://danamon.oforu.id',1,'[{\"added\": {}}]',10,1),(58,'2025-09-15 01:46:33.043327','33','danamon.oforu.id - https://danamon.oforu.id',3,'',10,1),(59,'2025-09-15 01:46:33.043361','32','https://inpension.opsitech.id/ - https://inpension.opsitech.id',3,'',10,1),(60,'2025-09-15 01:46:33.043371','26','add unikom - https://unikom.ac.id',3,'',10,1),(61,'2025-09-15 01:47:06.281060','34','danamon.oforu - https://danamon.oforu.id',1,'[{\"added\": {}}]',10,1),(62,'2025-09-15 01:52:43.418888','35','inpension - https://inpension.opsitech.id/',1,'[{\"added\": {}}]',10,1),(63,'2025-09-15 04:29:21.421047','36','inpension - https://inpension.opsitech.id',3,'',10,1),(64,'2025-09-15 04:29:21.421077','35','inpension - https://inpension.opsitech.id/',3,'',10,1),(65,'2025-09-15 04:29:34.410638','37','unifa - https://unifa.ac.id',1,'[{\"added\": {}}]',10,1),(66,'2025-09-15 04:41:47.605155','38','sayursehat.com - https://sayursehat.com',1,'[{\"added\": {}}]',10,1);
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
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-08-26 10:39:31.046381'),(2,'auth','0001_initial','2025-08-26 10:39:31.516322'),(3,'admin','0001_initial','2025-08-26 10:39:31.624551'),(4,'admin','0002_logentry_remove_auto_add','2025-08-26 10:39:31.631434'),(5,'admin','0003_logentry_add_action_flag_choices','2025-08-26 10:39:31.638819'),(6,'contenttypes','0002_remove_content_type_name','2025-08-26 10:39:31.734623'),(7,'auth','0002_alter_permission_name_max_length','2025-08-26 10:39:31.789352'),(8,'auth','0003_alter_user_email_max_length','2025-08-26 10:39:31.808544'),(9,'auth','0004_alter_user_username_opts','2025-08-26 10:39:31.814549'),(10,'auth','0005_alter_user_last_login_null','2025-08-26 10:39:31.860479'),(11,'auth','0006_require_contenttypes_0002','2025-08-26 10:39:31.862809'),(12,'auth','0007_alter_validators_add_error_messages','2025-08-26 10:39:31.869983'),(13,'auth','0008_alter_user_username_max_length','2025-08-26 10:39:31.922182'),(14,'auth','0009_alter_user_last_name_max_length','2025-08-26 10:39:31.970405'),(15,'auth','0010_alter_group_name_max_length','2025-08-26 10:39:31.988429'),(16,'auth','0011_update_proxy_permissions','2025-08-26 10:39:31.995402'),(17,'auth','0012_alter_user_first_name_max_length','2025-08-26 10:39:32.045348'),(18,'dashboard','0001_initial','2025-08-26 10:39:32.084815'),(19,'dast_reports','0001_initial','2025-08-26 10:39:32.105884'),(20,'message','0001_initial','2025-08-26 10:39:32.156762'),(21,'sessions','0001_initial','2025-08-26 10:39:32.186312'),(22,'dast_reports','0002_alter_dastscan_options_dastscan_active_and_more','2025-08-26 10:58:03.196090'),(23,'dast_reports','0003_alter_dastscan_active_alter_dastscan_scheduled','2025-08-26 11:52:46.690433'),(24,'dast_reports','0004_alter_dastscan_options_and_more','2025-09-09 03:37:39.326274'),(25,'dast_reports','0005_dastscan_jenkins_build_number_and_more','2025-09-09 06:21:35.226026'),(26,'dast_reports','0006_alter_dastscan_json_report_path','2025-09-10 08:00:35.080073'),(27,'dast_reports','0007_fix_cloning_issues','2025-09-10 08:37:34.558056'),(28,'dast_reports','0008_alter_dastscan_scan_config','2025-09-11 03:06:59.957277');
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
INSERT INTO `django_session` VALUES ('a1h3ajk2nkhk522bswofapravl26m4ba','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1ur5lX:MGduzzQNecFa-kze15x6i1Z8mkOeUk78rlANgHo-KSU','2025-09-10 02:19:59.128784'),('cexwhkocrfkqi87t74kvnyexmq647ng6','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uqwZw:_bjtmFNs8Xs6k6zBQraMxOZqBxMaIsJsx3j1hTUs-0E','2025-09-09 16:31:24.017755'),('imui9b0m3lwic3qnhsdddmhk851vk7nb','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uqrqR:JDwzIuZLpCafNjXQi9Q2qH3UyrhaZHjDdL9YVKb9DgE','2025-09-09 11:28:07.668772'),('lgqdlfp9zgnv4qljsdxz5l2z8ty9qygc','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uwWRr:1SJrRzuQqDXmNvOooizdlqsV1NJOcl-KoIx5MCkaxWI','2025-09-25 01:50:07.415833'),('owncg882tshpgr35reexh7z3slm0if2e','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uwh1k:JDnk5Y9dWaJxze0h1xYk8F6GtHX5RU1EotIlS0u-PR4','2025-09-25 13:07:52.148757'),('tybwsh8krw5st6pecj44nhdh74w4s5rz','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uxybf:B4cNQ3GqKku9JH1MYy15KG8p9pL8VvByzC0kHcNZaPM','2025-09-29 02:06:15.728345'),('w0m0zcb0n9a7uxt35f2pdsl73ne6egtt','.eJxVjEEOwiAQRe_C2hBwplRcuu8ZyDCDUjWQlHZlvLs26aLd_vfe_6hAy5zD0tIURlFXZdVpv0XiVyorkCeVR9VcyzyNUa-K3mjTQ5X0vm3u4SBTy_8ahDovYD2CdWKgdwh4Iew9MHsyzp1ZDJJF9kkEOmOZCPkuMUVGUd8fw5k4HA:1uvl7P:3Yh6rPsT-f-H6_SCgDfDFyOQZahFjx4FdDZjjDEk6KE','2025-09-22 23:17:51.287814');
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

-- Dump completed on 2025-09-15 12:03:49
