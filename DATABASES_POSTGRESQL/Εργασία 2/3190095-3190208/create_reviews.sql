CREATE TABLE "Reviews"(
   listing_id INT,
   id INT,
   date DATE,
   reviewer_id INT,
   reviewer_name VARCHAR(50),
   comments text,
   PRIMARY KEY (id)
);