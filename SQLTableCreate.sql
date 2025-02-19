# This file contains all the database objects creation scripts that can be run on a mysql database server at set up
# Author: Shaivi Nandi, Class 12 A, Meridian School Madhapur
# Copyright: All rights reserved

CREATE DATABASE `computerinstitute` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `course` (
  `courseid` varchar(10) NOT NULL,
  `coursedescription` varchar(200) DEFAULT NULL,
  `coursedurationdays` int DEFAULT NULL,
  `coursefees` decimal(10,2) DEFAULT NULL,
  `Prerequisites` varchar(100) DEFAULT 'NONE',
  PRIMARY KEY (`courseid`),
  UNIQUE KEY `courseid_UNIQUE` (`courseid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `faculty` (
  `facultyid` int NOT NULL AUTO_INCREMENT,
  `facultyname` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`facultyid`),
  UNIQUE KEY `facultyid_UNIQUE` (`facultyid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `student` (
  `studentid` int NOT NULL AUTO_INCREMENT,
  `studentfirstname` varchar(100) DEFAULT NULL,
  `studentsurname` varchar(100) DEFAULT NULL,
  `studentmiddlename` varchar(100) DEFAULT NULL,
  `studentisactive` tinyint DEFAULT '1',
  `studentdob` datetime DEFAULT NULL,
  `studentaddress` text,
  `studentphone1` varchar(10) DEFAULT NULL,
  `studentphone2` varchar(10) DEFAULT NULL,
  `studentgender` varchar(1) DEFAULT 'F',
  PRIMARY KEY (`studentid`),
  UNIQUE KEY `studentid_UNIQUE` (`studentid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `cohort` (
  `cohortid` int NOT NULL AUTO_INCREMENT,
  `cohortstartdate` date DEFAULT NULL,
  `cohortismondayclass` tinyint DEFAULT '1',
  `cohortistuesdayclass` tinyint DEFAULT '1',
  `cohortiswednesdayclass` tinyint DEFAULT '1',
  `cohortisthursdayclass` tinyint DEFAULT '1',
  `cohortisfridayclass` tinyint DEFAULT '1',
  `cohortissaturdayclass` tinyint DEFAULT '0',
  `cohortissundayclass` tinyint DEFAULT '0',
  `cohortclassstarttime` time DEFAULT NULL,
  `cohortclassduration` smallint DEFAULT '1',
  `cohortcourseid` varchar(10) DEFAULT NULL,
  `cohortfacultyid` int DEFAULT NULL,
  `cohortenddate` date DEFAULT NULL,
  `cohortisactive` tinyint DEFAULT '1',
  PRIMARY KEY (`cohortid`),
  UNIQUE KEY `cohortid_UNIQUE` (`cohortid`),
  KEY `cohortcourseid_idx` (`cohortcourseid`),
  KEY `chortfacultyid_fk_idx` (`cohortfacultyid`),
  CONSTRAINT `chortfacultyid_fk` FOREIGN KEY (`cohortfacultyid`) REFERENCES `faculty` (`facultyid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cohortcourseid_fk` FOREIGN KEY (`cohortcourseid`) REFERENCES `course` (`courseid`) ON DELETE SET RESTRICT UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `studentcohort` (
  `studentid` int NOT NULL,
  `cohortid` int NOT NULL,
  PRIMARY KEY (`studentid`,`cohortid`),
  KEY `studentcohort_cohortid_fk_idx` (`cohortid`,`studentid`),
  CONSTRAINT `studentcohort_cohortid_fk` FOREIGN KEY (`cohortid`) REFERENCES `cohort` (`cohortid`),
  CONSTRAINT `studentcohort_studentid_fk` FOREIGN KEY (`studentid`) REFERENCES `student` (`studentid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `studentcoursecohortfaculty`
AS select `student`.`studentfirstname` AS `studentfirstname`,
`student`.`studentmiddlename` AS `studentmiddlename`,
`student`.`studentsurname` AS `studentsurname`,
`cohort`.`cohortstartdate` AS `cohortstartdate`,
`course`.`coursedescription` AS `coursedescription`,
`course`.`coursedurationdays` AS `coursedurationdays`,
`faculty`.`facultyname` AS `facultyname`
from ((((`student` join `cohort`) join `course`) join `faculty`) join `studentcohort`)
where ((`student`.`studentid` = `studentcohort`.`studentid`) and
(`studentcohort`.`cohortid` = `cohort`.`cohortid`) and
(`cohort`.`cohortfacultyid` = `faculty`.`facultyid`) and
(`cohort`.`cohortcourseid` = `course`.`courseid`));

CREATE ALGORITHM = UNDEFINED DEFINER = `root`@`localhost` SQL SECURITY DEFINER
VIEW `coursecohort` AS
SELECT
`cohort`.`cohortid` AS `cohortid`,
`cohort`.`cohortstartdate` AS `cohortstartdate`,
`course`.`courseid` AS `courseid`,
`course`.`coursedescription` AS `coursedescription`,
`course`.`coursedurationdays` AS `coursedurationdays`,
`faculty`.`facultyname` AS `facultyname`
FROM
((`cohort`
JOIN `course`)
JOIN `faculty`)
WHERE
((`cohort`.`cohortfacultyid` = `faculty`.`facultyid`)
AND (`cohort`.`cohortcourseid` = `course`.`courseid`)
AND (`cohort`.`cohortisactive` = 1))

