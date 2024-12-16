CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT
);

INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'b01972e2a1d89bd958e295b4be9a402d');
