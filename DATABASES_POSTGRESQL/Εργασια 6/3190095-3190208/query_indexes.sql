CREATE INDEX hosts
ON "Listing2" (host_id);

CREATE INDEX location 
ON "Location" (neighbourhood_cleansed);

CREATE INDEX id 
ON 	"Listing2" (id) WHERE id > 40000000;

CREATE INDEX hostslistings 
ON "Host" (id) WHERE listings_count > 10;

CREATE INDEX reviewlistings 
ON "Listing2" (id) WHERE review_scores_rating = '100';

CREATE INDEX mp 
ON "Price" (listing_id) WHERE monthly_price < 5000;

CREATE INDEX rc 
ON "RoomCopy" (listing_id) WHERE beds > 8;

CREATE INDEX cal 
ON "Calendar2" (listing_id) WHERE date = '2020-06-25' AND available = true;

CREATE INDEX resptime 
ON "Host" (id) WHERE respone_time = 'within an hour';