
UPDATE movies_metadata SET 
genres = REPLACE (genres,'[','');
UPDATE movies_metadata SET 
genres = REPLACE (genres,']','');
UPDATE movies_metadata SET 
genres = REPLACE (genres,'id','');
UPDATE movies_metadata SET 
genres = REPLACE (genres,'name','');
UPDATE movies_metadata SET 
genres = REPLACE (genres,'''','');
UPDATE movies_metadata SET 
genres = REPLACE (genres,':','');
UPDATE movies_metadata SET 
genres = REPLACE (genres,'{','');

CREATE TABLE genres AS
SELECT id,split_part(regexp_split_to_table(genres, '},'), ',', 1) as genre_id,
split_part(regexp_split_to_table(genres, '},'), ',', 2) as genre_name
FROM movies_metadata;

UPDATE genres SET 
genre_name = REPLACE (genre_name,'}','');
UPDATE genres SET 
genre_name = LTRIM (genre_name);
DELETE FROM genres WHERE genre_id = '';

ALTER TABLE genres 
ALTER COLUMN genre_id TYPE INT
USING genre_id::integer;

ALTER TABLE movies_metadata DROP COLUMN genres;
ALTER TABLE genres ADD PRIMARY KEY (id,genre_id);
ALTER TABLE genres ADD CONSTRAINT genre_id_fkey FOREIGN KEY (id) REFERENCES movies_metadata (id);

--TAINIES ANA XRONO
SELECT DATE_PART('year',release_date) AS xronos, COUNT(id) AS arithmos_tainiwn FROM movies_metadata 
WHERE release_date IS NOT NULL
GROUP BY xronos
ORDER BY xronos;

--TAINIES ANA EIDOS
SELECT genre_name AS eidos, COUNT(id) AS tainies
FROM genres
GROUP BY eidos
ORDER BY eidos;

--TAINIES ANA EIDOS KAI XRONO
SELECT genre_name AS eidos, DATE_PART('year',release_date) AS xronos,COUNT(movies_metadata.id) AS arithmos_tainiwn 
FROM movies_metadata,genres 
WHERE release_date IS NOT NULL AND movies_metadata.id = genres.id
GROUP BY eidos,xronos
ORDER BY xronos,eidos;


--MESO RATING ANA XRHSTH
SELECT userid, AVG(rating)::NUMERIC(10,1) AS average_rating
FROM (
    SELECT userid, rating FROM ratings
    UNION ALL
    SELECT userid, rating FROM ratings_small
) AS avgrating
GROUP BY userid
ORDER BY userid;

--MESO RATING ANA EIDOS TAINIAS
SELECT genre_name, AVG(rating)::NUMERIC(10,1) AS average_rating
FROM (
    SELECT movieid,rating FROM ratings
    UNION ALL
    SELECT movieid,rating FROM ratings_small
) AS avgrating,genres
WHERE genres.id = avgrating.movieid
GROUP BY genre_name
ORDER BY genre_name;

-- RATINGS ANA XRHSTH
SELECT userid,COUNT(rating) AS ratings
FROM (
    SELECT userid, rating FROM ratings
    UNION ALL
    SELECT userid, rating FROM ratings_small
) AS avgrating
GROUP BY userid
ORDER BY userid;

--VIEW TABLE 
CREATE TABLE view_table AS
SELECT userid, count(rating) AS numbers, AVG(rating)::NUMERIC(10,1) AS average_rating
FROM (
    SELECT userid, rating FROM ratings
    UNION ALL
    SELECT userid, rating FROM ratings_small
) AS avgrating
GROUP BY userid
ORDER BY userid;

