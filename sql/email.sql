/*
 Navicat Premium Data Transfer

 Source Server         : 本地
 Source Server Type    : MySQL
 Source Server Version : 80032
 Source Host           : localhost:3306
 Source Schema         : email

 Target Server Type    : MySQL
 Target Server Version : 80033
 File Encoding         : 65001

 Date: 25/08/2023 11:39:56
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for body
-- ----------------------------
DROP TABLE IF EXISTS `body`;
CREATE TABLE `body`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `str_body` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '邮件正文',
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '语种',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for end
-- ----------------------------
DROP TABLE IF EXISTS `end`;
CREATE TABLE `end`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '结尾名称',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '结尾附件',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '结尾内容',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for info
-- ----------------------------
DROP TABLE IF EXISTS `info`;
CREATE TABLE `info`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '附件地址',
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '语种',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for title
-- ----------------------------
DROP TABLE IF EXISTS `title`;
CREATE TABLE `title`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `str_title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '邮件正文',
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品',
  `language` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '语种',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '邮箱账号',
  `pwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '邮箱授权码',
  `str_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '邮箱类型',
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- View structure for get_language
-- ----------------------------
DROP VIEW IF EXISTS `get_language`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `get_language` AS select substring_index(substring_index(`info`.`language`,',',(`b`.`help_topic_id` + 1)),',',-(1)) AS `language` from (`info` join `mysql`.`help_topic` `b` on((`b`.`help_topic_id` < ((length(`info`.`language`) - length(replace(`info`.`language`,',',''))) + 1)))) union select substring_index(substring_index(`body`.`language`,',',(`b`.`help_topic_id` + 1)),',',-(1)) AS `language` from (`body` join `mysql`.`help_topic` `b` on((`b`.`help_topic_id` < ((length(`body`.`language`) - length(replace(`body`.`language`,',',''))) + 1)))) union select substring_index(substring_index(`title`.`language`,',',(`b`.`help_topic_id` + 1)),',',-(1)) AS `language` from (`title` join `mysql`.`help_topic` `b` on((`b`.`help_topic_id` < ((length(`title`.`language`) - length(replace(`title`.`language`,',',''))) + 1))));

-- ----------------------------
-- View structure for get_product
-- ----------------------------
DROP VIEW IF EXISTS `get_product`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `get_product` AS select substring_index(substring_index(`user`.`product`,',',(`b`.`help_topic_id` + 1)),',',-(1)) AS `product` from (`user` join `mysql`.`help_topic` `b` on((`b`.`help_topic_id` < ((length(`user`.`product`) - length(replace(`user`.`product`,',',''))) + 1)))) union select substring_index(substring_index(`info`.`product`,',',(`b`.`help_topic_id` + 1)),',',-(1)) AS `product` from (`info` join `mysql`.`help_topic` `b` on((`b`.`help_topic_id` < ((length(`info`.`product`) - length(replace(`info`.`product`,',',''))) + 1)))) union select substring_index(substring_index(`body`.`product`,',',(`b`.`help_topic_id` + 1)),',',-(1)) AS `product` from (`body` join `mysql`.`help_topic` `b` on((`b`.`help_topic_id` < ((length(`body`.`product`) - length(replace(`body`.`product`,',',''))) + 1)))) union select substring_index(substring_index(`title`.`product`,',',(`b`.`help_topic_id` + 1)),',',-(1)) AS `product` from (`title` join `mysql`.`help_topic` `b` on((`b`.`help_topic_id` < ((length(`title`.`product`) - length(replace(`title`.`product`,',',''))) + 1))));

SET FOREIGN_KEY_CHECKS = 1;
