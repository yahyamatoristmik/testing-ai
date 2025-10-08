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
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'viewer');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (2,1,28),(1,1,32);
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
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add dast',7,'add_dast'),(26,'Can change dast',7,'change_dast'),(27,'Can delete dast',7,'delete_dast'),(28,'Can view dast',7,'view_dast'),(29,'Can add sast',8,'add_sast'),(30,'Can change sast',8,'change_sast'),(31,'Can delete sast',8,'delete_sast'),(32,'Can view sast',8,'view_sast'),(33,'Can add Message',9,'add_message'),(34,'Can change Message',9,'change_message'),(35,'Can delete Message',9,'delete_message'),(36,'Can view Message',9,'view_message'),(37,'Can add ZAP Scan Report',10,'add_zapscan'),(38,'Can change ZAP Scan Report',10,'change_zapscan'),(39,'Can delete ZAP Scan Report',10,'delete_zapscan'),(40,'Can view ZAP Scan Report',10,'view_zapscan'),(41,'Can add DAST Scan Report',11,'add_dastscan'),(42,'Can change DAST Scan Report',11,'change_dastscan'),(43,'Can delete DAST Scan Report',11,'delete_dastscan'),(44,'Can view DAST Scan Report',11,'view_dastscan');
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
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$zTuGb3S6XUyESLxfByYM0Y$gQ5kCRNElObeDaikA0ltA5iFUdCgzk4dtTezegJ0KCg=','2025-08-26 07:36:20.792769',1,'root','','','',1,1,'2025-08-13 05:02:05.269206'),(2,'pbkdf2_sha256$600000$zNurof6k5ekv02wvZP5Dco$PcPA8vLyANIqMxXF1rdclmI5uK9izuzkzztcn1eo8bU=','2025-08-14 02:06:25.493365',0,'yahyamatori','yahya','matori','yahya.matori@infovesta.com',1,1,'2025-08-13 07:20:57.000000');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,2,1);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `link` varchar(255) NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `nama_website` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_dast`
--

