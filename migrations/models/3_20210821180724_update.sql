-- upgrade --
CREATE TABLE IF NOT EXISTS "storesettings" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "encryption_key" VARCHAR(500) NOT NULL
);
-- downgrade --
DROP TABLE IF EXISTS "storesettings";
