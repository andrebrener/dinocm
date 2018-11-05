CREATE TABLE clients (
 id serial PRIMARY KEY,
 tw_username VARCHAR (355) NOT NULL,
 ig_username VARCHAR (355) NOT NULL,
 firstname VARCHAR(32) NOT NULL,
 lastname VARCHAR(32) NOT NULL,
 email TEXT NOT NULL,
 created_on TIMESTAMP NOT NULL
)
