--
-- Session
--
CREATE TABLE `session` (
  `date` datetime NOT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB;

--
-- A file identified by the md5 hash of the content
--
CREATE TABLE `file` (
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
CREATE TABLE `path` (
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
CREATE TABLE `node` (
  `hash` char(32) NOT NULL,
  `date` datetime NOT NULL,
  `owner` char(20) NOT NULL,
  `pid` int(11) NOT NULL,
  `atime` DATETIME NOT NULL,
  `mtime` DATETIME NOT NULL,
  `ctime` DATETIME NOT NULL,
  PRIMARY KEY (`date`,`pid`),
  KEY `owner` (`owner`),
  KEY `hash` (`hash`),
  KEY `pid` (`pid`),
  CONSTRAINT `node_ibfk_1` FOREIGN KEY (`hash`) REFERENCES `file` (`hash`),
  CONSTRAINT `node_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `path` (`id`)
) ENGINE=InnoDB;

--
-- Versioning & meta informations
--
CREATE TABLE `config` (
  `name` char(64) NOT NULL DEFAULT '',
  `value` char(255) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB;
INSERT INTO config(name,value) 
    VALUES ("version","2");

COMMIT;
-- end
