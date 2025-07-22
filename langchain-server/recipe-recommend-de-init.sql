DROP DATABASE IF EXISTS `recipe-recommend-db`;
CREATE DATABASE `recipe-recommend-db`;
DROP DATABASE IF EXISTS `recipe-recommend-message-history-db`;
CREATE DATABASE `recipe-recommend-message-history-db`;

USE mysql;
DROP USER IF EXISTS `recipe-recommend-db-manager`@`localhost`;
CREATE USER IF NOT EXISTS `recipe-recommend-db-manager`@`localhost` IDENTIFIED BY '12345';
GRANT ALL PRIVILEGES ON `recipe-recommend-db`.* TO `recipe-recommend-db-manager`@`localhost`;
GRANT ALL PRIVILEGES ON `recipe-recommend-message-history-db`.* TO `recipe-recommend-db-manager`@`localhost`;

USE `recipe-recommend-db`;
DROP TABLE IF EXISTS `user-info`;
CREATE TABLE `user-info` (
`user-id` VARCHAR(20) PRIMARY KEY,
`user-name` TEXT,
`user-password` TEXT
);
DROP TABLE IF EXISTS `login-status`;
CREATE TABLE `login-status` (
`login-user-id` VARCHAR(20) PRIMARY KEY,
FOREIGN KEY(`login-user-id`) REFERENCES `user-info`(`user-id`)
);
DROP TABLE IF EXISTS `recipes`;
CREATE TABLE `recipes` (
`name` VARCHAR(50) PRIMARY KEY,
`ingredients` TEXT,
`steps` TEXT,
`img` TEXT
);
DROP TABLE IF EXISTS `chat-history-info`;
CREATE TABLE `chat-history-info` (
`chat-history-id` VARCHAR(20) PRIMARY KEY,
`chat-history-name` TEXT,
`chat-user-id` VARCHAR(20)
);
DROP TABLE IF EXISTS `chat-history-content`;
CREATE TABLE `chat-history-content` (
`history-id` VARCHAR(20),
`message-index` INT,
`message-role` TEXT,
`message-content` TEXT,
PRIMARY KEY (`history-id`, `message-index`),
FOREIGN KEY (`history-id`) REFERENCES `chat-history-info`(`chat-history-id`)
);

INSERT INTO `user-info`(`user-id`, `user-name`, `user-password`)
VALUES ('0', 'admin', '12345'),
('1', 'test', '12345');

INSERT INTO `chat-history-info`(`chat-history-id`, `chat-history-name`, `chat-user-id`)
VALUES ('0', 'test history 0', '0'),
('1', 'test history 1', '1');

INSERT INTO `chat-history-content` (
`history-id`,
`message-index`,
`message-role`,
`message-content`
) VALUES
('0', 0, 'agent', 'hello'),
('0', 1, 'user', 'hello'),
('0', 2, 'agent', 'hello'),
('0', 3, 'user', 'hello'),
('1', 0, 'agent', 'hello'),
('1', 1, 'user', 'hello'),
('1', 2, 'agent', 'hello'),
('1', 3, 'user', 'hello');