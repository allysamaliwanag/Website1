-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.32-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for rfid
CREATE DATABASE IF NOT EXISTS `rfid` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `rfid`;

-- Dumping structure for table rfid.admin
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password` varchar(120) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'admin',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table rfid.attendance_records
CREATE TABLE IF NOT EXISTS `attendance_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `studentID` varchar(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL DEFAULT '',
  `grade_level` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `status` enum('Present','Absent') NOT NULL,
  `section` varchar(50) DEFAULT NULL,
  `log_stat` enum('Timed In','Timed Out') DEFAULT 'Timed Out',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table rfid.logs
CREATE TABLE IF NOT EXISTS `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nfcTag` varchar(50) DEFAULT NULL,
  `name` varchar(50) NOT NULL DEFAULT '',
  `role` varchar(50) DEFAULT NULL,
  `timeIn` datetime DEFAULT NULL,
  `timeOut` datetime DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table rfid.reports
CREATE TABLE IF NOT EXISTS `reports` (
  `reportID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `section` varchar(50) NOT NULL DEFAULT '',
  `timestamp` datetime NOT NULL,
  `description` text NOT NULL,
  `role` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Unresolved',
  `grade_level` varchar(50) NOT NULL,
  `nfcTag` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`reportID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table rfid.student
CREATE TABLE IF NOT EXISTS `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `studentID` varchar(50) DEFAULT NULL,
  `username` varchar(80) NOT NULL,
  `password` varchar(120) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `image` blob DEFAULT NULL,
  `nfcTag` varchar(50) DEFAULT NULL,
  `role` varchar(50) NOT NULL DEFAULT 'student',
  `attendance` varchar(50) DEFAULT NULL,
  `section` varchar(50) DEFAULT NULL,
  `grade_level` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`studentID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table rfid.teacher
CREATE TABLE IF NOT EXISTS `teacher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacherID` varchar(80) NOT NULL,
  `username` varchar(80) NOT NULL,
  `password` varchar(120) NOT NULL,
  `name` varchar(50) NOT NULL DEFAULT 'teacher',
  `email` varchar(50) NOT NULL DEFAULT 'teacher',
  `nfcTag` varchar(50) DEFAULT NULL,
  `role` varchar(50) NOT NULL DEFAULT 'teacher',
  `image` blob DEFAULT NULL,
  `attendance` varchar(50) DEFAULT 'Absent',
  `section` varchar(50) DEFAULT NULL,
  `grade_level` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`teacherID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
