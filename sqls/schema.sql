USE `neutralinfo`;
-- MySQL dump 10.13  Distrib 8.0.22, for macos10.15 (x86_64)
--
-- Host: 192.168.0.76    Database: neutralinfo
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `NewsPosition`
--

DROP TABLE IF EXISTS `NewsPosition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `NewsPosition` (
  `id` longtext,
  `position` varchar(31) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
-- Table structure for table `fbfanpage`
--

DROP TABLE IF EXISTS `fbfanpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fbfanpage` (
  `sys_id` text,
  `sys_type` text,
  `board_id` text,
  `post_id` text,
  `post_url` text,
  `post_time` text,
  `post_person` text,
  `post_message` text,
  `post_comment_count` bigint DEFAULT NULL,
  `allEmoji` text,
  `goodEmoji` bigint DEFAULT NULL,
  `haEmoji` bigint DEFAULT NULL,
  `waEmoji` bigint DEFAULT NULL,
  `heartEmoji` bigint DEFAULT NULL,
  `angryEmoji` bigint DEFAULT NULL,
  `cryEmoji` bigint DEFAULT NULL,
  `comeonEmoji` bigint DEFAULT NULL,
  `crawler_time` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `fbfanpage_lastpost`
--

DROP TABLE IF EXISTS `fbfanpage_lastpost`;
/*!50001 DROP VIEW IF EXISTS `fbfanpage_lastpost`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `fbfanpage_lastpost` AS SELECT 
 1 AS `sys_id`,
 1 AS `sys_type`,
 1 AS `board_id`,
 1 AS `post_id`,
 1 AS `post_url`,
 1 AS `post_time`,
 1 AS `post_person`,
 1 AS `post_message`,
 1 AS `post_comment_count`,
 1 AS `allEmoji`,
 1 AS `goodEmoji`,
 1 AS `haEmoji`,
 1 AS `waEmoji`,
 1 AS `heartEmoji`,
 1 AS `angryEmoji`,
 1 AS `cryEmoji`,
 1 AS `comeonEmoji`,
 1 AS `crawler_time`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `newsFromApi`
--

DROP TABLE IF EXISTS `newsFromApi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `news_lastpost`
--

