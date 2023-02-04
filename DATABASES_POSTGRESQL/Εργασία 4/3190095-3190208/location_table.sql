CREATE TABLE "Location" AS 
SELECT id AS listing_id, street, neighbourhood, neighbourhood_cleansed, city, state,
zipcode, market, smart_location, country_code, country, latitude, longitude,
is_location_exact FROM "Listing2";
ALTER TABLE "Location" ADD CONSTRAINT listing_id_fkey FOREIGN KEY (listing_id) REFERENCES "Listing2" (id);
ALTER TABLE "Listing2" DROP CONSTRAINT neighbourhood_cleansed_fkey;
ALTER TABLE "Location" ADD CONSTRAINT neighbourhood_cleansed_fkey FOREIGN KEY (neighbourhood_cleansed) REFERENCES 
"Neighbourhood2" (neighbourhood);
ALTER TABLE "Listing2"
DROP COLUMN street,
DROP COLUMN neighbourhood,
DROP COLUMN neighbourhood_cleansed,
DROP COLUMN city,
DROP COLUMN state,
DROP COLUMN zipcode,
DROP COLUMN market,
DROP COLUMN smart_location,
DROP COLUMN country_code,
DROP COLUMN country,
DROP COLUMN latitude,
DROP COLUMN longitude,
DROP COLUMN is_location_exact;
ALTER TABLE "Listing_Summary2"
DROP COLUMN neighbourhood,
DROP COLUMN latitude,
DROP COLUMN longitude;