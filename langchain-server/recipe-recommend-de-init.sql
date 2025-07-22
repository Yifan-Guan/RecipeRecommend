DROP DATABASE IF EXISTS `recipe-recommend-db`;
CREATE DATABASE `recipe-recommend-db`;

USE mysql;
CREATE USER IF NOT EXISTS `recipe-recommend-db-manager`@`*` IDENTIFIED BY '12345';
GRANT ALL PRIVILEGES ON `recipe-recommend-db`.* TO `recipe-recommend-db-manager`@`*`;

USE `recipe-recommend-db`;
DROP TABLE IF EXISTS `user-info`;
CREATE TABLE `user-info` (
`user-id` TEXT,
`user-name` TEXT,
`user-password` TEXT
);
DROP TABLE IF EXISTS `login-status`;
CREATE TABLE `login-status` (
`user-id` TEXT
);
DROP TABLE IF EXISTS `recipes`;
CREATE TABLE `recipes` (
`name` TEXT,
`ingredients` TEXT,
`steps` TEXT,
`img` TEXT
)

INSERT INTO `user-info`(`user-id`, `user-name`, `user-password`)
VALUES ('0', 'admin', '12345');