DROP TABLE IF EXISTS `news_lastpost`;
/*!50001 DROP VIEW IF EXISTS `news_lastpost`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `news_lastpost` AS SELECT 
 1 AS `source`,
 1 AS `author`,
 1 AS `title`,
 1 AS `description`,
 1 AS `url`,
 1 AS `urlToImage`,
 1 AS `publishedAt`,
 1 AS `content`,
 1 AS `newsuuid`,
 1 AS `keywords`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `position` (
  `position_id` int NOT NULL AUTO_INCREMENT,
  `position_desc` varchar(100) NOT NULL,
  PRIMARY KEY (`position_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `power`
--

DROP TABLE IF EXISTS `power`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `power` (
  `newsuuid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `power_now` double DEFAULT '0',
  `calculate_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `power_last`
--

DROP TABLE IF EXISTS `power_last`;
/*!50001 DROP VIEW IF EXISTS `power_last`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `power_last` AS SELECT 
 1 AS `newsuuid`,
 1 AS `power_now`,
 1 AS `calculate_time`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `producer`
--

DROP TABLE IF EXISTS `producer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producer` (
  `producer_id` varchar(100) NOT NULL,
  `producer_desc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `producer_position` varchar(100) NOT NULL,
  PRIMARY KEY (`producer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ptt`
--

DROP TABLE IF EXISTS `ptt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `ptt_lastpost`
--

DROP TABLE IF EXISTS `ptt_lastpost`;
/*!50001 DROP VIEW IF EXISTS `ptt_lastpost`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `ptt_lastpost` AS SELECT 
 1 AS `article_id`,
 1 AS `article_title`,
 1 AS `author`,
 1 AS `board`,
 1 AS `content`,
 1 AS `date`,
 1 AS `ip`,
 1 AS `messages`,
 1 AS `url`,
 1 AS `message_count.all`,
 1 AS `message_count.boo`,
 1 AS `message_count.count`,
 1 AS `message_count.neutral`,
 1 AS `message_count.push`,
 1 AS `triger_time`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `volume`
--

DROP TABLE IF EXISTS `volume`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `volume` (
  `newsuuid` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `volume_now` double DEFAULT '0',
  `ptt_volume` double NOT NULL DEFAULT '0',
  `fb_fanpage_volume` double NOT NULL DEFAULT '0',
  `fb_goup_volume` double NOT NULL DEFAULT '0',
  `calculate_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `volume_last`
--

DROP TABLE IF EXISTS `volume_last`;
/*!50001 DROP VIEW IF EXISTS `volume_last`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `volume_last` AS SELECT 
 1 AS `newsuuid`,
 1 AS `volume_now`,
 1 AS `ptt_volume`,
 1 AS `fb_fanpage_volume`,
 1 AS `fb_goup_volume`,
 1 AS `calculate_time`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `vwNews`
--

DROP TABLE IF EXISTS `vwNews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vwNews` (
  `id` text,
  `pubdate` text,
  `title` text,
  `text` longtext,
  `keywords` text,
  `channel_id` int NOT NULL DEFAULT '0',
  `channel_desc` varchar(2) NOT NULL DEFAULT '',
  `author_id` varchar(4) NOT NULL DEFAULT '',
  `author_desc` varchar(4) NOT NULL DEFAULT '',
  `author_position` varchar(100),
  `producer_id` text,
  `producer_desc` varchar(100) DEFAULT NULL,
  `producer_position` varchar(100),
  `position` varchar(100),
  `volume_now` double NOT NULL DEFAULT '0',
  `volume_yesterday` int NOT NULL DEFAULT '0',
  `power_now` double NOT NULL DEFAULT '0',
  `url` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `vwNews_view`
--

DROP TABLE IF EXISTS `vwNews_view`;
/*!50001 DROP VIEW IF EXISTS `vwNews_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vwNews_view` AS SELECT 
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
 1 AS `volume_yesterday`,
 1 AS `power_now`,
 1 AS `url`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'neutralinfo'
--

--
-- Final view structure for view `fbfanpage_lastpost`
--

/*!50001 DROP VIEW IF EXISTS `fbfanpage_lastpost`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `fbfanpage_lastpost` AS select `f2`.`sys_id` AS `sys_id`,`f2`.`sys_type` AS `sys_type`,`f2`.`board_id` AS `board_id`,`f2`.`post_id` AS `post_id`,`f2`.`post_url` AS `post_url`,`f2`.`post_time` AS `post_time`,`f2`.`post_person` AS `post_person`,`f2`.`post_message` AS `post_message`,`f2`.`post_comment_count` AS `post_comment_count`,`f2`.`allEmoji` AS `allEmoji`,`f2`.`goodEmoji` AS `goodEmoji`,`f2`.`haEmoji` AS `haEmoji`,`f2`.`waEmoji` AS `waEmoji`,`f2`.`heartEmoji` AS `heartEmoji`,`f2`.`angryEmoji` AS `angryEmoji`,`f2`.`cryEmoji` AS `cryEmoji`,`f2`.`comeonEmoji` AS `comeonEmoji`,`f2`.`crawler_time` AS `crawler_time` from `fbfanpage` `f2` where concat(`f2`.`sys_id`,`f2`.`crawler_time`) in (select concat(`tbl_id_with_time`.`a`,`tbl_id_with_time`.`b`) AS `id_with_time` from (select `f`.`sys_id` AS `a`,max(`f`.`crawler_time`) AS `b` from `fbfanpage` `f` group by `f`.`sys_id`) `tbl_id_with_time`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `news_lastpost`
--

/*!50001 DROP VIEW IF EXISTS `news_lastpost`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `news_lastpost` AS select `nfa2`.`source` AS `source`,`nfa2`.`author` AS `author`,`nfa2`.`title` AS `title`,`nfa2`.`description` AS `description`,`nfa2`.`url` AS `url`,`nfa2`.`urlToImage` AS `urlToImage`,`nfa2`.`publishedAt` AS `publishedAt`,`nfa2`.`content` AS `content`,`nfa2`.`newsuuid` AS `newsuuid`,`nfa2`.`keywords` AS `keywords` from `newsFromApi` `nfa2` where concat(`nfa2`.`url`,`nfa2`.`newsuuid`) in (select concat(`tbl_url_with_uuid`.`a`,`tbl_url_with_uuid`.`b`) AS `url_with_uuid` from (select `nfa`.`url` AS `a`,max(`nfa`.`newsuuid`) AS `b` from `newsFromApi` `nfa` where ((str_to_date(`nfa`.`publishedAt`,'%Y-%m-%dT%TZ') >= (now() - interval 14 day)) and (str_to_date(`nfa`.`publishedAt`,'%Y-%m-%dT%TZ') < now())) group by `nfa`.`url`) `tbl_url_with_uuid`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `power_last`
--

/*!50001 DROP VIEW IF EXISTS `power_last`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `power_last` AS select `v2`.`newsuuid` AS `newsuuid`,`v2`.`power_now` AS `power_now`,`v2`.`calculate_time` AS `calculate_time` from `power` `v2` where concat(`v2`.`newsuuid`,`v2`.`calculate_time`) in (select concat(`tbl_id_with_time`.`a`,`tbl_id_with_time`.`b`) AS `id_with_time` from (select `v`.`newsuuid` AS `a`,max(`v`.`calculate_time`) AS `b` from `power` `v` group by `v`.`newsuuid`) `tbl_id_with_time`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `ptt_lastpost`
--

/*!50001 DROP VIEW IF EXISTS `ptt_lastpost`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `ptt_lastpost` AS select `p`.`article_id` AS `article_id`,`p`.`article_title` AS `article_title`,`p`.`author` AS `author`,`p`.`board` AS `board`,`p`.`content` AS `content`,`p`.`date` AS `date`,`p`.`ip` AS `ip`,`p`.`messages` AS `messages`,`p`.`url` AS `url`,`p`.`message_count.all` AS `message_count.all`,`p`.`message_count.boo` AS `message_count.boo`,`p`.`message_count.count` AS `message_count.count`,`p`.`message_count.neutral` AS `message_count.neutral`,`p`.`message_count.push` AS `message_count.push`,`p`.`triger_time` AS `triger_time` from `ptt` `p` where concat(`p`.`article_id`,`p`.`triger_time`) in (select concat(`tbl_id_with_time`.`a`,`tbl_id_with_time`.`b`) AS `id_with_time` from (select `p1`.`article_id` AS `a`,max(`p1`.`triger_time`) AS `b` from `ptt` `p1` group by `p1`.`article_id`) `tbl_id_with_time`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `volume_last`
--

/*!50001 DROP VIEW IF EXISTS `volume_last`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `volume_last` AS select `v2`.`newsuuid` AS `newsuuid`,`v2`.`volume_now` AS `volume_now`,`v2`.`ptt_volume` AS `ptt_volume`,`v2`.`fb_fanpage_volume` AS `fb_fanpage_volume`,`v2`.`fb_goup_volume` AS `fb_goup_volume`,`v2`.`calculate_time` AS `calculate_time` from `volume` `v2` where concat(`v2`.`newsuuid`,`v2`.`calculate_time`) in (select concat(`tbl_id_with_time`.`a`,`tbl_id_with_time`.`b`) AS `id_with_time` from (select `v`.`newsuuid` AS `a`,max(`v`.`calculate_time`) AS `b` from `volume` `v` group by `v`.`newsuuid`) `tbl_id_with_time`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vwNews_view`
--

/*!50001 DROP VIEW IF EXISTS `vwNews_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vwNews_view` AS select `news`.`newsuuid` AS `id`,`news`.`publishedAt` AS `pubdate`,`news`.`title` AS `title`,regexp_replace(`news`.`description`,'<.+?>','') AS `text`,`news`.`keywords` AS `keywords`,1 AS `channel_id`,'新聞' AS `channel_desc`,'test' AS `author_id`,'新聞記者' AS `author_desc`,`p`.`producer_position` AS `author_position`,`news`.`source` AS `producer_id`,`p`.`producer_desc` AS `producer_desc`,`p`.`producer_position` AS `producer_position`,`p`.`producer_position` AS `position`,ifnull(`v`.`volume_now`,0) AS `volume_now`,0 AS `volume_yesterday`,floor((ifnull(`b`.`power_now`,0) * 1000)) AS `power_now`,`news`.`url` AS `url` from (((`news_lastpost` `news` left join `producer` `p` on((convert(convert(`news`.`source` using utf8) using utf8mb4) = `p`.`producer_id`))) left join `volume_last` `v` on((convert(convert(convert(`news`.`newsuuid` using utf8) using utf8) using utf8mb4) = `v`.`newsuuid`))) left join `power_last` `b` on((convert(convert(convert(`news`.`newsuuid` using utf8) using utf8) using utf8mb4) = `b`.`newsuuid`))) */;
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

-- Dump completed on 2021-03-17 22:13:32
