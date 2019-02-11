-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema jenbar
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema jenbar
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `jenbar` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `jenbar` ;

-- -----------------------------------------------------
-- Table `jenbar`.`currency`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jenbar`.`currency` ;

CREATE TABLE IF NOT EXISTS `jenbar`.`currency` (
  `currency_id` INT(11) NOT NULL AUTO_INCREMENT,
  `currency_short_name` VARCHAR(20) NOT NULL,
  `currency_long_name` VARCHAR(40) NOT NULL,
  `currency_symbol` VARCHAR(10) NOT NULL,
  `country_currency` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`currency_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `jenbar`.`cust_account`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jenbar`.`cust_account` ;

CREATE TABLE IF NOT EXISTS `jenbar`.`cust_account` (
  `account_id` INT(11) NOT NULL AUTO_INCREMENT,
  `currency_id` INT(11) NOT NULL,
  `quantity` DECIMAL(19,6) NOT NULL,
  `last_update` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`account_id`),
  INDEX `currency_id_idx` (`currency_id` ASC) VISIBLE,
  CONSTRAINT `currency_id`
    FOREIGN KEY (`currency_id`)
    REFERENCES `jenbar`.`currency` (`currency_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `jenbar`.`acct_transaction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jenbar`.`acct_transaction` ;

CREATE TABLE IF NOT EXISTS `jenbar`.`acct_transaction` (
  `transaction_id` INT(11) NOT NULL AUTO_INCREMENT,
  `account_id` INT(11) NOT NULL,
  `currency_id` INT(11) NOT NULL,
  `quantity` DECIMAL(19,6) NOT NULL DEFAULT '0.000000',
  `side` VARCHAR(20) NOT NULL,
  `transaction_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`transaction_id`),
  INDEX `fk_transact_acct_idx` (`account_id` ASC) VISIBLE,
  INDEX `fk_transact_currency_idx` (`currency_id` ASC) VISIBLE,
  CONSTRAINT `fk_transact_account`
    FOREIGN KEY (`account_id`)
    REFERENCES `jenbar`.`cust_account` (`account_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_transact_currency`
    FOREIGN KEY (`currency_id`)
    REFERENCES `jenbar`.`currency` (`currency_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `jenbar`.`customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jenbar`.`customer` ;

CREATE TABLE IF NOT EXISTS `jenbar`.`customer` (
  `customer_id` INT(10) NOT NULL DEFAULT '0',
  `user_name` VARCHAR(45) NOT NULL,
  `email_address` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `middle_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `jenbar`.`cust_acct_assoc`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jenbar`.`cust_acct_assoc` ;

CREATE TABLE IF NOT EXISTS `jenbar`.`cust_acct_assoc` (
  `account_id` INT(11) NOT NULL,
  `customer_id` INT(11) NOT NULL,
  `cust_acct_assoc_id` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`cust_acct_assoc_id`),
  INDEX `fk_caa_customer_id_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_caa_account_id_idx` (`account_id` ASC) VISIBLE,
  CONSTRAINT `fk_caa_account_id`
    FOREIGN KEY (`account_id`)
    REFERENCES `jenbar`.`cust_account` (`account_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_caa_customer_id`
    FOREIGN KEY (`customer_id`)
    REFERENCES `jenbar`.`customer` (`customer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

USE `jenbar` ;

-- -----------------------------------------------------
-- Placeholder table for view `jenbar`.`customer_balance`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jenbar`.`customer_balance` (`customer_id` INT, `user_name` INT, `email_address` INT, `first_name` INT, `middle_name` INT, `last_name` INT, `account_id` INT, `quantity` INT, `last_update` INT, `currency_id` INT, `currency_short_name` INT, `currency_long_name` INT, `currency_symbol` INT);

-- -----------------------------------------------------
-- View `jenbar`.`customer_balance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `jenbar`.`customer_balance`;
DROP VIEW IF EXISTS `jenbar`.`customer_balance` ;
USE `jenbar`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `jenbar`.`customer_balance` AS select `jenbar`.`customer`.`customer_id` AS `customer_id`,`jenbar`.`customer`.`user_name` AS `user_name`,`jenbar`.`customer`.`email_address` AS `email_address`,`jenbar`.`customer`.`first_name` AS `first_name`,`jenbar`.`customer`.`middle_name` AS `middle_name`,`jenbar`.`customer`.`last_name` AS `last_name`,`jenbar`.`cust_account`.`account_id` AS `account_id`,`jenbar`.`cust_account`.`quantity` AS `quantity`,`jenbar`.`cust_account`.`last_update` AS `last_update`,`jenbar`.`currency`.`currency_id` AS `currency_id`,`jenbar`.`currency`.`currency_short_name` AS `currency_short_name`,`jenbar`.`currency`.`currency_long_name` AS `currency_long_name`,`jenbar`.`currency`.`currency_symbol` AS `currency_symbol` from (((`jenbar`.`customer` join `jenbar`.`cust_acct_assoc` on((`jenbar`.`customer`.`customer_id` = `jenbar`.`cust_acct_assoc`.`customer_id`))) join `jenbar`.`cust_account` on((`jenbar`.`cust_account`.`account_id` = `jenbar`.`cust_acct_assoc`.`account_id`))) join `jenbar`.`currency` on((`jenbar`.`cust_account`.`currency_id` = `jenbar`.`currency`.`currency_id`)));

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
