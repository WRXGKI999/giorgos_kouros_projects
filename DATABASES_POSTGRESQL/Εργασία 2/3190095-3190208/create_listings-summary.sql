CREATE TABLE "Listings_Summary"(
   id INT,
   name VARCHAR(100),
   host_id INT,
   host_name VARCHAR(40),
   neighbourhood_group VARCHAR(10),
   neighbourhood VARCHAR(40),
   latitude VARCHAR(10),
   longitude VARCHAR(10),
   room_type VARCHAR(20),
   price VARCHAR(10),
   minimum_nights INT,
   number_of_reviews INT,
   last_review VARCHAR(10),
   reviews_per_month VARCHAR(10),
   calculated_host_listings_count INT,
   availability_365 INT,
   PRIMARY KEY(id)
);