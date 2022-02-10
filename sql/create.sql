CREATE SCHEMA `discuz_crawler` DEFAULT CHARACTER SET utf8mb4 ;

CREATE TABLE `discuz_crawler`.`post` (
  `thread_id` INT NOT NULL AUTO_INCREMENT,
  `is_available` TINYINT NULL,
  `is_locked` TINYINT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE `discuz_crawler`.`file` (
  `file_id` INT NOT NULL AUTO_INCREMENT,
  `key` CHAR(8) NULL,
  `password_unzip` VARCHAR(30) NULL,
  `has_transferred` TINYINT NULL DEFAULT 0,
  `associated_post` INT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE `discuz_crawler`.`file_detail` (
  `file_id` INT NOT NULL,
  `name` VARCHAR(15) NULL,
  `release_date` DATE NULL,
  `size` VARCHAR(10) NULL,
  PRIMARY KEY (`file_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE `discuz_crawler`.`post_detail` (
  `thread_id` INT NOT NULL,
  `title` VARCHAR(45) NULL,
  `forum_id` INT NULL,
  PRIMARY KEY (`thread_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE `discuz_crawler`.`user_site` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `cookie` VARCHAR(500) NULL,
  `name` VARCHAR(20) NULL,
  `formhash` VARCHAR(20) NULL,
  `last_login` DATETIME NULL,
  PRIMARY KEY (`user_id`));
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;

CREATE TABLE `discuz_crawler`.`user_feimao` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `cookie` VARCHAR(400) NULL,
  `name` VARCHAR(20) NULL,
  `last_login` DATETIME NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;
