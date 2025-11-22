-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-11-2025 a las 23:32:36
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `casas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `admins`
--

CREATE TABLE `admins` (
  `id_admin` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(120) NOT NULL,
  `contraseña` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `admins`
--

INSERT INTO `admins` (`id_admin`, `nombre`, `correo`, `contraseña`) VALUES
(1, 'Administrador Principal', 'admin@casasaltillo.com', 'admin123');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `casas`
--

CREATE TABLE `casas` (
  `id_casa` int(11) NOT NULL,
  `id_locacion` int(11) NOT NULL,
  `latitud` decimal(10,6) NOT NULL,
  `longitud` decimal(10,6) NOT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `costo` decimal(12,2) NOT NULL,
  `recamaras` int(11) NOT NULL,
  `baños` int(11) NOT NULL,
  `estatus_venta` enum('En Venta','Vendida') NOT NULL DEFAULT 'En Venta',
  `fotos` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `casas`
--

INSERT INTO `casas` (`id_casa`, `id_locacion`, `latitud`, `longitud`, `codigo_postal`, `costo`, `recamaras`, `baños`, `estatus_venta`, `fotos`) VALUES
(1, 1, 25.438056, -100.983333, '25000', 1450000.00, 2, 1, 'En Venta', ''),
(2, 2, 25.556357, -100.947549, '25900', 1550000.00, 3, 2, 'En Venta', ''),
(3, 3, 25.445891, -100.857489, '25350', 2680000.00, 4, 3, 'Vendida', ''),
(4, 4, 25.703790, -100.286518, '67130', 3200000.00, 3, 2, 'En Venta', ''),
(5, 5, 25.807640, -100.595940, '66023', 1780000.00, 3, 2, 'En Venta', ''),
(6, 6, 25.838090, -100.313200, '66072', 1600000.00, 2, 1, 'Vendida', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `catalogo_locacion`
--

CREATE TABLE `catalogo_locacion` (
  `id_locacion` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `catalogo_locacion`
--

INSERT INTO `catalogo_locacion` (`id_locacion`, `nombre`) VALUES
(3, 'Arteaga Coahuila'),
(6, 'Escobedo Nuevo León'),
(5, 'García Nuevo León'),
(4, 'Monterrey Nuevo León'),
(2, 'Ramos Arizpe Coahuila'),
(1, 'Saltillo Coahuila');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(120) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `correo`, `telefono`) VALUES
(1, 'Carlos Medina', 'carlos.medina@example.com', '8442001122'),
(2, 'Ana López', 'ana.lopez@example.com', '8441552983'),
(3, 'Luis Herrera', 'luis.herrera@example.com', '8441789021');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `casas`
--
ALTER TABLE `casas`
  ADD PRIMARY KEY (`id_casa`),
  ADD KEY `idx_locacion` (`id_locacion`),
  ADD KEY `idx_codigo_postal` (`codigo_postal`),
  ADD KEY `idx_estatus_venta` (`estatus_venta`),
  ADD KEY `idx_costo` (`costo`);

--
-- Indices de la tabla `catalogo_locacion`
--
ALTER TABLE `catalogo_locacion`
  ADD PRIMARY KEY (`id_locacion`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `admins`
--
ALTER TABLE `admins`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `casas`
--
ALTER TABLE `casas`
  MODIFY `id_casa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `catalogo_locacion`
--
ALTER TABLE `catalogo_locacion`
  MODIFY `id_locacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=223;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `casas`
--
ALTER TABLE `casas`
  ADD CONSTRAINT `casas_ibfk_1` FOREIGN KEY (`id_locacion`) REFERENCES `catalogo_locacion` (`id_locacion`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
