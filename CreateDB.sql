--
-- A file identified by the md5 hash of the content
--
CREATE TABLE IF NOT EXISTS file (
	hash CHAR(32) NOT NULL,
	mimetype CHAR(64) NOT NULL,
	size INT(10),
	status ENUM('?', 'X', 'OK','COPYRIGHT') DEFAULT '?',
	PRIMARY KEY(hash),
	INDEX(mimetype)
    ) ENGINE INNODB;

--
-- A path entry
--
CREATE TABLE IF NOT EXISTS path (
	hash CHAR(32) NOT NULL,
	date DATETIME NOT NULL,
	path VARCHAR(255) NOT NULL,
	owner CHAR(20) NOT NULL,
	PRIMARY KEY(date, path),
	INDEX(owner),
	FOREIGN KEY (hash) REFERENCES file(hash)
    ) ENGINE INNODB;

--
-- Versioning & meta informations
--
CREATE TABLE IF NOT EXISTS config (
	name CHAR(64),
	value CHAR(255),
	PRIMARY KEY(name)) ENGINE INNODB;
INSERT IGNORE INTO config(name,value) 
    VALUES ("version","0");

COMMIT;
-- end
