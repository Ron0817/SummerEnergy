-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema estore
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `estore` ;

-- -----------------------------------------------------
-- Schema estore
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `estore` DEFAULT CHARACTER SET utf8 ;
USE `estore` ;

-- -----------------------------------------------------
-- Table `estore`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `estore`.`category` ;

CREATE TABLE IF NOT EXISTS `estore`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `estore`.`product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `estore`.`product` ;

CREATE TABLE IF NOT EXISTS `estore`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `price` VARCHAR(45) NOT NULL,
  `quantity` INT NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_products_category_idx` (`category_id` ASC),
  CONSTRAINT `fk_products_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `estore`.`category` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `estore`.`customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `estore`.`customer` ;

CREATE TABLE IF NOT EXISTS `estore`.`customer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `estore`.`customer_has_product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `estore`.`customer_has_product` ;

CREATE TABLE IF NOT EXISTS `estore`.`customer_has_product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_customer_has_product_product1_idx` (`product_id` ASC),
  INDEX `fk_customer_has_product_customer1_idx` (`customer_id` ASC),
  CONSTRAINT `fk_customer_has_product_customer1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `estore`.`customer` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_customer_has_product_product1`
    FOREIGN KEY (`product_id`)
    REFERENCES `estore`.`product` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `estore`.`category`
-- -----------------------------------------------------
START TRANSACTION;
USE `estore`;
INSERT INTO `estore`.`category` (`id`, `name`) VALUES (1, 'Video Games');
INSERT INTO `estore`.`category` (`id`, `name`) VALUES (2, 'Movies');

COMMIT;


-- -----------------------------------------------------
-- Data for table `estore`.`product`
-- -----------------------------------------------------
START TRANSACTION;
USE `estore`;
INSERT INTO `estore`.`product` (`id`, `name`, `price`, `quantity`, `category_id`) VALUES (1, 'Pac-Man', '10', 5, 1);
INSERT INTO `estore`.`product` (`id`, `name`, `price`, `quantity`, `category_id`) VALUES (2, 'Donkey Kong', '15', 3, 1);
INSERT INTO `estore`.`product` (`id`, `name`, `price`, `quantity`, `category_id`) VALUES (3, 'Galaga', '20', 2, 1);
INSERT INTO `estore`.`product` (`id`, `name`, `price`, `quantity`, `category_id`) VALUES (4, 'Tetris', '12', 4, 1);
INSERT INTO `estore`.`product` (`id`, `name`, `price`, `quantity`, `category_id`) VALUES (5, 'Casa Blanca', '17', 7, 2);
INSERT INTO `estore`.`product` (`id`, `name`, `price`, `quantity`, `category_id`) VALUES (6, 'Gone with the Wind', '25', 3, 2);

COMMIT;


-- -----------------------------------------------------
-- Data for table `estore`.`customer`
-- -----------------------------------------------------
START TRANSACTION;
USE `estore`;
INSERT INTO `estore`.`customer` (`id`, `name`, `email`) VALUES (1, 'Homer Simpson', 'homer.simpson@mail.utronto.ca');
INSERT INTO `estore`.`customer` (`id`, `name`, `email`) VALUES (2, 'Marge Simpson', 'marge.simpson@mail.utoronto.ca');

COMMIT;


-- -----------------------------------------------------
-- Data for table `estore`.`customer_has_product`
-- -----------------------------------------------------
START TRANSACTION;
USE `estore`;
INSERT INTO `estore`.`customer_has_product` (`id`, `customer_id`, `product_id`) VALUES (1, 1, 2);
INSERT INTO `estore`.`customer_has_product` (`id`, `customer_id`, `product_id`) VALUES (2, 1, 3);
INSERT INTO `estore`.`customer_has_product` (`id`, `customer_id`, `product_id`) VALUES (3, 1, 5);
INSERT INTO `estore`.`customer_has_product` (`id`, `customer_id`, `product_id`) VALUES (4, 2, 2);
INSERT INTO `estore`.`customer_has_product` (`id`, `customer_id`, `product_id`) VALUES (5, 2, 4);

COMMIT;



DROP USER IF EXISTS 'ece1779'@'localhost';
CREATE USER 'ece1779'@'localhost' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON estore.* TO 'ece1779'@'localhost';

