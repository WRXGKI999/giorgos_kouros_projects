UPDATE "Calendar2" SET price = REPLACE (price,'$',''),
adjusted_price = REPLACE (adjusted_price,'$','');
UPDATE "Calendar2" SET price = REPLACE (price,',',''),
adjusted_price = REPLACE (adjusted_price,',','');
ALTER TABLE "Calendar2"
ALTER COLUMN price TYPE NUMERIC USING price::numeric,
ALTER COLUMN adjusted_price TYPE NUMERIC USING adjusted_price::numeric;