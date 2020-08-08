create database stop;

create table word (
	id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL
);