/*
Navicat MySQL Data Transfer

Source Server         : 10.66.32.18
Source Server Version : 50538
Source Host           : 10.66.32.18:3306
Source Database       : mylibvirt

Target Server Type    : MYSQL
Target Server Version : 50538
File Encoding         : 65001

Date: 2014-11-12 10:59:02
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for libvirtBandW
-- ----------------------------
DROP TABLE IF EXISTS `libvirtBandW`;
CREATE TABLE `libvirtBandW` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `uuidstring` varchar(45) NOT NULL,
  `timestamp` int(20) NOT NULL,
  `outputBandW` bigint(20) DEFAULT NULL,
  `inputBandW` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for libvirtDisk
-- ----------------------------
DROP TABLE IF EXISTS `libvirtDisk`;
CREATE TABLE `libvirtDisk` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `uuidstring` varchar(45) NOT NULL,
  `timestamp` int(20) NOT NULL,
  `usage` bigint(20) DEFAULT NULL,
  `capacity` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`,`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for libvirtMem
-- ----------------------------
DROP TABLE IF EXISTS `libvirtMem`;
CREATE TABLE `libvirtMem` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `uuidstring` varchar(45) NOT NULL,
  `timestamp` int(20) NOT NULL,
  `memTotal` bigint(20) DEFAULT NULL,
  `memSwap` bigint(20) DEFAULT NULL,
  `memRss` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`,`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for libvirtParameter
-- ----------------------------
DROP TABLE IF EXISTS `libvirtParameter`;
CREATE TABLE `libvirtParameter` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `uuidstring` varchar(45) NOT NULL,
  `interUUID` varchar(50) DEFAULT NULL,
  `vInterfacePath` varchar(20) DEFAULT NULL,
  `vDiskPath` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
