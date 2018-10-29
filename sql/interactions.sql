CREATE TABLE interactions (
 id bigserial PRIMARY KEY,
 client_id smallint REFERENCES clients(id),
 interaction_id smallint REFERENCES interaction_ids(id),
 media_id smallint REFERENCES media_ids(id),
 content_id bigint,
 content_text VARCHAR (355),
 username VARCHAR (25) NOT NULL,
 user_followers integer,
 user_follows integer,
 likes_in_content integer,
 kw_searched VARCHAR (30),
 user_to_follow VARCHAR (25),
 user_location VARCHAR (100),
 created_on TIMESTAMP NOT NULL
 );
