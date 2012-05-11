--
-- Version 3 add the timestamp for file status change
--
ALTER TABLE file
	ADD (stime DATETIME NOT NULL);

UPDATE file 
JOIN (select min(date) AS M,hash FROM node JOIN file USING(hash) GROUP BY hash ) AS T 
USING(hash) SET file.stime = M; 

UPDATE config SET value = '3' WHERE name = 'version';

COMMIT;
