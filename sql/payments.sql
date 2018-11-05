CREATE TABLE payments (
 id serial PRIMARY KEY,
 client_id int NOT NULL REFERENCES clients(id),
 date TIMESTAMP NOT NULL,
 created_on TIMESTAMP NOT NULL
)
