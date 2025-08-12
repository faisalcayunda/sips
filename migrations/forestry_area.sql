/*
 Navicat Premium Dump SQL

 Source Server         : SIPS SUMBAR Staging
 Source Server Type    : MySQL
 Source Server Version : 80042 (8.0.42-0ubuntu0.22.04.1)
 Source Host           : 103.235.75.47:3306
 Source Schema         : clone_sipssumbar

 Target Server Type    : MySQL
 Target Server Version : 80042 (8.0.42-0ubuntu0.22.04.1)
 File Encoding         : 65001

 Date: 12/08/2025 22:03:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for forestry_area
-- ----------------------------
DROP TABLE IF EXISTS `forestry_area`;
CREATE TABLE `forestry_area` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(512) NOT NULL,
  `abbreviation` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of forestry_area
-- ----------------------------
BEGIN;
INSERT INTO `forestry_area` (`id`, `name`, `abbreviation`) VALUES (1, 'Hutan Lindung', 'HL');
INSERT INTO `forestry_area` (`id`, `name`, `abbreviation`) VALUES (2, 'Hutan Konservasi', 'HK');
INSERT INTO `forestry_area` (`id`, `name`, `abbreviation`) VALUES (3, 'Hutan Produksi Tetap', 'HP');
INSERT INTO `forestry_area` (`id`, `name`, `abbreviation`) VALUES (4, 'Hutan Produksi Terbatas', 'HPT');
INSERT INTO `forestry_area` (`id`, `name`, `abbreviation`) VALUES (5, 'Hutan Produksi yang dapat di Konservasi', 'HPK');
INSERT INTO `forestry_area` (`id`, `name`, `abbreviation`) VALUES (6, 'Area Penggunaan Lain', 'APL');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
