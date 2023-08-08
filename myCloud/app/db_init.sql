-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema memcache
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `memcache` ;

-- -----------------------------------------------------
-- Schema memcache
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `memcache` DEFAULT CHARACTER SET utf8 ;
USE `memcache` ;

-- -----------------------------------------------------
-- Table `memcache`.`config`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `memcache`.`config` ;

CREATE TABLE IF NOT EXISTS `memcache`.`config` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `policy` VARCHAR(45) NOT NULL,
  `capacity` DECIMAL(5,2),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;




SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `memcache`.`config`
-- -----------------------------------------------------
START TRANSACTION;
USE `memcache`;
INSERT INTO `memcache`.`config` (`id`, `policy`, `capacity`) VALUES (1, 'Random', 10);

COMMIT;




DROP USER IF EXISTS 'ece1779'@'localhost';
CREATE USER 'ece1779'@'localhost' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON memcache.* TO 'ece1779'@'localhost';

