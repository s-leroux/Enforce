--
-- A file identified by the md5 hash of the content
--
CREATE TABLE IF NOT EXISTS `file` (
  `hash` char(32) NOT NULL,
  `mimetype` char(64) NOT NULL,
  `size` int(10) DEFAULT NULL,
  `status` enum('?','X','OK','COPYRIGHT') NOT NULL DEFAULT '?',
  PRIMARY KEY (`hash`),
  KEY `mimetype` (`mimetype`)
) ENGINE=InnoDB;

--
-- A path entry
--
CREATE TABLE IF NOT EXISTS `path` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basename` varchar(255) NOT NULL DEFAULT '',
  `dirname` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dirname` (`dirname`,`basename`),
  KEY `basename` (`basename`)
) ENGINE=InnoDB;

--
-- A node
--
CREATE TABLE IF NOT EXISTS `node` (
  `hash` char(32) NOT NULL,
  `date` datetime NOT NULL,
  `owner` char(20) NOT NULL,
  `pid` int(11) NOT NULL,
  PRIMARY KEY (`date`,`pid`),
  KEY `owner` (`owner`),
  KEY `hash` (`hash`),
  KEY `pid` (`pid`),
  CONSTRAINT `node_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `path` (`id`),
  CONSTRAINT `node_ibfk_1` FOREIGN KEY (`hash`) REFERENCES `file` (`hash`)
) ENGINE=InnoDB;

--
-- Versioning & meta informations
--
CREATE TABLE IF NOT EXISTS config (
	name CHAR(64),
	value CHAR(255),
	PRIMARY KEY(name)) ENGINE INNODB;
INSERT IGNORE INTO config(name,value) 
    VALUES ("version","1");

COMMIT;
-- end
