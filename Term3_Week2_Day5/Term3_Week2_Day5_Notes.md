More PostgreSQL
CREATE Sports Database
CREATE DATABASE Sports;
CREATE TABLE Game
(MatchName VARCHAR,
 Win INTEGER,
 Loss INTEGER);
 
INSERT INTO Game
VALUES('Match A', 2, 4),
('Match B', 2, 2),
('Match C', 4, 1),
('Match D', 2, 0),
('Match E', 2, 1),
('Match F', 2, 2),
('Match G', 1, 3),
('Match H', 3, 3);

CREATE TABLE Players
(
 Name VARCHAR,
 Country VARCHAR
);

INSERT INTO Players
VALUES('Jack', 'Australia'),
('Kate', 'Brazil'),
('Mario', 'China'),
('Dan', 'USA');

CREATE TABLE NominatedCountries
(
 Name VARCHAR
);

INSERT INTO NominatedCountries
VALUES('Australia'),
('China'),
('Cameron');
Subquery, IN and NOT IN
SELECT Name, Country
FROM Players
WHERE Country IN (SELECT Name FROM NominatedCountries);
SELECT Name, Country
FROM Players
WHERE Country NOT IN (SELECT Name FROM NominatedCountries);
CASE
SELECT MatchName, Win, Loss,
CASE
    WHEN Win > Loss THEN 'Home Team Won'
    WHEN Win < Loss THEN 'Away Team Won'
    ELSE 'It is a Tie'
END AS Result
FROM Game;
CREATE TABLE FinalResults AS
SELECT MatchName, Win, Loss,
CASE
    WHEN Win > Loss THEN 'Home Team Won'
    WHEN Win < Loss THEN 'Away Team Won'
    ELSE 'It is a Tie'
END AS Result
FROM Game;
Now, connect to PizzaRestaurant Database:

More Subquery
SELECT * 
FROM items
WHERE item_price > ( SELECT AVG(item_price)
                     FROM items );
SELECT * 
FROM items
WHERE item_price < ( SELECT AVG(item_price)
                     FROM items );
Date functions
SELECT CURRENT_DATE;
SELECT TO_CHAR(CURRENT_DATE, 'dd/mm/yyyy') AS order_date;

SELECT TO_CHAR(CURRENT_DATE, 'dd/mm/yy') AS order_date;

SELECT TO_CHAR(CURRENT_DATE, 'mm/yy') AS order_date;

SELECT TO_CHAR(CURRENT_DATE, 'mm') AS order_date;

SELECT TO_CHAR(CURRENT_DATE, 'Mon dd, yyyy') AS order_date;
SELECT order_id, order_date, now() - order_date AS order_age
FROM orders;
SELECT order_id, order_date, AGE(order_date)
FROM orders;

SELECT order_id, order_date, AGE('2022-12-31', order_date)
FROM orders;
SELECT order_id,
       EXTRACT (DAY FROM order_date) AS Day,
       EXTRACT (YEAR FROM order_date) AS Year,
       EXTRACT (MONTH FROM order_date) AS Month
FROM orders;
SELECT * 
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = '2020';
SCHEMA and Access Privileges
To make database objects more organised and manageable you will need to use schemas. Schemas allow multiple users access a database in a manageable manner withour interference. ALso, allow only authorised users access database objects.

List of schemas
\dn
Show current schema
SELECT current_schema();
View current search path
SHOW search_path;
Create new schema
CREATE SCHEMA ccc
Add schema to search path
SET search_path TO ccc;
Create a table in the ccc schema
CREATE TABLE userdata(
us_id INTEGER,
us_name VARCHAR
);

INSERT INTO userdata
VALUES (12, 'Jamal'), (13, 'Bruce');
Query records from created table using ccc schema
SELECT * FROM userdata;

SELECT * FROM ccc.userdata;
Query records from created table using public schema
SELECT * FROM public.userdata;

-- ERROR:  relation "public.userdata" does not exist
Create table in the public schema
CREATE TABLE public.userdata(
us_id INTEGER,
us_name VARCHAR
);

INSERT INTO public.userdata
VALUES (12, 'Garret'), (13, 'Sam');
Query records from created table using public schema
SELECT * FROM public.userdata;
Drop ccc schema
DROP SCHEMA ccc;

-- ERROR:  cannot drop schema ccc because other objects depend on it
-- DETAIL:  table ccc.mytable depends on schema ccc
DROP SCHEMA ccc CASCADE;

-- NOTICE:  drop cascades to table ccc.mytable
SCHEMA and Access Privileges Excercise
SCHEMA and Access Privileges

CREATE DATABASE dcompany;
CREATE ROLE user1 LOGIN;

CREATE ROLE user2 LOGIN;

CREATE ROLE user3 LOGIN;

CREATE ROLE user4 LOGIN;

CREATE ROLE user5 LOGIN;

CREATE ROLE payroll LOGIN;

CREATE ROLE hr LOGIN;

