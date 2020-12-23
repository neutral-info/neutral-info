USE `neutralinfo`;
-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 192.168.0.76    Database: neutralinfo
-- ------------------------------------------------------
-- Server version	8.0.20
--
-- Dumping data for table `channel`
--

/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+08:00' */;

LOCK TABLES `channel` WRITE;
INSERT INTO `channel` VALUES (1,'新聞'),(2,'社群論壇'),(3,'聊天'),(4,'部落格'),(5,'內容農場'),(6,'影音');
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

--
-- Dumping data for table `position`
--

LOCK TABLES `position` WRITE;
INSERT INTO `position` VALUES (1,'民進黨'),(2,'國民黨'),(3,'時力'),(4,'親中'),(5,'泛統派');
UNLOCK TABLES;

--
-- Dumping data for table `producer`
--

LOCK TABLES `producer` WRITE;
INSERT INTO `producer` VALUES ('appledaily.com','蘋果日報','民進黨*0.5|國民黨*0.5|時力*0.2'),('cna.com.tw','中央社','民進黨*0.45|國民黨*0.5|時力*0.4|親中*0.5'),('cnyes.com','鉅亨','民進黨*0.5|國民黨*0.5'),('ctwant.com','王道旺台','民進黨*0.5|國民黨*0.5'),('ettoday.net','ETToday','國民黨*0.6'),('gamer.com.tw','巴哈姆特','民進黨*0.5|國民黨*0.5'),('ltn.com.tw','自由時報','民進黨*0.75|國民黨*0.25|時力*0.6'),('newtalk.tw','新頭殼','民進黨*0.55|國民黨*0.5|華派*0.55'),('udn.com','聯合新聞網','民進黨*0.35|國民黨*0.75|時力*0.4|親中*0.6|泛統派*0.8'),('yahoo.com.tw','YAHOO台灣','國民黨*0.6');
UNLOCK TABLES;
