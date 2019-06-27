DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  credit INTEGER DEFAULT 0.0,
  card_number INTEGER,
  card_expire_date INTEGER,
  address TEXT NOT NULL,
  phone_number INTEGER
);
