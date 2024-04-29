/* Για να λειτουργήσει σωστά η trigger συνάρτησή μας πρέπει κατά την εισαγωγή μιας νέας εγγραφής στον πίνακα Listing2 να
εισάγουμε τον ήδη υπολογισμένο αριθμό Entire home/apt,Private room, Shared room στα 3 αντίστοιχα πεδία 
calculated_host_listings_count για τον host που του ανήκει το id του σπιτιού που θέλουμε να κάνουμε εγγραφή. Με αυτόν τον τρόπο
ενωμερώνεται σωστά και η νέα εγγραφή μας στα 3 αυτα πεδία του πίνακα Listing2.
Το παράδειγμα που τρέξαμε έχει ως εξής:
INSERT INTO "Listing2" (id,host_id,room_type,calculated_host_listings_count_entire_homes,
calculated_host_listings_count_private_rooms,calculated_host_listings_count_shared_rooms)
VALUES (1,37177,'Entire home/apt',6,0,0);
Μέχρι την εισαγωγή αυτής της εγγραφής ο host με id 37177 είχε καταχωρημένα 6 Entire home/apt οπότε μπαίνουν και οι
αντίστοιχες τιμές στο παραπάνω απόσπασμα κώδικα για να λειτουργήσουν σωστά οι πράξεις και οι ενημερώσεις. Με ίδιο τρόπο
πρέπει να γίνεται κάθε νέα εγγραφή στον πίνακά μας.*/

CREATE OR REPLACE FUNCTION addition_subtraction()
RETURNS TRIGGER AS
$$
BEGIN
        IF TG_OP = 'DELETE' THEN
            UPDATE "Host"
            SET listings_count = listings_count - 1, 
            calculated_listings_count = calculated_listings_count - 1,
			total_listings_count = total_listings_count - 1
            WHERE id = OLD.host_id;
            IF OLD.room_type = 'Entire home/apt' THEN
            	UPDATE "Listing2"
            	SET calculated_host_listings_count_entire_homes = calculated_host_listings_count_entire_homes - 1
            	WHERE host_id = OLD.host_id;
            END IF;
            IF OLD.room_type = 'Shared room' THEN                
            	UPDATE "Listing2"
            	SET calculated_host_listings_count_shared_rooms = calculated_host_listings_count_shared_rooms - 1
            	WHERE host_id = OLD.host_id;                
            END IF;
            IF OLD.room_type = 'Private room' THEN               
            	UPDATE "Listing2"
            	SET calculated_host_listings_count_private_rooms = calculated_host_listings_count_private_rooms - 1
            	WHERE host_id = OLD.host_id;               
            END IF;
            RETURN OLD;
        ELSE
            UPDATE "Host"
            SET listings_count = listings_count + 1, 
            calculated_listings_count = calculated_listings_count + 1,
			total_listings_count = total_listings_count + 1
            WHERE id = NEW.host_id;
            IF NEW.room_type = 'Entire home/apt' THEN
                UPDATE "Listing2"
                SET calculated_host_listings_count_entire_homes = calculated_host_listings_count_entire_homes + 1
                WHERE host_id = NEW.host_id;
            END IF;
            IF NEW.room_type = 'Shared room' THEN
                UPDATE "Listing2"
                SET calculated_host_listings_count_shared_rooms = calculated_host_listings_count_shared_rooms + 1
                WHERE host_id = NEW.host_id;
            END IF;
            IF NEW.room_type = 'Private room' THEN
                UPDATE "Listing2"
                SET calculated_host_listings_count_private_rooms = calculated_host_listings_count_private_rooms + 1
                WHERE host_id = NEW.host_id;
            END IF;
            RETURN NEW;
        END IF;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER In_Del
AFTER INSERT OR DELETE
ON "Listing2"
FOR EACH ROW
EXECUTE PROCEDURE addition_subtraction();


---------------------------------------------------------------------------------------------------------------------------------


/* Με τη συνάρτηση trigger valid_neighbourhood απαγορεύεται η εισαγωγή πλειάδας στον πίνακα Location με 
neighbourhood_cleansed(γειτονιά) η οποία δεν αντιστοιχεί σε μία απο τις 45 γειτονιές (column name : neighbourhood) του πίνακα 
Neighbourhood2.
Παράδειγμα :
	INSERT INTO "Listing2" (id)
	VALUES(1);
	INSERT INTO "Location" (listing_id,neighbourhood_cleansed)
	VALUES (1,'ΚΟΡΙΝΘΟΣ');
Προκειμένου να εισάγωγουμε μια νέα πλειάδα στον πίνακα Location πρέπει πρώτα να εισαχθεί η αντίστοιχη πλειάδα με το καινούργιο id 
του σπιτιού στον πίνακα Listing2 και μετά να εισαχθεί στον Location. Στο παραπάνω παράδειγμα λόγω της συνάρτησής μας η εισαγωγή 
INSERT INTO Location (listing_id,neighbourhood_cleansed) VALUES (1,'ΚΟΡΙΝΘΟΣ'); θα απαγορευτεί και θα εμφανιστεί στην οθόνη 
το αντίστοιχο error message που έχουμε ορίσει. Αν η γειτονιά υπάρχει στον πίνακα Neighbourhood2 η εισαγωγή θα γίνει κανονικά.*/


CREATE OR REPLACE FUNCTION check_neighbourhood()
RETURNS TRIGGER AS
$$
BEGIN
		IF NEW.neighbourhood_cleansed = (select neighbourhood from "Neighbourhood2" where neighbourhood=NEW.neighbourhood_cleansed) THEN
			RETURN NEW;
		ELSE 
			RAISE EXCEPTION 'The neighbourhood of this house is not valid';
		END IF;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER valid_neighbourhood
BEFORE INSERT ON "Location"
FOR EACH ROW 
EXECUTE PROCEDURE check_neighbourhood();

---------------------------------------------------------------------------------------------------------------------------------

