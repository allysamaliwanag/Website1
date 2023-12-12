-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.22-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.0.0.6468
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
CREATE DATABASE IF NOT EXISTS `rfid` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `rfid`;

-- Dumping structure for table rfid.admin
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password` varchar(120) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'admin',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table rfid.admin: ~1 rows (approximately)
DELETE FROM `admin`;
INSERT INTO `admin` (`id`, `username`, `password`, `role`) VALUES
	(1, 'admin', 'password', 'admin');

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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table rfid.attendance_records: ~6 rows (approximately)
DELETE FROM `attendance_records`;
INSERT INTO `attendance_records` (`id`, `studentID`, `name`, `email`, `grade_level`, `date`, `status`, `section`) VALUES
	(1, '20-04868', 'Johndrey Jester B. Orense', 'johndreyjester@gmail.com', '', '2023-11-06', 'Present', ''),
	(2, '20-04868', 'Johndrey Jester B. Orense', 'johndreyjester@gmail.com', '', '2023-11-07', 'Absent', ''),
	(3, '20-04868', 'Johndrey Jester B. Orense', 'johndreyjester@gmail.com', '', '2023-11-08', 'Present', ''),
	(4, '20-04864', 'Johndrey Jester B. Orense', 'johndreyjester@gmail.com', '', '2023-11-08', 'Present', ''),
	(5, '20-04868', 'Johndrey Jester B. Orense', 'johndreyjester@gmail.com', 'Grade 11', '2023-12-03', 'Present', 'TVL'),
	(6, '20-04868', 'Johndrey Jester B. Orense', 'johndreyjester@gmail.com', 'Grade 11', '2023-12-03', 'Present', 'TVL');

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table rfid.logs: ~3 rows (approximately)
DELETE FROM `logs`;
INSERT INTO `logs` (`id`, `nfcTag`, `name`, `role`, `timeIn`, `timeOut`, `status`) VALUES
	(1, '0011706940', 'Johndrey Jester B. Orense', 'student', '2023-11-06 12:34:12', '2023-11-06 13:10:33', 'Possible Cutting Classes'),
	(2, '0011706940', 'Johndrey Jester B. Orense', 'student', '2023-12-03 07:13:56', '2023-12-03 10:19:02', 'Possible Cutting Classes'),
	(3, '0011706940', 'Johndrey Jester B. Orense', 'student', '2023-12-03 10:16:55', '2023-12-03 10:19:02', 'Possible Cutting Classes');

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
  PRIMARY KEY (`reportID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table rfid.reports: ~3 rows (approximately)
