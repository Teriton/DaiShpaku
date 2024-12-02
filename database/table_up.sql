CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_tg_id VARCHAR(30) DEFAULT NULL UNIQUE,
    name VARCHAR (20) DEFAULT NULL,
    bio VARCHAR (100) DEFAULT NULL,
    gender CHAR (1) DEFAULT NULL,
    current_user_id SERIAL,
    interested_in_gender CHAR (1) DEFAULT NULL
);

CREATE TABLE relations(
    sender_id SERIAL,
    reciever_id SERIAL,
    PRIMARY KEY (sender_id, reciever_id),
    FOREIGN KEY (sender_id) REFERENCES users (user_id),
    FOREIGN KEY (reciever_id) REFERENCES users (user_id)
)