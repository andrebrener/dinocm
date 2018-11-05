CREATE TABLE payments (
 id serial PRIMARY KEY,
 client_id int NOT NULL REFERENCES clients(id),
 amount decimal NOT NULL,
 date TIMESTAMP NOT NULL,
 created_on TIMESTAMP NOT NULL,
 method text NOT NULL
)
