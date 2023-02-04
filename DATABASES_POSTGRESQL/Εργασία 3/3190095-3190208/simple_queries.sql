/*Find all Cottage AirBnbs available in 18-03-2020 ordered by the maximum nights you can stay (descending) Output : 3 rows */

SELECT "Listings".id,"Listings".property_type,"Calendar".date,"Calendar".available,"Calendar".maximum_nights,"Calendar".price
FROM "Listings" 
INNER JOIN "Calendar" ON "Listings".id = "Calendar".listing_id
WHERE "Calendar".date = '2020-06-18' AND "Calendar".available = true AND "Listings".property_type = 'Cottage'
ORDER BY "Calendar".maximum_nights DESC




/* Find all AirBnbs that are unavailable in 02/05/2020-04/05/2020 and the host's name ends with an s 
ordered by the date (ascending) Output : 3560 rows */

SELECT "Listings".id,"Listings".host_name,"Calendar".date 
FROM "Calendar"
INNER JOIN "Listings" ON "Listings".id = "Calendar".listing_id
WHERE "Calendar".date BETWEEN '2020-05-02' AND '2020-05-04'
AND "Calendar".available = false
AND "Listings".host_name LIKE '%s'
ORDER BY date 




/* Find the geographical coordinates of the ΑΜΠΕΛΟΚΗΠΟΙ neighbourhood Output : 1 row */

SELECT * FROM "Geolocation"
INNER JOIN "Neighbourhoods" ON "Geolocation".properties_neighbourhood = "Neighbourhoods".neighbourhood
WHERE "Neighbourhoods".neighbourhood = 'ΑΜΠΕΛΟΚΗΠΟΙ'




/* Find how many reviews does each AirBnb have, ordered by the amount of the reviews(descending) Output : 11541 rows */

SELECT "Listings".id,count("Reviews".comments) as Total_Reviews  
FROM "Listings"
LEFT OUTER JOIN "Reviews" ON "Listings".id = "Reviews".listing_id
GROUP BY "Listings".id
ORDER BY Total_Reviews DESC




/* Find which AirBnbs in ΓΚΑΖΙ neighbourhood have the highest review score rating (100) ordered by AirBnb id(ascending) 
Output : 22 rows */

SELECT "Listings".id,"Neighbourhoods".neighbourhood FROM "Listings"
INNER JOIN "Neighbourhoods" ON "Neighbourhoods".neighbourhood = "Listings".neighbourhood_cleansed
WHERE "Neighbourhoods".neighbourhood = 'ΓΚΑΖΙ' AND "Listings".review_scores_rating = '100'
ORDER BY "Listings".id




/* Find the average number of reviews of the AirBnbs in each neighbourhood ordered by the average number of reviews(ascending)
 Output : 45 rows */

SELECT "Neighbourhoods".neighbourhood,AVG("Listings".number_of_reviews)::NUMERIC(10,0) AS "Average_number_of_reviews"
FROM "Listings"
INNER JOIN "Neighbourhoods" ON "Listings".neighbourhood_cleansed = "Neighbourhoods".neighbourhood
GROUP BY "Neighbourhoods".neighbourhood
ORDER BY "Average_number_of_reviews"




/* Find the maximum number of bedrooms that an available AirBnb can have Output : 1 row */

SELECT MAX(DISTINCT "Listings".bedrooms) AS "Max_number_of_bedrooms" 
FROM "Listings"
INNER JOIN "Calendar" ON "Listings".id = "Calendar".listing_id
WHERE "Calendar".available = true




/* Find the minimum number of guests that an AirBnb, priced at $50.00, can have in each neighbourhood (some neighbourhoods 
may not have AirBnbs priced at $50.00 so they are not shown in the table) Output : 41 rows */

SELECT "Neighbourhoods".neighbourhood,"Listings".price, MIN(DISTINCT "Listings".guests_included) AS "min_Num_Of_Guests" 
FROM "Listings"
INNER JOIN "Neighbourhoods" ON "Listings".neighbourhood_cleansed = "Neighbourhoods".neighbourhood
WHERE "Listings".price = '$50.00'
GROUP BY "Listings".price,"Neighbourhoods".neighbourhood
ORDER BY "min_Num_Of_Guests"




/* Find all the AirBnbs where the reviews are saying that the host was excellent and the host's identity is verified
Output : 1339 rows */ 

SELECT "Listings".id, "Reviews".reviewer_name,"Reviews".comments 
FROM "Listings"
INNER JOIN "Reviews" ON "Listings".id = "Reviews".listing_id
WHERE ("Reviews".comments LIKE '%excellent host%'OR "Reviews".comments LIKE '%Excellent host%') 
AND "Listings".host_identity_verified = true




/* Find for every AirBnb the dates that it has been reviewed by someone. An AirBnb with the variable "null" in the column 
"Reviews".date means that it has not been reviewed by anyone yet. Ordered by the ids(descending) Output : 416794 rows */

SELECT "Listings".id, "Reviews".date
FROM "Listings"
FULL OUTER JOIN "Reviews" ON "Listings".id = "Reviews".listing_id
ORDER BY "Listings".id DESC




/* Find how many Airbnbs all the superhosts with 100% response and acceptance rate have. Output : 1420 rows */

SELECT host_name, host_id,count(host_id) AS "Number_of_owned_AirBnbs" 
FROM "Listings"
WHERE host_response_rate = '100%' AND host_acceptance_rate = '100%' AND host_is_superhost = true
GROUP BY host_name,host_id
ORDER BY host_name




/* Find all the Villa AirBnbs that have at least 5 beds and not more than 10. Output : 8 rows */

SELECT id,property_type,beds 
FROM "Listings"
WHERE property_type = 'Villa' AND beds BETWEEN 5 AND 10
ORDER BY id



