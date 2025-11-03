-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema esquema_estudiantes_cursos
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema_estudiantes_cursos` ;

-- -----------------------------------------------------
-- Schema esquema_estudiantes_cursos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema_estudiantes_cursos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
-- -----------------------------------------------------
-- Schema esquema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema` ;

-- -----------------------------------------------------
-- Schema esquema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `esquema_estudiantes_cursos` ;

-- -----------------------------------------------------
-- Table `esquema_estudiantes_cursos`.`cursos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `esquema_estudiantes_cursos`.`cursos` ;

CREATE TABLE IF NOT EXISTS `esquema_estudiantes_cursos`.`cursos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NOT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  `create_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `esquema_estudiantes_cursos`.`estudiantes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `esquema_estudiantes_cursos`.`estudiantes` ;

CREATE TABLE IF NOT EXISTS `esquema_estudiantes_cursos`.`estudiantes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NOT NULL,
  `apellido` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `curso_id` INT NOT NULL,
  `create_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE,
  INDEX `curso_id` (`curso_id` ASC) VISIBLE,
  CONSTRAINT `estudiantes_ibfk_1`
    FOREIGN KEY (`curso_id`)
    REFERENCES `esquema_estudiantes_cursos`.`cursos` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

USE `esquema` ;

-- -----------------------------------------------------
-- Table `esquema`.`usuarios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `esquema`.`usuarios` ;

CREATE TABLE IF NOT EXISTS `esquema`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
