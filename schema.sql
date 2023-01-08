-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_data;

CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE user_data (
  user_data_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,

  url TEXT DEFAULT "",
  prefix TEXT DEFAULT "",
  flip BIT DEFAULT 0,
  recording BIT DEFAULT 0,

  FOREIGN KEY (user_id) REFERENCES user (user_id)
);