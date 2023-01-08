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
  user_id INTEGER PRIMARY KEY,

  url TEXT DEFAULT "http://192.168.178.72:5050/video_feed/pi2?resolution=high",
  prefix TEXT DEFAULT "video",
  flip BIT DEFAULT FALSE,
  recording BIT DEFAULT FALSE,

  FOREIGN KEY (user_id) REFERENCES user (user_id)
);