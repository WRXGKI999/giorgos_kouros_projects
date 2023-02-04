import psycopg2
import matplotlib.pyplot as mp

host = "tsirigo.postgres.database.azure.com"
dbname = "MOVIES"
user = "ananas@tsirigo"
password = "@n@n@$2021"
sslmode = "require"

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()

# cursor.execute("SELECT DATE_PART('year',release_date) AS xronos, COUNT(id) AS arithmos_tainiwn FROM movies_metadata \
# WHERE release_date IS NOT NULL \
# GROUP BY xronos \
# ORDER BY xronos; ")
#q1 = cursor.fetchall()
#for i in q1:
#    x = i[0]
#    y = i[1]
#    mp.scatter(x, y, s = 2)
 
# cursor.execute("SELECT genre_name AS eidos, COUNT(id) AS tainies \
# FROM genres \
# GROUP BY eidos \
# ORDER BY eidos;")
# q2 = cursor.fetchall()
# for i in q2:
    # x = i[0]
    # y = i[1]
    # mp.scatter(y, x, s = 2)

# cursor.execute("SELECT genre_name AS eidos, DATE_PART('year',release_date) AS xronos,COUNT(movies_metadata.id) AS arithmos_tainiwn \
# FROM movies_metadata,genres \
# WHERE release_date IS NOT NULL AND movies_metadata.id = genres.id \
# GROUP BY eidos,xronos \
# ORDER BY xronos,eidos;")
# q3 = cursor.fetchall()

# fig = mp.figure()
# figur = fig.add_subplot(projection='3d')
# print(q3)
# for i in q3:
    # x = i[0]
    # y = i[1]
    # z = i[2]
    # figur.scatter(z, y, x, s = 2)
    
cursor.execute("SELECT userid, AVG(rating)::numeric(10,1) AS average_rating \
    FROM ( \
    SELECT userid, rating FROM ratings \
    UNION ALL \
    SELECT userid, rating FROM ratings_small \
) AS avgrating \
GROUP BY userid \
ORDER BY userid;")
q4 = cursor.fetchall()

for i in q4:
    x = i[0]
    y = i[1]
    mp.scatter(x, y, s = 2)
    
# EDW EXEIS MEINEI
# cursor.execute("SELECT genre_name, AVG(rating)::numeric(10,1) AS average_rating \
    # FROM ( \
    # SELECT movieid,rating FROM ratings \
    # UNION ALL \
    # SELECT movieid,rating FROM ratings_small \
# ) AS avgrating,genres \
# WHERE genres.id = avgrating.movieid \
# GROUP BY genre_name \
# ORDER BY genre_name; ")
# q5 = cursor.fetchall()

# for i in q5:
    # x = i[0]
    # y = i[1]
    # mp.scatter(x, y, s = 2)

# cursor.execute("SELECT userid,count(rating) as ratings \
    # FROM (  \
    # SELECT userid, rating FROM ratings \
    # UNION ALL \
    # SELECT userid, rating FROM ratings_small \
# ) AS avgrating \
# GROUP BY userid \
# ORDER BY userid; \ ")
# q6 = cursor.fetchall()

# for i in q6:
    # x = i[0]
    # y = i[1]
    # mp.scatter(x, y, s = 2)


mp.show()



conn.commit()
cursor.close()
conn.close()