CREATE TABLE "Calendar"(
   listing_id INT,
   date DATE,
   available BOOLEAN,
   price VARCHAR(10),
   adjusted_price VARCHAR(10),
   minimum_nights INT,
   maximum_nights INT,
   PRIMARY KEY (listing_id,date)
);