LOCK TABLES `dashboard_dast` WRITE;
/*!40000 ALTER TABLE `dashboard_dast` DISABLE KEYS */;
INSERT INTO `dashboard_dast` VALUES (2,'http://sentinel.investpro.id:8080/','2025-08-13 05:03:54.662567','jenkins-dast-infovesta');
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
  `nama_aplikasi` varchar(255) NOT NULL,
  `versi_aplikasi` varchar(50) NOT NULL,
  `hasil_scan` longtext NOT NULL,
  `tanggal_scan` datetime(6) NOT NULL,
  `link_hasil_scan` longtext NOT NULL DEFAULT (_utf8mb3''),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_sast`
--

LOCK TABLES `dashboard_sast` WRITE;
/*!40000 ALTER TABLE `dashboard_sast` DISABLE KEYS */;
INSERT INTO `dashboard_sast` VALUES (1,'chatBot-BE-V1','V1-344','http://sentinel.investpro.id/sast/p-chatbot-be/semgrep-output.json','2025-08-13 07:00:46.909847','http://sentinel.investpro.id/sast/p-chatbot-be/semgrep-output.json');
/*!40000 ALTER TABLE `dashboard_sast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dast_reports_zapscan`
--

DROP TABLE IF EXISTS `dast_reports_zapscan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dast_reports_zapscan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `scan_directory` varchar(500) NOT NULL,
  `scan_date` datetime(6) NOT NULL,
  `json_report_path` varchar(500) NOT NULL,
  `html_report_path` varchar(500) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dast_reports_zapscan`
--

LOCK TABLES `dast_reports_zapscan` WRITE;
/*!40000 ALTER TABLE `dast_reports_zapscan` DISABLE KEYS */;
/*!40000 ALTER TABLE `dast_reports_zapscan` ENABLE KEYS */;
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
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-08-13 05:03:13.219746','1','jenkins-dast-infovesta',1,'[{\"added\": {}}]',7,1),(2,'2025-08-13 05:03:46.138080','1','jenkins-dast-infovesta',3,'',7,1),(3,'2025-08-13 05:03:54.663079','2','jenkins-dast-infovesta',1,'[{\"added\": {}}]',7,1),(4,'2025-08-13 07:00:46.911773','1','chatBot-BE-V1',1,'[{\"added\": {}}]',8,1),(5,'2025-08-13 07:15:23.163161','1','chatBot-BE-V1',2,'[{\"changed\": {\"fields\": [\"Link hasil scan\"]}}]',8,1),(6,'2025-08-13 07:20:02.200035','1','viewer',1,'[{\"added\": {}}]',3,1),(7,'2025-08-13 07:20:58.128994','2','yahyamatori',1,'[{\"added\": {}}]',4,1),(8,'2025-08-13 07:21:46.516280','2','yahyamatori',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Groups\", \"Last login\"]}}]',4,1),(9,'2025-08-19 07:12:58.133688','2','mbmbm - ewet (Read)',2,'[{\"changed\": {\"fields\": [\"Status\", \"Priority\"]}}]',9,1),(10,'2025-08-20 14:17:05.690161','7','Dinda - Tete (Read)',2,'[{\"changed\": {\"fields\": [\"Status\", \"Priority\"]}}]',9,1),(11,'2025-08-21 04:33:33.885174','7','Dinda - Tete (Read)',3,'',9,1),(12,'2025-08-25 10:55:22.697830','9','eafsdgsdgf - rerefefefef (Unread)',3,'',9,1),(13,'2025-08-25 10:55:22.697876','8','Bai - Tekkkk (Unread)',3,'',9,1),(14,'2025-08-25 10:55:22.697896','6','c cccvcv - ascac (Unread)',3,'',9,1),(15,'2025-08-25 10:55:22.697913','5','zcvzxv - CZvZV (Unread)',3,'',9,1),(16,'2025-08-25 10:55:22.697928','4','Yahya Matori - Gjthu (Unread)',3,'',9,1),(17,'2025-08-25 10:55:22.697943','3','wewe - wewe (Unread)',3,'',9,1),(18,'2025-08-25 10:55:22.697956','2','mbmbm - ewet (Read)',3,'',9,1),(19,'2025-08-25 10:55:22.697969','1','asfafadf - rerefefefef (Unread)',3,'',9,1),(20,'2025-08-26 07:59:09.349673','10','fdfdfd - aca (Unread)',1,'[{\"added\": {}}]',9,1),(21,'2025-08-26 07:59:24.232994','11','ssssss - ss (Unread)',1,'[{\"added\": {}}]',9,1),(22,'2025-08-26 07:59:32.875453','11','ssssss - ss (Unread)',3,'',9,1),(23,'2025-08-26 07:59:37.382783','10','fdfdfd - aca (Unread)',3,'',9,1),(24,'2025-08-26 08:10:17.958556','12','sdasda - adfaf (Unread)',1,'[{\"added\": {}}]',9,1),(25,'2025-08-26 08:10:25.043237','12','sdasda - adfaf (Unread)',3,'',9,1);
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
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'dashboard','dast'),(8,'dashboard','sast'),(11,'dast_reports','dastscan'),(10,'dast_reports','zapscan'),(9,'message','message'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-08-13 05:00:49.863020'),(2,'auth','0001_initial','2025-08-13 05:01:11.285019'),(3,'admin','0001_initial','2025-08-13 05:01:17.076154'),(4,'admin','0002_logentry_remove_auto_add','2025-08-13 05:01:17.157771'),(5,'admin','0003_logentry_add_action_flag_choices','2025-08-13 05:01:17.299824'),(6,'contenttypes','0002_remove_content_type_name','2025-08-13 05:01:21.747256'),(7,'auth','0002_alter_permission_name_max_length','2025-08-13 05:01:23.988751'),(8,'auth','0003_alter_user_email_max_length','2025-08-13 05:01:24.326365'),(9,'auth','0004_alter_user_username_opts','2025-08-13 05:01:24.471155'),(10,'auth','0005_alter_user_last_login_null','2025-08-13 05:01:26.430019'),(11,'auth','0006_require_contenttypes_0002','2025-08-13 05:01:26.882921'),(12,'auth','0007_alter_validators_add_error_messages','2025-08-13 05:01:27.045174'),(13,'auth','0008_alter_user_username_max_length','2025-08-13 05:01:29.588708'),(14,'auth','0009_alter_user_last_name_max_length','2025-08-13 05:01:32.060751'),(15,'auth','0010_alter_group_name_max_length','2025-08-13 05:01:32.393603'),(16,'auth','0011_update_proxy_permissions','2025-08-13 05:01:32.480410'),(17,'auth','0012_alter_user_first_name_max_length','2025-08-13 05:01:34.699191'),(18,'dashboard','0001_initial','2025-08-13 05:01:35.649236'),(19,'sessions','0001_initial','2025-08-13 05:01:37.503211'),(20,'dashboard','0002_sast','2025-08-13 06:54:39.776012'),(21,'dashboard','0003_sast_link_hasil_scan','2025-08-13 07:14:36.696445'),(22,'message','0001_initial','2025-08-19 07:10:17.428965'),(23,'message','0002_alter_message_service','2025-08-19 07:10:17.433215'),(24,'dast_reports','0001_initial','2025-08-26 07:34:49.012687');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4q4ui6eynrk3rgqnw6d5gbwq1t0fmejx','.eJxVjEEOwiAQRe_C2hCgAwMu3XsGwgxUqoYmpV0Z765NutDtf-_9l4hpW2vcelnilMVZaHH63Sjxo7Qd5Htqt1ny3NZlIrkr8qBdXudcnpfD_TuoqddvzUyjCQGYwDs9FO0zoSFtLYJVrFwqDq1XwWjghL4EGsOABKw8Ahvx_gDZfjdO:1unpET:Nu1ScdHx1Hzpiiml2rmCH1nLW7LHpPHLeV8N-MYGcCI','2025-09-01 02:04:21.652752'),('ddrpgj5y12eluu69z76crkgiuqnnw8h7','.eJxVjEEOwiAQRe_C2hAoFBiX7nsGMnSmUjWQlHZlvLtt0oVu_3vvv0XEbc1xa7zEmcRVaHH53RKOTy4HoAeWe5VjLesyJ3ko8qRNDpX4dTvdv4OMLe91msAEz51lw0lTQgCDHQEkjQ7BBjKu50Bod6aUBh961tqDMw4mZcXnC_VAN7Y:1uqoE8:2W8uxHAaUCYRFblc2IJYn0EK_uTmpqifG6Y2LZVaNFQ','2025-09-09 07:36:20.795750'),('o4igbb8t8intrt4d2751fjk1lnkwhiw2','.eJxVjEEOwiAQRe_C2hAoFBiX7nsGMnSmUjWQlHZlvLtt0oVu_3vvv0XEbc1xa7zEmcRVaHH53RKOTy4HoAeWe5VjLesyJ3ko8qRNDpX4dTvdv4OMLe91msAEz51lw0lTQgCDHQEkjQ7BBjKu50Bod6aUBh961tqDMw4mZcXnC_VAN7Y:1uojcA:08_QPiWlSQuSE7x4Fn-rpqUl-ATX7bEwcO49sUAyJ24','2025-09-03 14:16:34.406429');
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
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `subject` varchar(200) NOT NULL,
  `service` varchar(50) DEFAULT NULL,
  `message` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `priority` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `message_mes_status_03314b_idx` (`status`,`created_at`),
  KEY `message_mes_priorit_ca2ec8_idx` (`priority`,`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message_message`
--

LOCK TABLES `message_message` WRITE;
/*!40000 ALTER TABLE `message_message` DISABLE KEYS */;
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

-- Dump completed on 2025-08-26 17:38:00
