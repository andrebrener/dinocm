CREATE TABLE clients_accounts (
 id bigserial PRIMARY KEY,
 client_id smallint REFERENCES clients(id),
 media_id smallint REFERENCES media_ids(id),
 followers integer,
 follows integer,
 follower_users jsonb,
 created_on TIMESTAMP NOT NULL
 );
