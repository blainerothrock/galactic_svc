DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS simulation;
DROP TABLE IF EXISTS cluster;
DROP TABLE IF EXISTS system;
DROP TABLE IF EXISTS character;
DROP TABLE IF EXISTS character_simulation;
DROP TABLE IF EXISTS vessel;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  name TEXT NOT NULL
);

CREATE TABLE simulation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user (id)
);

CREATE TABLE cluster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    FOREIGN KEY (simulation_id) REFERENCES simulation (id)
);

CREATE TABLE system (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cluster_id INTEGER NOT NULL,
    x_coordinate FLOAT NOT NULL,
    y_coordinate FLOAT NOT NULL,
    z_coordinate FLOAT NOT NULL,
    metal FLOAT NOT NULL,
    organics FLOAT NOT NULL,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES character (id),
    FOREIGN KEY (cluster_id) REFERENCES cluster (id)
);

-- CREATE TABLE star (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     system_id INTEGER NOT NULL,
--     FOREIGN KEY (system_id) REFERENCES system (id),
--     class TEXT NOT NULL,
--     temperature INTEGER NOT NULL,
--     mass FLOAT NOT NULL,
--     radius FLOAT NOT NULL
-- )
--
-- CREATE TABLE planet (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     system_id INTEGER NOT NULL,
--     FOREIGN KEY (system_id) REFERENCES system (id),
--     orbital_distance FLOAT NOT NULL,
-- )

CREATE TABLE character (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE character_simulation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    simulation_id INTEGER NOT NULL,
    FOREIGN KEY (character_id) REFERENCES character (id),
    FOREIGN KEY (simulation_id) REFERENCES simulation (id)
);

CREATE TABLE vessel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    class TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 0,
    system_id INTEGER,
    x_coordinate FLOAT NOT NULL,
    y_coordinate FLOAT NOT NULL,
    z_coordinate FLOAT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES character (id),
    FOREIGN KEY (system_id) REFERENCES system (id)
);