CREATE TABLE "Room" AS 
SELECT id AS "listing_id", accommodates, bathrooms, bedrooms, beds, bed_type, 
amenities, square_feet, price, weekly_price, monthly_price, security_deposit
FROM "Listing2";
ALTER TABLE "Listing2"
DROP COLUMN accommodates,
DROP COLUMN bathrooms,
DROP COLUMN bedrooms,
DROP COLUMN beds,
DROP COLUMN bed_type,
DROP COLUMN amenities,
DROP COLUMN square_feet;
ALTER TABLE "Room" ADD CONSTRAINT listing_id_fkey FOREIGN KEY (listing_id) REFERENCES "Listing2" (id);
UPDATE "Room" SET 
price = REPLACE (price,'$',''),
weekly_price = REPLACE (weekly_price,'$',''),
monthly_price = REPLACE (monthly_price, '$',''),
security_deposit = REPLACE (security_deposit,'$','');
UPDATE "Room" SET 
price = REPLACE (price,',',''),
weekly_price = REPLACE (weekly_price,',',''),
monthly_price = REPLACE (monthly_price, ',',''),
security_deposit = REPLACE (security_deposit,',','');
ALTER TABLE "Room"
ALTER COLUMN price TYPE NUMERIC USING price::numeric,
ALTER COLUMN weekly_price TYPE NUMERIC USING weekly_price::numeric,
ALTER COLUMN monthly_price TYPE NUMERIC USING monthly_price::numeric,
ALTER COLUMN security_deposit TYPE NUMERIC USING security_deposit::numeric;