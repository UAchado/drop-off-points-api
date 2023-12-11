CREATE DATABASE IF NOT EXISTS points_db;
USE points_db;

CREATE TABLE IF NOT EXISTS points (
    id INT PRIMARY KEY auto_increment,
    name VARCHAR(30) UNIQUE,
    location VARCHAR(50),
    coordinates VARCHAR(200) UNIQUE,
    image VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS auth_point (
    id INT PRIMARY KEY auto_increment,
    email VARCHAR(30),
    dropoff_point_id INTEGER,
);

INSERT INTO points (id, name, location, coordinates, image) VALUES 
(1, "Reitoria", "Departamento 25", "40.631417730224, -8.657526476133642", "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fuaonline.ua.pt%2Fupload%2Fimg%2Fjoua_i_3090.jpg&width=1200"),
(2, "CP", "Departamento 23", "40.62957166653202, -8.655231694880136", "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F001%2F838%2Foriginal.jpg&width=1200"),
(3, "DETI", "Departamento 4", "40.63331148617483, -8.659589862642955", "https://api-assets.ua.pt/files/imgs/000/000/380/original.jpg"),
(4, "Cantina de Santiago", "Departamento 6", "40.630659968175124, -8.659097986459223", "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fuaonline.ua.pt%2Fupload%2Fimg%2Fjoua_i_12306.jpg&width=1200"),
(5, "Cantina do Crasto", "Departamento M", "40.62450887522072, -8.656864475040406", "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fuaonline.ua.pt%2Fupload%2Fimg%2Fjoua_i_2828.JPG&width=1200"),
(6, "Pavilhão Aristides Hall", "Departamento E", "40.63000326980208, -8.654180591479575", "https://d1bvpoagx8hqbg.cloudfront.net/originals/bem-vindos-a-ua-399bd8560914b519d0dca3fc57bd0afe.jpg");

INSERT INTO auth_point (id, email, dropoff_point_id) VALUES 
(1, "tiagogcarvalho2002@gmail.com", 5)