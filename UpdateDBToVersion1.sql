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
	    KEY(basename)) ENGINE = INNODB
	IGNORE
	SELECT substring_index(path, "/", -1) AS basename,
	    left(path, char_length(path)-char_length(substring_index(path, "/", -1))) AS dirname
	    FROM node;
ALTER TABLE node ADD COLUMN pid INT;

UPDATE node 
    INNER JOIN path ON node.path = concat_ws("/", dirname,basename)
    SET node.pid = path.id;
ALTER TABLE node DROP PRIMARY KEY,
    CHANGE pid pid INT PRIMARY KEY NOT NULL,
    ADD FOREIGN KEY pid REFERENCES path(id),
    DROP COLUMN node.path;

UPDATE config SET value='1' where name='version';

COMMIT;
