CREATE DATABASE  IF NOT EXISTS `neutralinfo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `neutralinfo`;
-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 192.168.0.76    Database: neutralinfo
-- ------------------------------------------------------
-- Server version 8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+08:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `NewsPosition`
--

DROP TABLE IF EXISTS `NewsPosition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `NewsPosition` (
  `id` longtext,
  `position` varchar(31) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `channel`
--

DROP TABLE IF EXISTS `channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `channel` (
  `channel_id` int NOT NULL AUTO_INCREMENT,
  `channel_desc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`channel_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `newsFromApi`
--

DROP TABLE IF EXISTS `newsFromApi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `newsFromApi` (
  `source` text,
  `author` text,
  `title` text,
  `description` text,
  `url` text,
  `urlToImage` text,
  `publishedAt` text,
  `content` text,
  `newsuuid` text,
  `keywords` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `position` (
  `position_id` int NOT NULL AUTO_INCREMENT,
  `position_desc` varchar(100) NOT NULL,
  PRIMARY KEY (`position_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `producer`
--

DROP TABLE IF EXISTS `producer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `producer` (
  `producer_id` varchar(100) NOT NULL,
  `producer_desc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `producer_position` varchar(100) NOT NULL,
  PRIMARY KEY (`producer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ptt`
--

DROP TABLE IF EXISTS `ptt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ptt` (
  `article_id` text,
  `article_title` text,
  `author` text,
  `board` text,
  `content` longtext,
  `date` text,
  `ip` text,
  `messages` longtext,
  `url` text,
  `message_count.all` text,
  `message_count.boo` text,
  `message_count.count` text,
  `message_count.neutral` text,
  `message_count.push` text,
  `triger_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `volume`
--

DROP TABLE IF EXISTS `volume`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `volume` (
  `newsuuid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `volume_now` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `vwNews`
--

DROP TABLE IF EXISTS `vwNews`;
/*!50001 DROP VIEW IF EXISTS `vwNews`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vwNews` AS SELECT 
 1 AS `id`,
 1 AS `pubdate`,
 1 AS `title`,
 1 AS `text`,
 1 AS `keywords`,
 1 AS `channel_id`,
 1 AS `channel_desc`,
 1 AS `author_id`,
 1 AS `author_desc`,
 1 AS `author_position`,
 1 AS `producer_id`,
 1 AS `producer_desc`,
 1 AS `producer_position`,
 1 AS `position`,
 1 AS `volume_now`,
 1 AS `volume_yesterday`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vwNews`
--

/*!50001 DROP VIEW IF EXISTS `vwNews`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vwNews` AS select `news`.`newsuuid` AS `id`,`news`.`publishedAt` AS `pubdate`,`news`.`title` AS `title`,regexp_replace(`news`.`description`,'<.+?>','') AS `text`,`news`.`keywords` AS `keywords`,1 AS `channel_id`,'新聞' AS `channel_desc`,'test' AS `author_id`,'新聞記者' AS `author_desc`,`p`.`producer_position` AS `author_position`,`news`.`source` AS `producer_id`,`p`.`producer_desc` AS `producer_desc`,`p`.`producer_position` AS `producer_position`,`p`.`producer_position` AS `position`,`v`.`volume_now` AS `volume_now`,0 AS `volume_yesterday` from ((`newsFromApi` `news` left join `producer` `p` on((convert(`news`.`source` using utf8) = `p`.`producer_id`))) left join `volume` `v` on((convert(convert(`news`.`newsuuid` using utf8) using utf8) = `v`.`newsuuid`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-23 11:49:42

--
-- Dumping data for table `channel`
--

LOCK TABLES `channel` WRITE;
/*!40000 ALTER TABLE `channel` DISABLE KEYS */;
INSERT INTO `channel` VALUES (1,'新聞'),(2,'社群論壇'),(3,'聊天'),(4,'部落格'),(5,'內容農場'),(6,'影音');
/*!40000 ALTER TABLE `channel` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

--
-- Dumping data for table `position`
--

LOCK TABLES `position` WRITE;
/*!40000 ALTER TABLE `position` DISABLE KEYS */;
INSERT INTO `position` VALUES (1,'民進黨'),(2,'國民黨'),(3,'時力'),(4,'親中'),(5,'泛統派');
/*!40000 ALTER TABLE `position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `producer`
--

LOCK TABLES `producer` WRITE;
/*!40000 ALTER TABLE `producer` DISABLE KEYS */;
INSERT INTO `producer` VALUES ('appledaily.com','蘋果日報','民進黨*0.5|國民黨*0.5|時力*0.2'),('cna.com.tw','中央社','民進黨*0.45|國民黨*0.5|時力*0.4|親中*0.5'),('cnyes.com','鉅亨','民進黨*0.5|國民黨*0.5'),('ctwant.com','王道旺台','民進黨*0.5|國民黨*0.5'),('ettoday.net','ETToday','國民黨*0.6'),('gamer.com.tw','巴哈姆特','民進黨*0.5|國民黨*0.5'),('ltn.com.tw','自由時報','民進黨*0.75|國民黨*0.25|時力*0.6'),('newtalk.tw','新頭殼','民進黨*0.55|國民黨*0.5|華派*0.55'),('udn.com','聯合新聞網','民進黨*0.35|國民黨*0.75|時力*0.4|親中*0.6|泛統派*0.8'),('yahoo.com.tw','YAHOO台灣','國民黨*0.6');
/*!40000 ALTER TABLE `producer` ENABLE KEYS */;
UNLOCK TABLES;
