-- To reduce space on disk, the DB version 1 add
-- a new table for file names. Those are splitted in (path, name)
-- in order to speedup retrieving of a file by its name.
-- 
-- The new table is named 'path' and the previous 'path' table is
-- now renamed 'node'

RENAME TABLE path TO node;
CREATE TABLE path (
	    id INT NOT NULL AUTO_INCREMENT,
	    PRIMARY KEY(id),
	    UNIQUE(dirname,basename),
	    KEY(fullname),
	    KEY(basename)) ENGINE = INNODB
	IGNORE
	SELECT path AS fullname, substring_index(path, "/", -1) AS basename,
	    left(path, char_length(path)-char_length(substring_index(path, "/", -1))) AS dirname
	    FROM node;
ALTER TABLE node ADD COLUMN pid INT;

UPDATE node 
    INNER JOIN path ON node.path = fullname
    SET node.pid = path.id;
ALTER TABLE node DROP PRIMARY KEY,
    CHANGE pid pid INT NOT NULL,
    ADD PRIMARY KEY (date, pid),
    ADD FOREIGN KEY (pid) REFERENCES path(id),
    DROP COLUMN node.path;
ALTER TABLE path DROP COLUMN fullname;

ALTER TABLE file CHANGE status status enum('?','X','OK','COPYRIGHT')
				    NOT NULL DEFAULT '?';

CREATE TABLE IF NOT EXISTS `config` (
  `name` char(64) NOT NULL DEFAULT '',
  `value` char(255) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB;

UPDATE config SET value='1' where name='version';

COMMIT;
