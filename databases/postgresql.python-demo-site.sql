-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               PostgreSQL 18.3 on x86_64-windows, compiled by msvc-19.44.35225, 64-bit
-- Server OS:                    
-- HeidiSQL Version:             12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table public.contact_us
CREATE TABLE IF NOT EXISTS "contact_us" (
	"id" SERIALNOT NULL,
	"client_ip" VARCHAR(255) NOT NULL,
	"first_name" VARCHAR(255) NOT NULL,
	"last_name" VARCHAR(255) NOT NULL,
	"email" VARCHAR(255) NOT NULL,
	"subject" VARCHAR(255) NOT NULL,
	"message" TEXT NULL DEFAULT NULL,
	"created_at" TIMESTAMP NULL DEFAULT NULL,
	"updated_at" TIMESTAMP NULL DEFAULT NULL,
	PRIMARY KEY ("id")
);

-- Dumping data for table public.contact_us: -1 rows
INSERT INTO "contact_us" ("id", "client_ip", "first_name", "last_name", "email", "subject", "message", "created_at", "updated_at") VALUES
	(1, '127.0.0.1', 'Sasa', 'Rakic', 'rakics@gmsil.com', 'Product Question', 'An test....', '2026-05-18 04:00:36', NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