DELETE FROM `reports`;
INSERT INTO `reports` (`reportID`, `name`, `section`, `timestamp`, `description`, `role`, `status`, `grade_level`) VALUES
	(1, 'Johndrey Jester B. Orense', 'student_section', '2023-11-06 13:10:33', 'Possible Cutting Classes', 'student', 'Resolved', 'student_grade_level'),
	(2, 'Johndrey Jester B. Orense', 'student_section', '2023-12-03 07:16:13', 'Possible Cutting Classes', 'student', 'Unresolved', 'student_grade_level'),
	(3, 'Johndrey Jester B. Orense', 'student_section', '2023-12-03 10:19:02', 'Possible Cutting Classes', 'student', 'Possible Cutting Classes', 'student_grade_level');

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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table rfid.student: ~8 rows (approximately)
DELETE FROM `student`;
INSERT INTO `student` (`id`, `studentID`, `username`, `password`, `name`, `email`, `image`, `nfcTag`, `role`, `attendance`, `section`, `grade_level`) VALUES
	(1, '20-04868', 'Johndrey', '$2b$12$qH/QU2mp9y6hdaCjK9gCMuLu0F.EYwFcSry3C04cnX0mljKGsnyAa', 'Johndrey Jester B. Orense', 'johndreyjester@gmail.com', _binary 0x737464706963735c313638323732343134393936372e6a7067, '0011706940', 'student', 'Absent', 'TVL', 'Grade 11'),
	(4, '20-0982', 'Guini', '$2b$12$CLPvzd.T/5LSea5v6mE8A.82/8GjeJMEYyZ7UpvwHqsSlJQLV6trG', 'guini mae', 'guini123@gmail.comm', _binary 0x737464706963735c313639363731383839323439382e6a7067, NULL, 'student', 'Absent', NULL, NULL),
	(5, '20-0631', 'Jollibee', '$2b$12$zbq/78lQBdBnNEREHlk7E.y0WFW7LteyT4xWLZnHymxwiHdYyWhou', 'jollihotdog', 'jollibee123@gmail.com', _binary 0x737464706963735c313638323732343134393936372e6a7067, NULL, 'student', 'Absent', NULL, NULL),
	(6, '21-7681', 'Heart', '$2b$12$.NGodzk5w2RYJfDGePeGDOx9wg3oZelR46mMDXfyWq.wV51/FOwma', 'heart', 'heart123123@gmail.com', _binary 0x737464706963735c313638323732343134393936372e6a7067, NULL, 'student', 'Absent', NULL, NULL),
	(8, '22-2123', 'Tammy', '$2b$12$em74DerNrHDlitYp1Xu7qOw8RKZdSJKdIw8xvyGS6d57Z2yvs5raq', 'Tammy T.', 'rachelTummy@gmail.com', _binary 0x737464706963735c72656365697665645f3537373137393736343435313533302e6a706567, NULL, 'student', 'Absent', NULL, NULL),
	(11, '20-04862', 'rachel', '$2b$12$eNrqEffXwvlljSX2Hi2DP.HGvG3w9HKjXq5qIHSxM6x1GhVqMdySS', 'Rachel B. haikyu', 'Rachb1123@gmail.com', _binary 0x737464706963735c313638323732343134393936372e6a7067, NULL, 'student', 'Absent', NULL, NULL),
	(12, '22-15306', 'Michael', '$2b$12$6nLfdqnz3L2PROWo5cdZQOgXQVubHpPnOw3psKmO80lUDg0pKFk5C', 'Michael M. Prezto', 'Michael342@gmail.com', _binary 0x737464706963735c313638323732343134393936372e6a7067, NULL, 'student', 'Absent', NULL, NULL),
	(13, '20-04546', 'Allysa', '$2b$12$LNnGQK5W4osPqltj/wCoNOt8Q6doMowvC0l7aVBqBxtMJNPqdT30S', 'Allysa Magpantay', 'Ammsmm@gmail.com', _binary 0x737464706963735c313638323732343439393234382e6a7067, NULL, 'student', 'Absent', NULL, NULL);

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
  `image` blob NOT NULL,
  `attendance` varchar(50) DEFAULT 'Absent',
  `section` varchar(50) DEFAULT NULL,
  `grade_level` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`teacherID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table rfid.teacher: ~3 rows (approximately)
DELETE FROM `teacher`;
INSERT INTO `teacher` (`id`, `teacherID`, `username`, `password`, `name`, `email`, `nfcTag`, `role`, `image`, `attendance`, `section`, `grade_level`) VALUES
	(1, '20-11111', 'Willie', 'winwin', 'Willie D. Poo', 'Williedpoo@gmail.com', NULL, 'teacher', _binary 0x737464706963735c313638323732343134393936372e6a7067, 'Absent', 'TVL', NULL),
	(2, '20-11112', 'Marvels', '333333', 'Marvels H.Pew', 'marvelus12@gmail.com', NULL, 'teacher', _binary 0x737464706963735c313638323732343439393234382e6a7067, 'Absent', 'ABM', NULL),
	(3, '20-1114', 'Uri', 'arfarfarf', 'Uri D. Buri', 'UriBuri.D1@gmail.com', NULL, 'teacher', _binary 0x737464706963735c313638323732343235363732352e6a7067, 'Absent', 'Stem', NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
