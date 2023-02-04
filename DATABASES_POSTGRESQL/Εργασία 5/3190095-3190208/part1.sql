CREATE TABLE "RoomCopy" AS 
SELECT listing_id, accommodates, bathrooms, bedrooms, beds, bed_type, 
amenities, square_feet, price, weekly_price, monthly_price, security_deposit
FROM "Room";
ALTER TABLE "RoomCopy" ADD CONSTRAINT listing_id_fkey FOREIGN KEY (listing_id) REFERENCES "Listing2" (id);
UPDATE "RoomCopy" SET 
amenities = REPLACE (amenities,'{','');
UPDATE "RoomCopy" SET 
amenities = REPLACE (amenities,'}','');
UPDATE "RoomCopy" SET 
amenities = REPLACE (amenities,'"','');
CREATE TABLE "Amenity" AS
SELECT DISTINCT regexp_split_to_table(amenities, ',') AS amenity_name 
FROM "RoomCopy";
DELETE FROM "Amenity" WHERE amenity_name = '';
ALTER TABLE "Amenity" ADD COLUMN amenity_id SERIAL PRIMARY KEY;

CREATE TABLE "RoomAmenities" AS SELECT DISTINCT listing_id , regexp_split_to_table(amenities, ',') AS amenity_name FROM "RoomCopy"
WHERE amenities != '';
ALTER TABLE "RoomAmenities" ADD COLUMN amenity_id INT; 
UPDATE "RoomAmenities"
SET amenity_id = ids.amenity_id
FROM "Amenity" AS ids
WHERE "RoomAmenities".amenity_name = ids.amenity_name;
ALTER TABLE "RoomCopy" ADD PRIMARY KEY (listing_id);
ALTER TABLE "RoomAmenities" ADD CONSTRAINT listing_id_fkey FOREIGN KEY (listing_id) REFERENCES "RoomCopy" (listing_id);
ALTER TABLE "RoomAmenities" ADD CONSTRAINT amenity_id_fkey FOREIGN KEY (amenity_id) REFERENCES "Amenity" (amenity_id);
ALTER TABLE "RoomAmenities" ADD PRIMARY KEY (listing_id,amenity_id);
ALTER TABLE "RoomCopy" DROP COLUMN amenities;