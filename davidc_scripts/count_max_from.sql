/*
SELECT data->'From'
FROM pydev
GROUP BY data->'From'
HAVING COUNT(data->'From')=
    (SELECT MAX(fromcount) FROM
            (SELECT data->'From', COUNT(data->'From') AS fromcount
                 FROM pydev
                 GROUP BY data->'From') t1)
*/

/* http://stackoverflow.com/questions/5159928/sql-displaying-entries-that-are-the-max-of-a-count */
SELECT data->'From'
FROM pylist
GROUP BY data->'From'
HAVING COUNT(data->'From') = 
    (SELECT MAX(fromcount) FROM
        (SELECT data->'From', COUNT(data->'From') AS fromcount
             FROM pylist
             GROUP BY data->'From') t1);
