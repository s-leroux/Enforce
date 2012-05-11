--
-- Version 2 store {a,c,m}time for each node
--
ALTER TABLE node
	ADD (atime DATETIME NOT NULL,
	     mtime DATETIME NOT NULL,
	     ctime DATETIME NOT NULL);

CREATE TABLE session (date DATETIME NOT NULL,
			PRIMARY KEY(date),
			FOREIGN KEY (date) REFERENCES node(date))
		    ENGINE=InnoDB;
INSERT INTO session(date) SELECT DISTINCT date FROM node;

UPDATE config SET value = '2' WHERE name = 'version';

COMMIT;
