CREATE TABLE "Price" AS
SELECT id AS listing_id, price, weekly_price, monthly_price, security_deposit, cleaning_fee,
guests_included, extra_people, minimum_nights, maximum_nights,
minimum_minimum_nights, maximum_minimum_nights, minimum_maximum_nights,
maximum_maximum_nights, minimum_nights_avg_ntm, maximum_nights_avg_ntm FROM "Listing2";
ALTER TABLE "Listing2"
DROP COLUMN price,
DROP COLUMN weekly_price,
DROP COLUMN monthly_price,
DROP COLUMN security_deposit,
DROP COLUMN cleaning_fee,
DROP COLUMN guests_included,
DROP COLUMN extra_people,
DROP COLUMN minimum_nights,
DROP COLUMN maximum_nights,
DROP COLUMN minimum_minimum_nights,
DROP COLUMN maximum_minimum_nights,
DROP COLUMN minimum_maximum_nights,
DROP COLUMN maximum_maximum_nights,
DROP COLUMN minimum_nights_avg_ntm,
DROP COLUMN maximum_nights_avg_ntm;
ALTER TABLE "Listing_Summary2"
DROP COLUMN price,
DROP COLUMN minimum_nights;
ALTER TABLE "Price" ADD CONSTRAINT listing_id_fkey FOREIGN KEY (listing_id) REFERENCES "Listing2" (id);
UPDATE "Price" SET 
price = REPLACE (price,'$',''),
weekly_price = REPLACE (weekly_price,'$',''),
monthly_price = REPLACE (monthly_price, '$',''),
security_deposit = REPLACE (security_deposit,'$',''),
cleaning_fee = REPLACE (cleaning_fee,'$',''),
extra_people = REPLACE (extra_people,'$','');
UPDATE "Price" SET
price = REPLACE (price,',',''),
weekly_price = REPLACE (weekly_price,',',''),
monthly_price = REPLACE (monthly_price, ',',''),
security_deposit = REPLACE (security_deposit,',',''),
cleaning_fee = REPLACE (cleaning_fee,',',''),
extra_people = REPLACE (extra_people,',','');
ALTER TABLE "Price"
ALTER COLUMN price TYPE NUMERIC USING price::numeric,
ALTER COLUMN weekly_price TYPE NUMERIC USING weekly_price::numeric,
ALTER COLUMN monthly_price TYPE NUMERIC USING monthly_price::numeric,
ALTER COLUMN security_deposit TYPE NUMERIC USING security_deposit::numeric,
ALTER COLUMN cleaning_fee TYPE NUMERIC USING cleaning_fee::numeric,
ALTER COLUMN extra_people TYPE NUMERIC USING extra_people::numeric;