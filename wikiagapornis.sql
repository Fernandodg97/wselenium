-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 28, 2025 at 04:21 PM
-- Server version: 8.0.40-0ubuntu0.24.04.1
-- PHP Version: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wikiagapornis`
--

-- --------------------------------------------------------

--
-- Table structure for table `Avistamientos`
--

CREATE TABLE `Avistamientos` (
  `id_pajaro` int NOT NULL,
  `id_lugar` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Datos`
--

CREATE TABLE `Datos` (
  `id_clave` int NOT NULL,
  `id_pajaro` int NOT NULL,
  `estado_conservacion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `dieta` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `poblacion_europea` text,
  `pluma` text,
  `longitud` text,
  `peso` text,
  `envergadura` text,
  `habitats` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Lugares`
--

CREATE TABLE `Lugares` (
  `id_lugar` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `ubicacion` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Pajaro`
--

CREATE TABLE `Pajaro` (
  `id_pajaro` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `nombre_cientifico` varchar(150) NOT NULL,
  `grupo` varchar(50) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `como_identificar` text,
  `canto_audio` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Avistamientos`
--
ALTER TABLE `Avistamientos`
  ADD PRIMARY KEY (`id_pajaro`,`id_lugar`),
  ADD KEY `id_lugar` (`id_lugar`);

--
-- Indexes for table `Datos`
--
ALTER TABLE `Datos`
  ADD PRIMARY KEY (`id_clave`),
  ADD KEY `id_pajaro` (`id_pajaro`);

--
-- Indexes for table `Lugares`
--
ALTER TABLE `Lugares`
  ADD PRIMARY KEY (`id_lugar`);

--
-- Indexes for table `Pajaro`
--
ALTER TABLE `Pajaro`
  ADD PRIMARY KEY (`id_pajaro`),
  ADD KEY `id_pajaro` (`id_pajaro`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Datos`
--
ALTER TABLE `Datos`
  MODIFY `id_clave` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Lugares`
--
ALTER TABLE `Lugares`
  MODIFY `id_lugar` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Pajaro`
--
ALTER TABLE `Pajaro`
  MODIFY `id_pajaro` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Avistamientos`
--
ALTER TABLE `Avistamientos`
  ADD CONSTRAINT `Avistamientos_ibfk_1` FOREIGN KEY (`id_pajaro`) REFERENCES `Pajaro` (`id_pajaro`) ON DELETE CASCADE,
  ADD CONSTRAINT `Avistamientos_ibfk_2` FOREIGN KEY (`id_lugar`) REFERENCES `Lugares` (`id_lugar`) ON DELETE CASCADE;

--
-- Constraints for table `Datos`
--
ALTER TABLE `Datos`
  ADD CONSTRAINT `Datos_ibfk_1` FOREIGN KEY (`id_pajaro`) REFERENCES `Pajaro` (`id_pajaro`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
