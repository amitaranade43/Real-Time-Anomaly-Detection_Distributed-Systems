-- USE abnormal_db;

-- CREATE TABLE IF NOT EXISTS abnormal_table (
--     id INT NOT NULL AUTO_INCREMENT,
--     temp FLOAT NOT NULL,
--     server_id INT NOT NULL,
--     status BOOLEAN NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--     PRIMARY KEY (id)
-- );


-- CREATE TABLE IF NOT EXISTS abnormal_history (
--     id INT NOT NULL AUTO_INCREMENT,
--     temp FLOAT NOT NULL,
--     server_id INT NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY (id)
-- );

CREATE TABLE IF NOT EXISTS abnormal_table (
    id SERIAL PRIMARY KEY,
    temp FLOAT NOT NULL,
    server_id INT NOT NULL,
    status BOOLEAN NOT NULL,
    created_at TIMESTAMP default current_timestamp,
    updated_at TIMESTAMP default current_timestamp
);

CREATE TABLE IF NOT EXISTS abnormal_history (
    id SERIAL PRIMARY KEY,
    temp FLOAT NOT NULL,
    server_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
