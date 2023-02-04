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
SELECT userid, AVG(rating)::numeric(10,1) AS average_rating
FROM (
    SELECT userid, rating FROM ratings
    UNION ALL
    SELECT userid, rating FROM ratings_small
) AS avgrating
GROUP BY userid
ORDER BY userid;

--MESO RATING ANA EIDOS TAINIAS
SELECT genre_name, AVG(rating)::numeric(10,1) AS average_rating
FROM (
    SELECT movieid,rating FROM ratings
    UNION ALL
    SELECT movieid,rating FROM ratings_small
) AS avgrating,genres
WHERE genres.id = avgrating.movieid
GROUP BY genre_name
ORDER BY genre_name;

-- RATINGS ANA XRHSTH
SELECT userid,count(rating) as ratings
FROM (
    SELECT userid, rating FROM ratings
    UNION ALL
    SELECT userid, rating FROM ratings_small
) AS avgrating
GROUP BY userid
ORDER BY userid;