ALTER TABLE "Calendar" ADD CONSTRAINT calendar_listing_id_fkey FOREIGN KEY (listing_id) REFERENCES "Listings" (id);
ALTER TABLE "Reviews" ADD CONSTRAINT reviews_listing_id_fkey FOREIGN KEY (listing_id) REFERENCES "Listings" (id);
ALTER TABLE "Reviews_Summary" ADD CONSTRAINT reviews_summary_listing_id_fkey FOREIGN KEY (listing_id) REFERENCES "Listings" (id);
ALTER TABLE "Listings_Summary" ADD CONSTRAINT listings_summary_id_fkey FOREIGN KEY (id) REFERENCES "Listings" (id);
ALTER TABLE "Listings_Summary" ADD CONSTRAINT listings_summary_neighbourhood_fkey FOREIGN KEY (neighbourhood) REFERENCES "Neighbourhoods" (neighbourhood);
ALTER TABLE "Geolocation" ADD CONSTRAINT geolocation_properties_neighbourhood_fkey FOREIGN KEY (properties_neighbourhood) REFERENCES "Neighbourhoods" (neighbourhood);
ALTER TABLE "Listings" ADD CONSTRAINT listings_neighbourhood_cleansed_fkey FOREIGN KEY (neighbourhood_cleansed) REFERENCES "Neighbourhoods" (neighbourhood);
