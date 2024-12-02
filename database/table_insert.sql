INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Shpack','20 км от тебя, время убегать', 'M','shpack','F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Виталя','Позабочусь о твоей безопастности в сети', 'M', 'shpack1','F');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Александр','I speak English, еб твою мать!', 'M', 'shpack2','F');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Жена Валеры','Валера сэби от сюда, на кой хуй я тебе нужна', 'F', 'ValerasWife','M');

INSERT INTO relations(sender_id, reciever_id) VALUES (1,2);
INSERT INTO relations(sender_id, reciever_id) VALUES (3,2);
INSERT INTO relations(sender_id, reciever_id) VALUES (2,1);