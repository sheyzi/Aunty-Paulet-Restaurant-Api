-- upgrade --
CREATE TABLE IF NOT EXISTS "payments" (
    "transaction_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "amount" VARCHAR(10) NOT NULL,
    "tx_ref" VARCHAR(30) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
-- downgrade --
DROP TABLE IF EXISTS "payments";
