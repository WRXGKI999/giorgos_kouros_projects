CREATE TABLE Credits(
   actors TEXT,
   crew TEXT,
   id INT
);

CREATE TABLE Keywords(
   id INT,
   keywords TEXT
);

CREATE TABLE Links(
   movieId INT,
   imdbId INT,
   tmdbId INT
);

CREATE TABLE Movies_Metadata(
   adult BOOL,
   belongs_to_collection VARCHAR(190),
   budget INT,
   genres VARCHAR(270),
   homepage VARCHAR(250),
   id INT,
   imdb_id VARCHAR(10),
   original_language VARCHAR(10),
   original_title VARCHAR(110),
   overview VARCHAR(1000),
   popularity NUMERIC,
   poster_path VARCHAR(40),
   production_companies VARCHAR(1260),
   production_countries VARCHAR(1040),
   release_date DATE,
   revenue BIGINT,
   runtime NUMERIC,
   spoken_languages VARCHAR(770),
   status VARCHAR(20),
   tagline VARCHAR(300),
   title VARCHAR(110),
   video BOOL,
   vote_average NUMERIC,
   vote_count INT
);

CREATE TABLE Ratings_Small(
   userId INT,
   movieId INT,
   rating NUMERIC,
   timestamp BIGINT
);

CREATE TABLE Ratings(
   userId INT,
   movieId INT,
   rating NUMERIC,
   timestamp BIGINT
);

/*Se auto to shmeio meta ta create ektelesame to arxeio python gia tin proepexergasia twn dedomenwn 
kai sth synexeia ektelesame tis parakato entoles ALTER TABLE sthn bash mas */

ALTER TABLE movies_metadata ADD PRIMARY KEY (id);
ALTER TABLE keywords ADD PRIMARY KEY (id);
ALTER TABLE credits ADD PRIMARY KEY (id);
ALTER TABLE links ADD PRIMARY KEY (movieId);
ALTER TABLE ratings_smalls ADD PRIMARY KEY (userId,movieId);
ALTER TABLE ratings ADD PRIMARY KEY (userId,movieId);
ALTER TABLE keywords ADD CONSTRAINT k_id_fkey FOREIGN KEY (id) REFERENCES movies_metadata (id);
ALTER TABLE credits ADD CONSTRAINT c_id_fkey FOREIGN KEY (id) REFERENCES movies_metadata (id);
ALTER TABLE links ADD CONSTRAINT l_id_fkey FOREIGN KEY (tmdbId) REFERENCES movies_metadata (id);
ALTER TABLE ratings ADD CONSTRAINT r_movieId_fkey FOREIGN KEY (movieId) REFERENCES movies_metadata (id);
ALTER TABLE ratings_small ADD CONSTRAINT rs_movieId_fkey FOREIGN KEY (movieId) REFERENCES movies_metadata (id);
