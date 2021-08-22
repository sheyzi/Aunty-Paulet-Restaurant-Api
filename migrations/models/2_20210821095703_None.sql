-- upgrade --
CREATE TABLE IF NOT EXISTS "category" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(20) NOT NULL,
    "slug" VARCHAR(50) NOT NULL UNIQUE,
    "image_url" VARCHAR(500) NOT NULL  DEFAULT 'https://res.cloudinary.com/sheyzisilver/image/upload/v1628729409/placeholder_rl2wsr.png',
    "date_created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "product" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "slug" VARCHAR(60) NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "price" REAL NOT NULL,
    "image_url" VARCHAR(500) NOT NULL  DEFAULT 'https://res.cloudinary.com/sheyzisilver/image/upload/v1628729409/placeholder_rl2wsr.png',
    "is_featured" INT NOT NULL  DEFAULT 0,
    "date_created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(200) NOT NULL UNIQUE,
    "email" VARCHAR(200) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "is_active" INT NOT NULL  DEFAULT 1,
    "is_admin" INT NOT NULL  DEFAULT 0,
    "join_date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "balance" REAL NOT NULL  DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "order" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "receiver_name" VARCHAR(100) NOT NULL,
    "receiver_phone_number" VARCHAR(12) NOT NULL,
    "receiver_street_address" TEXT NOT NULL,
    "receiver_city" VARCHAR(20) NOT NULL,
    "receiver_state" VARCHAR(20) NOT NULL  DEFAULT 'Lagos',
    "amount" REAL NOT NULL,
    "payment_ref_id" VARCHAR(150) NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(30) NOT NULL  DEFAULT 'PENDING_PAYMENT',
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "orderitem" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "price" REAL NOT NULL,
    "quantity" INT NOT NULL,
    "order_id" INT NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE,
    "product_id" INT NOT NULL REFERENCES "product" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "userpushtoken" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "push_token" VARCHAR(255) NOT NULL,
    "user_id" INT NOT NULL UNIQUE REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);
