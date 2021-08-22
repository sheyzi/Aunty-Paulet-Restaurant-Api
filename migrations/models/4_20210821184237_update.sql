-- upgrade --
ALTER TABLE "storesettings" ADD "secret_key" VARCHAR(500) NOT NULL  DEFAULT 'FLWSECK-7df341197189906ab0dd5c045b057216-X';
ALTER TABLE "storesettings" ADD "public_key" VARCHAR(500) NOT NULL  DEFAULT 'FLWPUBK-8d86cd80110eab28ded75457e92d47f4-X';
-- downgrade --
ALTER TABLE "storesettings" DROP COLUMN "secret_key";
ALTER TABLE "storesettings" DROP COLUMN "public_key";
