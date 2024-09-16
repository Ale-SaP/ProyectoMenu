create database proyecto_menu;

CREATE USER 'django'@'localhost' IDENTIFIED BY 'django';
GRANT INDEX, ALTER, REFERENCES, SELECT, INSERT, UPDATE, DELETE ON proyecto_menu.* TO 'django'@'localhost';
grant create on proyecto_menu.* to 'django'@'localhost';

use proyecto_menu;

CREATE TABLE IF NOT EXISTS `organization` (
  `id_org` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `location` VARCHAR(255) NOT NULL,
  `status` BOOLEAN NOT NULL DEFAULT TRUE,
  `attendant` VARCHAR(255) 
);

CREATE TABLE IF NOT EXISTS `org_configs` (
  `id_org_configs` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `id_org` INT NOT NULL,
  `json_config` JSON NOT NULL,
  `org_configs` INDEX (`id_org`);
);

CREATE TABLE IF NOT EXISTS `menu` (
  `id_menu` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100),
  `creation_date` DATE DEFAULT NULL,
  `status` BOOLEAN DEFAULT TRUE,
  `id_org` INT NOT NULL
);

CREATE TABLE IF NOT EXISTS `menu_product` (
  `id_menu` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `id_product` INT NOT NULL
);

CREATE TABLE IF NOT EXISTS `product` (
  `id_product` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `description` VARCHAR(255),
  `price` DECIMAL(10,2) NOT NULL,
  `status` BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS `category` (
  `id_category` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL
  `svg_path` varchar(255);
);

CREATE TABLE IF NOT EXISTS `product_category` (
  `id_category` INT NOT NULL,
  `id_product` INT NOT NULL PRIMARY KEY
);

ALTER TABLE `organization` ADD CONSTRAINT `organization_id_org_fk` FOREIGN KEY (`id_org`) REFERENCES `org_configs` (`id_org`);
ALTER TABLE `menu` ADD CONSTRAINT `menu_id_menu_fk` FOREIGN KEY (`id_menu`) REFERENCES `menu_product` (`id_menu`);
ALTER TABLE `menu_product` ADD CONSTRAINT `menu_product_id_product_fk` FOREIGN KEY (`id_product`) REFERENCES `product` (`id_product`);
ALTER TABLE `menu` ADD CONSTRAINT `menu_id_org_fk` FOREIGN KEY (`id_org`) REFERENCES `organization` (`id_org`);
ALTER TABLE `product` ADD CONSTRAINT `product_id_product_fk` FOREIGN KEY (`id_product`) REFERENCES `product_category` (`id_product`);
ALTER TABLE `product_category` ADD CONSTRAINT `product_category_id_category_fk` FOREIGN KEY (`id_category`) REFERENCES `category` (`id_category`);