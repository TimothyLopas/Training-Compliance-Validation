-- Create the database
--CREATE DATABASE training_database.db;

-- Switch to the new database
--.open training_database.db

-- Create the tables
CREATE TABLE trainings (
    id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE,
    PRIMARY KEY (id)
);

CREATE TABLE employee_training (
    id INT AUTO_INCREMENT,
    employee_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    Cybersecurity_Awareness DATE,
    Anti_Bribery DATE,
    Diversity_Awareness DATE,
    Insider_Trading_Awareness DATE,
    PRIMARY KEY (id)
);

CREATE TABLE vacations (
    id INT AUTO_INCREMENT,
    employee_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE,
    PRIMARY KEY (id)
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT,
    employee_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

--Populate the tables
INSERT INTO trainings (name, description, due_date) VALUES
('Cybersecurity Awareness', 'This course covers the essentials of protecting personal and company data from cyber threats.', '2024-04-30'),
('Anti Bribery', 'This training provides comprehensive insights into the legal and ethical implications of bribery and how to prevent it.', '2024-05-30'),
('Diversity Awareness', 'Explore the importance of diversity and inclusion in the workplace and learn strategies to promote an inclusive environment.', '2024-08-01'),
('Insider Trading Awareness', 'Learn about the legalities of insider trading and how to avoid activities that could be construed as insider trading.', '2024-08-01');


BEGIN TRANSACTION;

WITH RECURSIVE
seq(id) AS (
  SELECT 1 UNION ALL SELECT id + 1 FROM seq WHERE id < 20
),
random_dates AS (
  SELECT
    id,
    date('2024-03-01', '+' || (ABS(random()) % 284) || ' days') AS start_date,
    (ABS(random()) % 15) + 1 AS length -- Random vacation length between 1 and 15 days
  FROM seq
)
INSERT INTO vacations (id, employee_id, name, start_date, end_date)
SELECT
  id,
  id AS employee_id, -- Assuming employee_id corresponds with the sequence for illustration
  'Employee ' || id,
  start_date,
  date(start_date, '+' || length || ' days') AS end_date
FROM random_dates;

COMMIT;
