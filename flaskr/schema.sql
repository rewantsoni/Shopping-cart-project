DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS incart;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_id;
DROP TABLE IF EXISTS payment;

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

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT  NOT NULL,
  type TEXT NOT NULL,
  cost INTEGER NOT NULL,
  details TEXT	NOT NULL,
  manufacturer TEXT NOT NULL,
  supplier TEXT NOT NULL
);

CREATE TABLE incart (
  product_id INTEGER REFERENCES product(id),
  cart_id INTEGER REFERENCES user(id)
);

CREATE TABLE orders (
  product_id INTEGER REFERENCES product(id),
  user_id INTEGER REFERENCES user(id)
);

CREATE TABLE order_id (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  orders INTEGER REFERENCES orders(id)
);
CREATE TABLE payment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  payment_mode TEXT UNIQUE NOT NULL,
  order_id REFERENCES order_id(id),
  value INTEGER NOT NULL,
  status INTEGER NOT NULL
);