CREATE ROLE marketing LOGIN;
\c dcompany
CREATE TABLE sales
(id SERIAL,
item VARCHAR(10),
saleamount NUMERIC
);

INSERT INTO sales (item, saleamount)
VALUES ('Item1', 125.2), ('Item2', 325.2),('Item3', 165.8);
CREATE TABLE products
(id SERIAL,
product VARCHAR(10),
description TEXT
);

INSERT INTO products (product, description)
VALUES ('Product1', 'Description1'), ('Product2', 'Description2'),('Product3', 'Description3');
CREATE TABLE employees
(id SERIAL,
empname VARCHAR(10),
salary NUMERIC
);

INSERT INTO employees (empname, salary)
VALUES ('Jack', 120), ('Sara', 80),('James', 140);
Login into a separate PostgreSQL session as payroll
psql -U payroll dcompany
Run some SELECT queries
SELECT * 
FROM employees;

-- ERROR:  permission denied for table employees

SELECT * 
FROM products;

-- ERROR:  permission denied for table products

SELECT * 
FROM sales;

-- ERROR:  permission denied for table sales
Try the same with all roles user1, user2, user3, user4, user5, marketing, and hr. All created roles can only LOGIN and nothing else, so should expect same error. It is not only SELECT but same applies on all privileges such as INSERT, UPDATE, and DELETE.

GRANT payroll some privileges
GRANT ALL
ON sales
TO payroll;

GRANT ALL
ON sales_id_seq
TO payroll;

GRANT SELECT
ON products
TO payroll;
Run some testing queries
SELECT * 
FROM products;

SELECT * 
FROM sales;

INSERT INTO sales (item, saleamount)
VALUES ('Item5', 3425.2);

SELECT * 
FROM employees;

-- ERROR:  permission denied for table employees

INSERT INTO products (product, description)
VALUES ('Product5', 'Description5');

-- ERROR:  permission denied for table products
GRANT marketing some privileges
GRANT ALL
ON products, products_id_seq
TO marketing;
Run some testing queries
SELECT * 
FROM products;

INSERT INTO products (product, description)
VALUES ('Product6', 'Description6');

DELETE FROM products
WHERE product = 'Product3';

SELECT * 
FROM employees;

-- ERROR:  permission denied for table employees

SELECT * 
FROM sales;

-- ERROR:  permission denied for table sales
GRANT hr some privileges
GRANT ALL
ON employees, employees_id_seq
TO hr;
Run some testing queries
INSERT INTO employees (empname, salary)
VALUES ('Martin', 125)

UPDATE employees
SET salary = 110
WHERE empname = 'Sara';

SELECT * 
FROM employees;

SELECT * 
FROM products;

-- ERROR:  permission denied for table products

DELETE FROM products
WHERE product = 'Product2';

-- ERROR:  permission denied for table products

SELECT * 
FROM sales;

-- ERROR:  permission denied for table sales
GRANT user1 and user2 the payroll group_role
GRANT payroll TO user1, user2;
GRANT user3 and user4 the marketing group_role
GRANT marketing TO user3, user4;
GRANT user5 the hr group_role
GRANT hr TO user5;
Now do some testing, login using different users and check the granted privileges in a similar way as we did with group_roles payroll, hr, and marketing.
user1 and user2 have same privileges as payroll
user3 and user4 have same privileges as marketing
user5 have same privileges as hr
Show schemas
\dn
Create a new schema
CREATE SCHEMA private;
Create table in the private schema
CREATE TABLE private.secretcodes(code VARCHAR);

INSERT INTO private.secretcodes 
VALUES ('ccc1357'),('ccc2468');
View current search path
SHOW search_path;
Change search path
SET search_path TO private, public;
Query data from table secretcodes as superuser
SELECT * 
FROM secretcodes;
Query data from table secretcodes as user1
SELECT * 
FROM private.secretcodes;

-- ERROR:  permission denied for schema private
GRANT payroll usage on private schema
GRANT USAGE ON SCHEMA private
TO payroll;
Query data from table secretcodes as user1
SELECT * 
FROM private.secretcodes;

-- ERROR:  permission denied for table secretcodes
GRANT payroll SELECT access to secretcodes table
GRANT SELECT
ON secretcodes
TO payroll;
GRANT hr SELECT access to secretcodes table
GRANT SELECT
ON secretcodes
TO hr;
Query data from table secretcodes as user5
SELECT * 
FROM private.secretcodes;

-- ERROR:  permission denied for schema private
GRANT hr usage on private schema
GRANT USAGE ON SCHEMA private
TO hr;
Query data from table secretcodes as user5
SELECT * 
FROM private.secretcodes;
Create table as user5 in private schema
CREATE TABLE private.somedata(datadescrip VARCHAR);

-- ERROR:  permission denied for schema private
We have previously granted USAGE privilege which allows the use of the schema but not creation of objects. To allow creation of objects need to GRANT CREATE to roles. You may want to practice the same exercise but this time using CREATE and not USAGE.