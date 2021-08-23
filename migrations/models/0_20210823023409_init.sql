-- upgrade --
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(20) NOT NULL,
    "slug" VARCHAR(50) NOT NULL UNIQUE,
    "image_url" VARCHAR(500) NOT NULL  DEFAULT 'https://res.cloudinary.com/sheyzisilver/image/upload/v1628729409/placeholder_rl2wsr.png',
    "date_created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "product" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "slug" VARCHAR(60) NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "image_url" VARCHAR(500) NOT NULL  DEFAULT 'https://res.cloudinary.com/sheyzisilver/image/upload/v1628729409/placeholder_rl2wsr.png',
    "is_featured" BOOL NOT NULL  DEFAULT False,
    "date_created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "storesettings" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "encryption_key" VARCHAR(500) NOT NULL,
    "public_key" VARCHAR(500) NOT NULL  DEFAULT 'FLWPUBK-8d86cd80110eab28ded75457e92d47f4-X',
    "secret_key" VARCHAR(500) NOT NULL  DEFAULT 'FLWSECK-7df341197189906ab0dd5c045b057216-X'
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(200) NOT NULL UNIQUE,
    "email" VARCHAR(200) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_admin" BOOL NOT NULL  DEFAULT False,
    "join_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "balance" DOUBLE PRECISION NOT NULL  DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "adminpushtoken" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "push_token" VARCHAR(255) NOT NULL,
    "user_id" INT NOT NULL UNIQUE REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "order" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "receiver_name" VARCHAR(100) NOT NULL,
    "receiver_phone_number" VARCHAR(12) NOT NULL,
    "receiver_street_address" TEXT NOT NULL,
    "receiver_city" VARCHAR(20) NOT NULL  DEFAULT 'Ikorodu',
    "receiver_state" VARCHAR(20) NOT NULL  DEFAULT 'Lagos',
    "amount" DOUBLE PRECISION NOT NULL,
    "payment_ref_id" VARCHAR(150) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(30) NOT NULL  DEFAULT 'PENDING_PAYMENT',
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "orderitem" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "price" DOUBLE PRECISION NOT NULL,
    "quantity" INT NOT NULL,
    "order_id" INT NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE,
    "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "transactions" (
    "transaction_id" SERIAL NOT NULL PRIMARY KEY,
    "status" VARCHAR(20) NOT NULL,
    "amount" VARCHAR(10) NOT NULL,
    "tx_ref" VARCHAR(30) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "userpushtoken" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "push_token" VARCHAR(255) NOT NULL,
    "user_id" INT NOT NULL UNIQUE REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
