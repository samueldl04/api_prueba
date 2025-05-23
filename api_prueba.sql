-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-05-2025 a las 03:36:23
-- Versión del servidor: 8.0.42
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `api_prueba`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `company`
--

CREATE TABLE `company` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `cif` varchar(9) NOT NULL,
  `address` varchar(200) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `company`
--

INSERT INTO `company` (`id`, `name`, `cif`, `address`, `phone`, `active`) VALUES
(1, 'Tech Solutions S.L.', 'B12345678', 'Calle Falsa 123, Madrid', '912345678', 1),
(2, 'Innovate Corp.', 'B87654321', 'Av. de la Ciencia 45, Barcelona', '934567890', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `device`
--

CREATE TABLE `device` (
  `id` int NOT NULL,
  `ip_device` varchar(20) NOT NULL,
  `device_status_id` int NOT NULL,
  `id_company` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `device`
--

INSERT INTO `device` (`id`, `ip_device`, `device_status_id`, `id_company`) VALUES
(1, '192.168.1.10', 1, 1),
(2, '192.168.1.11', 2, 1),
(3, '192.168.2.10', 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `device_status`
--

CREATE TABLE `device_status` (
  `id` int NOT NULL,
  `name` varchar(15) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `device_status`
--

INSERT INTO `device_status` (`id`, `name`, `description`) VALUES
(1, 'Activo', 'El dispositivo está en funcionamiento'),
(2, 'Inactivo', 'El dispositivo está desconectado'),
(3, 'Mantenimiento', 'El dispositivo está siendo revisado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `employee`
--

CREATE TABLE `employee` (
  `id` int NOT NULL,
  `dni` varchar(9) NOT NULL,
  `email` varchar(128) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `first_name` varchar(15) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `status` tinyint(1) DEFAULT '0',
  `company_id` int DEFAULT NULL,
  `role_id` int NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `employee`
--

INSERT INTO `employee` (`id`, `dni`, `email`, `phone_number`, `first_name`, `last_name`, `password`, `status`, `company_id`, `role_id`, `active`) VALUES
(1, '1', 'juan@example.com', '600111222', 'sada', 'Pérez', '1', 1, 1, 1, 1),
(2, '2', 'ana@example.com', '600333444', 'Ana', 'Gómez', '2', 1, 1, 2, 1),
(3, '11223344C', 'luis@example.com', '600555666', 'Luis', 'Martínez', 'hashed_password3', 0, 2, 0, 1),
(4, 'q', '43381094N', 'q', 'q', 'q', '1234567Aa', 1, 1, 1, 0),
(5, '', '43381094N', '', '', '', '1234567Aa', 1, 1, 1, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `record`
--

CREATE TABLE `record` (
  `id` int NOT NULL,
  `company_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `room_id` int NOT NULL,
  `record_type_id` int NOT NULL,
  `details` varchar(100) DEFAULT NULL,
  `date_record` date NOT NULL,
  `time_record` time NOT NULL DEFAULT (curtime())
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `record`
--

INSERT INTO `record` (`id`, `company_id`, `user_id`, `room_id`, `record_type_id`, `details`, `date_record`, `time_record`) VALUES
(1, 1, 1, 1, 1, '', '2024-05-01', '19:26:22'),
(2, 1, 2, 2, 1, '', '2024-05-01', '19:26:22'),
(3, 1, 1, 1, 2, '', '2024-05-01', '19:26:22'),
(4, 2, 3, 3, 1, '', '2024-05-02', '19:26:22'),
(5, 1, 1, 1, 2, '', '2025-05-22', '16:10:14'),
(6, 1, NULL, 1, 2, '', '2025-05-22', '16:11:34'),
(7, 1, NULL, 1, 2, '', '2025-05-22', '16:31:49'),
(8, 1, 1, 1, 3, '', '2025-05-22', '16:31:55'),
(9, 1, NULL, 2, 2, '', '2025-05-22', '16:49:25'),
(10, 1, NULL, 2, 2, '', '2025-05-22', '16:52:22'),
(11, 1, NULL, 2, 2, '', '2025-05-22', '17:22:29'),
(12, 1, 1, 2, 3, '', '2025-05-22', '17:22:37'),
(13, 1, NULL, 1, 2, '', '2025-05-22', '18:11:37'),
(14, 1, 1, 2, 4, '', '2025-05-22', '18:19:35'),
(15, 1, NULL, 2, 2, '', '2025-05-22', '18:19:54'),
(16, 1, 1, 2, 3, '', '2025-05-22', '18:20:00'),
(17, 1, 1, 2, 4, '', '2025-05-22', '18:20:05'),
(18, 1, 1, 2, 4, '', '2025-05-22', '18:28:22'),
(19, 1, NULL, 2, 2, '', '2025-05-22', '18:28:23'),
(20, 1, 1, 2, 3, '', '2025-05-22', '18:28:30'),
(21, 1, 1, 2, 4, '', '2025-05-22', '18:28:37'),
(22, 1, 1, 2, 4, '', '2025-05-22', '18:28:38'),
(23, 1, 1, 2, 4, '', '2025-05-22', '18:28:42'),
(24, 1, NULL, 1, 2, '', '2025-05-22', '18:33:24'),
(25, 1, 1, 1, 3, '', '2025-05-22', '18:33:31'),
(26, 1, 1, 1, 4, '', '2025-05-22', '18:33:41'),
(27, 1, NULL, 1, 2, '', '2025-05-22', '18:43:53'),
(28, 1, 1, 1, 3, '', '2025-05-22', '18:44:04'),
(29, 1, 1, 1, 4, '', '2025-05-22', '18:44:06'),
(30, 1, NULL, 1, 2, '', '2025-05-22', '22:58:42'),
(31, 1, NULL, 1, 2, '', '2025-05-23', '01:33:14'),
(32, 1, 1, 1, 3, '', '2025-05-23', '01:33:24'),
(33, 1, 1, 1, 4, '', '2025-05-23', '01:34:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `record_type`
--

CREATE TABLE `record_type` (
  `id` int NOT NULL,
  `name` varchar(15) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `record_type`
--

INSERT INTO `record_type` (`id`, `name`, `description`) VALUES
(1, 'Sin estado', 'Registro de entrada al edificio'),
(2, 'Llamada', 'Usuario pide asistencia'),
(3, 'Asignado', 'empleado asignado a la llamada'),
(4, 'Presencia', 'empleado se presenta en la cama');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `role_employee`
--

CREATE TABLE `role_employee` (
  `id` int NOT NULL,
  `name` varchar(15) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `role_employee`
--

INSERT INTO `role_employee` (`id`, `name`, `description`) VALUES
(1, 'admin', 'Administrator role with full system access'),
(2, 'employee', 'Regular employee role with limited access');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rooms`
--

CREATE TABLE `rooms` (
  `id` int NOT NULL,
  `floor` int NOT NULL,
  `room_number` int NOT NULL,
  `call_point` varchar(10) NOT NULL,
  `detail_call_point` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `company_id` int NOT NULL,
  `ip_room` varchar(15) DEFAULT NULL COMMENT 'IP address of the room'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `rooms`
--

INSERT INTO `rooms` (`id`, `floor`, `room_number`, `call_point`, `detail_call_point`, `company_id`, `ip_room`) VALUES
(1, 1, 101, 'CP101', 'Punto 1', 1, NULL),
(2, 2, 202, 'CP202', 'Punto 2', 1, NULL),
(3, 1, 103, 'CP103', 'Punto 3', 2, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cif` (`cif`);

--
-- Indices de la tabla `device`
--
ALTER TABLE `device`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_status_id` (`device_status_id`),
  ADD KEY `id_company` (`id_company`);

--
-- Indices de la tabla `device_status`
--
ALTER TABLE `device_status`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_employee_role` (`role_id`),
  ADD KEY `fk_employee_company` (`company_id`);

--
-- Indices de la tabla `record`
--
ALTER TABLE `record`
  ADD PRIMARY KEY (`id`),
  ADD KEY `company_id` (`company_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `room_id` (`room_id`),
  ADD KEY `record_type_id` (`record_type_id`);

--
-- Indices de la tabla `record_type`
--
ALTER TABLE `record_type`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `role_employee`
--
ALTER TABLE `role_employee`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`),
  ADD KEY `company_id` (`company_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `company`
--
ALTER TABLE `company`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `device`
--
ALTER TABLE `device`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `device_status`
--
ALTER TABLE `device_status`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `record`
--
ALTER TABLE `record`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `record_type`
--
ALTER TABLE `record_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `role_employee`
--
ALTER TABLE `role_employee`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `device`
--
ALTER TABLE `device`
  ADD CONSTRAINT `device_ibfk_1` FOREIGN KEY (`device_status_id`) REFERENCES `device_status` (`id`),
  ADD CONSTRAINT `device_ibfk_2` FOREIGN KEY (`id_company`) REFERENCES `company` (`id`);

--
-- Filtros para la tabla `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`),
  ADD CONSTRAINT `fk_employee_company` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_employee_role` FOREIGN KEY (`role_id`) REFERENCES `role_employee` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Filtros para la tabla `record`
--
ALTER TABLE `record`
  ADD CONSTRAINT `record_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`),
  ADD CONSTRAINT `record_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `employee` (`id`),
  ADD CONSTRAINT `record_ibfk_3` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`),
  ADD CONSTRAINT `record_ibfk_4` FOREIGN KEY (`record_type_id`) REFERENCES `record_type` (`id`);

--
-- Filtros para la tabla `rooms`
--
ALTER TABLE `rooms`
  ADD CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
