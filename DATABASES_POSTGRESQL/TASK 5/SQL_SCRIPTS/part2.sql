/* Find which neighbourhoods have more than 1000 AirBnbs . Using OUTER JOIN here, even neighbourhoods with 0 AirBnbs
would have been taken into consideration! Output : 2 rows */

SELECT "Geolocation2".properties_neighbourhood,COUNT("Location".listing_id) AS Total_AirBnbs
FROM "Geolocation2"
FULL OUTER JOIN "Location" ON "Geolocation2".properties_neighbourhood = "Location".neighbourhood_cleansed
GROUP BY "Geolocation2".properties_neighbourhood
HAVING COUNT("Location".listing_id) > 1000




/* Find for AirBnbs with id number larger than 40000000, the review comments that they have. 
Using OUTER JOIN here, it will output all the requested AirBnbs even if they do not have any comment yet ! Output : 2570 rows */

SELECT "Listing2".id, "Review2".comments
FROM "Listing2"
FULL OUTER JOIN "Review2" ON "Listing2".id = "Review2".listing_id
WHERE "Listing2".id > 40000000
ORDER BY "Listing2".id DESC




/* Find all the hosts that have in their property more than 10 AirBnbs and more than 9 of them have a 100 review score
rating. Output : 11 rows */

SELECT "Host".id, "Host".name,COUNT("Listing2".id) AS Total_AirBnbs_With_100_score
FROM "Host"
INNER JOIN "Listing2" ON "Host".id = "Listing2".host_id
WHERE "Host".listings_count > 10 AND "Listing2".review_scores_rating = '100'
GROUP BY "Host".id,"Host".name
HAVING COUNT("Listing2".id) > 9
ORDER BY Total_AirBnbs_With_100_score DESC




/* Find the AirBnbs with a monthly price less than 5000 and a number of beds more than 8. Output : 2 rows */

SELECT "Price".listing_id,"Price".monthly_price,"RoomCopy".beds
FROM "Price"
INNER JOIN "RoomCopy" ON "Price".listing_id = "RoomCopy".listing_id
WHERE "Price".monthly_price < 5000 AND "RoomCopy".beds > 8
ORDER BY "Price".listing_id




/* Find all the AirBnbs and their Host's name that are available at 25-06-2020 and the host's respone time is about an hour.
Output : 5517 rows */

SELECT "Listing2".id,"Host".name
FROM "Host"
INNER JOIN "Listing2" ON "Host".id = "Listing2".host_id
INNER JOIN "Calendar2" ON "Listing2".id = "Calendar2".listing_id
WHERE "Calendar2".date = '2020-06-25' AND "Calendar2".available = true AND "Host".respone_time = 'within an hour'
ORDER BY "Listing2".id