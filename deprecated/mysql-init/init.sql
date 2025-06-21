CREATE TABLE IF NOT EXISTS my_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO my_table (name, email) VALUES
('Alice Example', 'alice@example.com'),
('Bob Smith', 'bob@example.com');
