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

 Date: 12/08/2025 22:03:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for role_users
-- ----------------------------
DROP TABLE IF EXISTS `role_users`;
CREATE TABLE `role_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_role_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of role_users
-- ----------------------------
BEGIN;
INSERT INTO `role_users` (`id`, `name`) VALUES (1, 'SUPER_ADMIN');
INSERT INTO `role_users` (`id`, `name`) VALUES (2, 'ADMIN_VERIFIKATOR');
INSERT INTO `role_users` (`id`, `name`) VALUES (3, 'ADMIN_KONTRIBUTOR');
INSERT INTO `role_users` (`id`, `name`) VALUES (4, 'MITRA_BISNIS');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
