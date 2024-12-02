CREATE DATABASE daishpakudb;

\c daishpakudb

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
);

INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Shpack','20 км от тебя, время убегать', 'M','shpack','F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Виталя','Позабочусь о твоей безопастности в сети', 'M', 'shpack1','F');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Александр','I speak English, еб твою мать!', 'M', 'shpack2','F');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Иван Золо','Даже Стопапупа процитирует ТикТок для своей выгоды.!', 'M', 'shpack3','F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Борис Ельцин','Вы — это надежда России. Вы — это вера России. Вы — это любовь России. Вы — это будущее России.', 'M', 'shpack4', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Геннадий Горыныч','У меня не только три головы', 'M', 'shpack5', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Дмитрий Длинный(8)','Могу достать до луны', 'M', 'shpack6', 'F');

INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Евгений Енот','Люблю ночные прогулки по мусоркам', 'M', 'shpack7', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Жора Жук','Всегда на связи, даже под землей', 'M', 'shpack8', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Захар Зебра','Полосатый, но не опасный', 'M', 'shpack9', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Илья Игуана','Холоднокровный, но с горячим сердцем', 'M', 'shpack10', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Кирилл Кот','Мурлыкаю на все 100', 'M', 'shpack11', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Леонид Лев','Король джунглей в душе', 'M', 'shpack12', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Михаил Медведь','Люблю мед и спячку', 'M', 'shpack13', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Николай Носорог','Сильный и уверенный', 'M', 'shpack14', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Олег Орел','Высоко летаю, далеко гляжу', 'M', 'shpack15', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Павел Пингвин','Люблю холод и рыбу', 'M', 'shpack16', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Роман Рысь','Тихий охотник', 'M', 'shpack17', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Сергей Слон','Большой и добрый', 'M', 'shpack18', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Тимур Тигр','Полосатый и опасный', 'M', 'shpack19', 'F');
INSERT INTO users(name,bio,gender,user_tg_id,interested_in_gender) VALUES ('Ульяна Утка','Крякаю на все 100', 'M', 'shpack20', 'F');


INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Жена Валеры','Валера сэби от сюда, на кой хуй я тебе нужна', 'F', 'ValerasWife','M');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Екатерина Дамтебе','Люблю побольше, но и твой сойдет', 'F', 'shpekachka1','M');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Футболиска','Люблю загонять мяч в свои ворота', 'F', 'shpekachka2','M');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Валентина','Жду тебя на своей кухне', 'F', 'shpekachka3','M');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Cоциал-демократ','Готова свергнуть твою монархию', 'F', 'shpekachka4','M');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Ритуальные Услуги','Похороню твоего деда', 'F', 'shpekachka5','M');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Виталя','И что, что у меня член есть, я тоже мужской любви хочу', 'F', 'shpekachka6','M');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Лена','Очень стесняюсь, но тебя не испугаюсь', 'F', 'shpekachka7','M');
INSERT INTO users(name,bio,gender,user_tg_id, interested_in_gender) VALUES ('Дочь Путина','Мой папы полюбит тебя даже если ты пробитый', 'F', 'shpekachka8','M');

INSERT INTO relations(sender_id, reciever_id) VALUES (1,2);
INSERT INTO relations(sender_id, reciever_id) VALUES (3,2);
INSERT INTO relations(sender_id, reciever_id) VALUES (2,1);