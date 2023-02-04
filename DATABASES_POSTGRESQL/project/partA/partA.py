import psycopg2

host = "tsirigo.postgres.database.azure.com"
dbname = "MOVIES"
user = "ananas@tsirigo"
password = "@n@n@$2021"
sslmode = "require"

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()

cursor.execute("CREATE TABLE credits_temp (LIKE credits); INSERT INTO credits_temp (id,actors,crew) SELECT DISTINCT ON  (id) id, actors, crew FROM credits; DROP TABLE credits; ALTER TABLE credits_temp  RENAME TO credits; ")
print('teleiwse to drop duplicates sto table credits')
cursor.execute("CREATE TABLE keywords_temp (LIKE keywords); INSERT INTO keywords_temp (id,keywords) SELECT DISTINCT ON  (id) id, keywords FROM keywords; DROP TABLE keywords; ALTER TABLE keywords_temp  RENAME TO keywords; ")
print('teleiwse to drop duplicates sto table keywords')
cursor.execute("CREATE TABLE movies_metadata_temp (LIKE movies_metadata); INSERT INTO movies_metadata_temp (id,adult,belongs_to_collection,budget,genres,homepage,imdb_id,original_language,original_title,overview,popularity,poster_path,production_companies,production_countries,release_date ,revenue,runtime,spoken_languages,status,tagline,title,video,vote_average,vote_count) SELECT DISTINCT ON (id) id, adult,belongs_to_collection,budget,genres,homepage,imdb_id,original_language,original_title,overview,popularity,poster_path,production_companies,production_countries,release_date ,revenue,runtime,spoken_languages,status,tagline,title,video,vote_average,vote_count FROM movies_metadata; DROP TABLE movies_metadata; ALTER TABLE movies_metadata_temp RENAME TO movies_metadata; ")
print('teleiwse to drop duplicates sto table movies_metadata')
cursor.execute("CREATE TABLE links_temp (LIKE links); INSERT INTO links_temp (movieId,imdbId,tmdbId) SELECT DISTINCT ON  (movieId) movieId,imdbId,tmdbId FROM links; DROP TABLE links; ALTER TABLE links_temp RENAME TO links;") # delete du
print('teleiwse to drop duplicates sto table links')

print('ksekinise sugkrish me ratings_small')
cursor.execute("DELETE FROM ratings_small WHERE  NOT EXISTS (SELECT  movies_metadata.id FROM   movies_metadata WHERE  movies_metadata.id = ratings_small.movieId  ); ")
print('teleiwse h sygkirish ratings_small - movies')
print('ksekinise sugkrish me links')
cursor.execute("DELETE FROM links WHERE  NOT EXISTS (SELECT  movies_metadata.id FROM   movies_metadata WHERE  movies_metadata.id = links.tmdbId  ); ")
print('teleiwse h sygkirish links - movies')
print('ksekinise sugkrish me credits')
cursor.execute("DELETE FROM credits WHERE  NOT EXISTS (SELECT  movies_metadata.id FROM   movies_metadata WHERE  movies_metadata.id = credits.id  ); ")
print('teleiwse h sygkirish cretids - movies')
print('ksekinise sugkrish me keywords')
cursor.execute("DELETE FROM keywords WHERE  NOT EXISTS ( SELECT  movies_metadata.id FROM   movies_metadata WHERE  movies_metadata.id = keywords.id  ); ")
print('teleiwse h sygkirish keywords - movies')
print('ksekinise sugkrish me ratings')
cursor.execute("DELETE FROM ratings WHERE  NOT EXISTS (SELECT  movies_metadata.id FROM   movies_metadata WHERE  movies_metadata.id = ratings.movieId  ); ")
print('teleiwse h sygkirish ratings - movies') 

conn.commit()
cursor.close()
conn.close()