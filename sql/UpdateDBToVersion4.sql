--
-- Version 4 fix a bug in the DB where 
-- path.dirname sometime have a trailing '/' 
-- and sometime not.
--
-- The correct behaviour is not to have terminal '/'
--
UPDATE node 
    JOIN path AS a ON node.pid = a.id 
    JOIN path AS b ON a.dirname = concat(b.dirname,'/') 
			AND a.basename = b.basename
    SET node.pid = b.id;
 
UPDATE IGNORE path SET dirname = substr(dirname, 1, length(dirname)-1)
	WHERE dirname LIKE '%/';

DELETE FROM path WHERE dirname LIKE '%/';

UPDATE config SET value = '4' WHERE name = 'version';

COMMIT;
