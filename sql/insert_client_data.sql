INSERT INTO clients (tw_username, ig_username, phone, firstname,
            lastname, email, tw_password, ig_password, created_on) VALUES (
            '{tw_username}',
            '{ig_username}',
            '{phone}',
            '{firstname}',
            '{lastname}',
            '{email}',
            crypt('{tw_password}', gen_salt('bf')),
            crypt('{ig_password}', gen_salt('bf')),
            '{created_on}'
)
