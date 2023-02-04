/* ΚΩΔΙΚΑΣ POSTGRESQL ΠΟΥ ΕΚΤΕΛΕΣΤΗΚΕ ΣΤΟ VM ΤΡΕΧΟΝΤΑΣ psql -U postgres -d GDPR */

/* ΑΣΚΗΣΗ 1, ΑΣΚΗΣΗ 2 */

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	description VARCHAR(255)
);

INSERT INTO users (username, password, description) VALUES ('3190095',
'pwd1', 'This is me, pwd1');

INSERT INTO users (username, password, description) VALUES ('admin',
'pwd2', 'This is me, pwd2');

ALTER TABLE users ADD COLUMN hashed_pwd TEXT;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

UPDATE users SET hashed_pwd = crypt(password, gen_salt('bf'));

ALTER TABLE users DROP COLUMN password;

ALTER TABLE users RENAME COLUMN hashed_pwd TO password;

CREATE OR REPLACE FUNCTION hash(pwd TEXT)
RETURNS TEXT AS $$
BEGIN
   RETURN crypt(pwd, gen_salt('bf', 8));
END;
$$ LANGUAGE plpgsql; /*function that can be used when we want to insert new user data in the table, it hashes the password using salting(8 bytes) 
with blowfish algorithm*/

/* ΑΣΚΗΣΗ 4 */

CREATE TABLE logging (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
	success BOOLEAN
);

/* για debugs της άσκησης 4 χρησιμοποιήθηκε η εντολή TRUNCATE logging RESTART IDENTITY; κάθε φορά πριν από νεά εκκίνηση του server, 
η οποία αδειάζει τον πίνακα (κάνει και reset τα ids να ξεκινάνε ξανά από το 1), ώστε με κάθε εκκίνηση του server για DEBUG
να γίνεται έλεγχος μόνο με τα δεδομένα εκείνου του session, ο πίνακας θα μείνει άδειος ώστε να πραγματοποιήσετε και εσείς τις δοκιμές σας και να 
τεστάρετε όλες τις λειτουργίες του κώδικα. */

ALTER TABLE users
ADD last_pwd_change TIMESTAMP;

UPDATE users
SET last_pwd_change = NOW();

INSERT INTO users (username, description, password, last_pwd_change) VALUES ('username', 'description', hash('password'), NOW());



UPDATE users SET password=hash('newpassword'), last_pwdchange=NOW() WHERE username='username';