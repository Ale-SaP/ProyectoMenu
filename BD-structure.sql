drop database IF exists proyecto_ecommerce;

CREATE DATABASE IF NOT exists proyecto_ecommerce;

use proyecto_ecommerce;

CREATE user if not exists 'django'@'localhost' IDENTIFIED BY 'django';
GRANT INDEX, ALTER, REFERENCES, SELECT, INSERT, UPDATE, DELETE, CREATE ON proyecto_ecommerce.* TO 'django'@'localhost';

CREATE TABLE
  organization (
    id_organization INT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID ()),
    name VARCHAR(255) NOT NULL
  );

CREATE TABLE
  sector (
    id_sector INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_organization INT,
    FOREIGN KEY (id_organization) REFERENCES organization (id_organization)
  );

CREATE TABLE
  catalog (
    id_catalog INT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID ()),
    name VARCHAR(255) NOT NULL,
    status INT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_organization INT,
    FOREIGN KEY (id_organization) REFERENCES organization (id_organization)
  );

CREATE TABLE
  category (
    id_category INT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID ()),
    name VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

CREATE TABLE
  sector_category (
    id_sector_category INT PRIMARY KEY AUTO_INCREMENT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_sector INT NOT NULL,
    id_category INT NOT NULL,
    FOREIGN KEY (id_sector) REFERENCES sector (id_sector),
    FOREIGN KEY (id_category) REFERENCES category (id_category)
  );

CREATE TABLE
  product (
    id_product INT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID ()),
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NULL,
    price DECIMAL(10, 2),
    status INT NULL,
    image_link_alt VARCHAR(255) NULL,
    image_link VARCHAR(255) NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_catalog INT,
    FOREIGN KEY (id_catalog) REFERENCES catalog (id_catalog)
  );

CREATE TABLE
  client (
    id_client INT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID ()),
    name VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

CREATE TABLE
  `order` (
    id_order INT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID ()),
    order_date DATE NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_client INT,
    FOREIGN KEY (id_client) REFERENCES client (id_client)
  );

CREATE TABLE
  payment_method (
    id_payment_method INT PRIMARY KEY AUTO_INCREMENT,
    method_name VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

CREATE TABLE
  payment_status (
    id_payment_status INT PRIMARY KEY AUTO_INCREMENT,
    status_name VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

CREATE TABLE
  receipt (
    id_receipt INT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL DEFAULT (UUID ()),
    receipt_date DATE NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_order INT,
    id_payment_method INT,
    id_payment_status INT,
    FOREIGN KEY (id_order) REFERENCES `order` (id_order),
    FOREIGN KEY (id_payment_method) REFERENCES payment_method (id_payment_method),
    FOREIGN KEY (id_payment_status) REFERENCES payment_status (id_payment_status)
  );

CREATE TABLE
  org_config (
    id_org_config INT PRIMARY KEY AUTO_INCREMENT,
    nombre_tienda VARCHAR(255) NULL,
    contenido_inicial INT NULL,
    logo_url VARCHAR(255) NULL,
    descripcion_logo VARCHAR(255) NULL,
    texto_superior VARCHAR(255) NULL,
    horario_atencion VARCHAR(255) NULL,
    telefono_contacto VARCHAR(50) NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_organization INT,
    FOREIGN KEY (id_organization) REFERENCES organization (id_organization)
  );

CREATE TABLE
  detail (
    id_detail INT PRIMARY KEY AUTO_INCREMENT,
    quantity INT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_order INT,
    id_product INT,
    FOREIGN KEY (id_order) REFERENCES `order` (id_order),
    FOREIGN KEY (id_product) REFERENCES product (id_product)
  );

CREATE TABLE
  product_category (
    id_product_category INT PRIMARY KEY AUTO_INCREMENT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_category INT NOT NULL,
    id_product INT NOT NULL,
    FOREIGN KEY (id_category) REFERENCES category (id_category),
    FOREIGN KEY (id_product) REFERENCES product (id_product)
  );


DELIMITER $$

CREATE PROCEDURE search_products(IN search_term VARCHAR(255))
BEGIN
    SELECT DISTINCT
        p.id_product,
        p.uuid,
        p.name,
        p.description,
        p.price,
        p.status,
        p.image_link_alt,
        p.image_link,
        p.creation_date,
        p.id_catalog
    FROM
        product p
    LEFT JOIN
        product_category pc ON p.id_product = pc.id_product
    LEFT JOIN
        category c ON pc.id_category = c.id_category
    WHERE
        p.name LIKE CONCAT('%', search_term, '%')
        OR p.description LIKE CONCAT('%', search_term, '%')
        OR c.name LIKE CONCAT('%', search_term, '%');
END $$

DELIMITER ;