-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: Monitor
-- ------------------------------------------------------
-- Server version	5.5.44-0+deb8u1

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
-- Table structure for table `Logs`
--

DROP TABLE IF EXISTS `Logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Logs` (
  `lID` int(11) NOT NULL AUTO_INCREMENT,
  `sID` int(11) NOT NULL,
  `TimeStamp` varchar(45) NOT NULL,
  `r1` varchar(45) DEFAULT NULL,
  `r2` varchar(45) DEFAULT NULL,
  `r3` varchar(45) DEFAULT NULL,
  `r4` varchar(45) DEFAULT NULL,
  `r5` varchar(100) DEFAULT NULL,
  `r6` varchar(45) DEFAULT NULL,
  `r7` varchar(45) DEFAULT NULL,
  `r8` varchar(511) DEFAULT NULL,
  PRIMARY KEY (`lID`),
  KEY `ServerID_idx` (`sID`),
  CONSTRAINT `ServerID` FOREIGN KEY (`sID`) REFERENCES `Server` (`sID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `Server`
--

DROP TABLE IF EXISTS `Server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Server` (
  `sID` int(11) NOT NULL AUTO_INCREMENT,
  `IPAdres` varchar(45) NOT NULL,
  `IPPort` varchar(5) NOT NULL,
  `MACAdres` varchar(45) NOT NULL,
  `OperatingSystem` varchar(45) NOT NULL,
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`sID`),
  UNIQUE KEY `IPAdres_UNIQUE` (`IPAdres`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `error`
--

DROP TABLE IF EXISTS `error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `error` (
  `eID` int(11) NOT NULL AUTO_INCREMENT,
  `sID` int(11) NOT NULL,
  `TimeStamp` varchar(45) NOT NULL,
  `level` varchar(45) NOT NULL,
  `error` varchar(500) NOT NULL,
  PRIMARY KEY (`eID`),
  KEY `eID-sID_idx` (`sID`),
  CONSTRAINT `eID-sID` FOREIGN KEY (`sID`) REFERENCES `Server` (`sID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-01-10 11:45:07
