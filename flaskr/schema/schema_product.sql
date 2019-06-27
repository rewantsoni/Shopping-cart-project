DROP TABLE IF EXISTS product;
CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT  NOT NULL,
  type TEXT NOT NULL,
  cost INTEGER NOT NULL,
  details TEXT	NOT NULL,
  manufacturer TEXT NOT NULL,
  supplier TEXT NOT NULL
);