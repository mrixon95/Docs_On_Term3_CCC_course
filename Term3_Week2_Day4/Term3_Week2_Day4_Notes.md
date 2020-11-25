



Q1: Which command creates a database called hospital?

A1: CREATE DATABASE hospital

Q2: Which statement is True?


CREATE TABLE Patient
(
 PatientId INTEGER PRIMARY KEY,
 PatientFName VARCHAR,
 PatientLName VARCHAR,
 PatientSuburb VARCHAR
);

A2: Creates patient table with patientid uniquely identifies a record


Q3: Below query will execute with no issues?

INSERT INTO Patient
VALUES (201901,'Jack','D','Rhodes'),
       (201902,'Dan','J','Ryde'),
       (201903,'Rachel','K','Medowbank'),
       (201904,'Karen','L','Rhodes');

A3: True

Q4: Below query will ___

SELECT *
FROM doctor;

A4: Retrieve all records from doctor table

Q5: Below query will ____

SELECT DISTINCT doctorsuburb
FROM doctor;

A5: Retrieve unique doctorsuburb from doctor table

Q6: CREATE, DROP, ALTER, and TRUNCATE are ___

A6: DDL

Q7: INSERT, UPDATE, and DELETE are ___?

A7: DML

Q8: GRANT and REVOKE are ___

A8: DCL

Q9: BEGIN, COMMIT, and ROLLBACK are ___

A9: TCL

Q10: Which of the below insertions is not permitted

CONSTRAINT citycheck CHECK (
	per_city IN ('Sydney', 'Brisbane', 'Melbourne'))

A10: (...., 'sydney')


## Day 4 SQL Aggregate Function & Joins




### Launch psql utility or connect to sql server using:
```
    
	sudo apt-get --purge remove postgresql
	sudo apt-get -y install postgresql
	sudo service postgresql start
	
	/* Connect to PostgreSQL using the postgres role */
	sudo -i -u postgres

	/* Access PostgreSQL using the psql */
	psql
   
```


Let’s create some databases before we dive into querying data from a database:

```
CREATE a Hospital Database
CREATE Hospital Database
CREATE DATABASE Hospital;
CREATE Patient table
CREATE TABLE Patient
(
 PatientId INTEGER PRIMARY KEY,
 PatientFName VARCHAR,
 PatientLName VARCHAR,
 PatientSuburb VARCHAR
);
CREATE Doctor table
CREATE TABLE Doctor
(
 DoctorId INTEGER PRIMARY KEY,
 DoctorFName VARCHAR,
 DoctorLName VARCHAR,
 DoctorSuburb VARCHAR
);


The Doctor to Patient table is many-to-many so therefore we need a JOINT table
CREATE Appointment table (Junction Table - Many to Many Relationship)
In a many to many relationship need to create a junction table. The junction table will have two foreign keys which are the primary keys of other two table we want to relate. In this example, a patient can see many doctors and a doctor can have many patients. The table Appointment is the joint table holding the Patient PK(PatientId) and Doctor Pk(DoctorId).

CREATE TABLE Appointment
(
 PatientId INTEGER,
 DoctorId INTEGER,
 AppDate TIMESTAMP,
 CONSTRAINT patientFK FOREIGN KEY (PatientId)
 REFERENCES Patient (PatientId),
 CONSTRAINT doctorFK FOREIGN KEY (DoctorId)
 REFERENCES Doctor (DoctorId)
);
Insert data into Patient table
INSERT INTO Patient
VALUES (201901,'Jack','D','Rhodes'),
       (201902,'Dan','J','Ryde'),
       (201903,'Rachel','K','Medowbank'),
       (201904,'Karen','L','Rhodes');
Insert data into Doctor table
INSERT INTO Doctor
VALUES (201,'SAM','K','Medowbank'),
       (202,'Mac','B','Rhodes'),
       (303,'Randy','L','Ryde'),
       (404,'Hans','N','Silverwater'),
       (406,'Dan','K','Medowbank'),
       (413,'Mars','B','Rhodes'),
       (423,'Roshan','L','Rhodes'),
       (408,'Brian','N','Silverwater');
Insert data into Appointment table
INSERT INTO Appointment
VALUES (201901,201,'2019-04-23 10:30'),
       (201902,202,'2020-05-24 11:30'),
       (201903,303,'2019-06-23 12:30'),
       (201904,404,'2021-04-25 11:30'),
       (201901,203,'2019-03-23 13:30'),
       (201902,201,'2017-02-25 14:30'),
       (201903,303,'2019-07-26 15:30'),
       (201904,201,'2018-08-27 15:30');
```
This will output an error:

ERROR: insert or update on table “appointment” violates foreign key constraint “doctorfk”

DETAIL: Key (doctorid)=(203) is not present in table “doctor”.

So, updated the wrong doctor id with the correct one:

```
INSERT INTO Appointment
VALUES (201901,201,'2019-04-23 10:30'),
       (201902,202,'2020-05-24 11:30'),
       (201903,303,'2019-06-23 12:30'),
       (201904,404,'2021-04-25 11:30'),
       (201901,303,'2019-03-23 13:30'),
       (201902,201,'2017-02-25 14:30'),
       (201903,303,'2019-07-26 15:30'),
       (201904,201,'2018-08-27 15:30');
CREATE a PizzaRestaurant Database
CREATE PizzaRestaurant Database
CREATE DATABASE PizzaRestaurant;
CREATE Customers table
CREATE TABLE customers
( customer_id INTEGER,
  customer_name VARCHAR NOT NULL,
  customer_location VARCHAR DEFAULT 'Sydney',
  CONSTRAINT customers_pk PRIMARY KEY (customer_id)
);
CREATE Orders table
CREATE TABLE orders
( order_id INTEGER,
  order_date Date NOT NULL,
  order_type VARCHAR DEFAULT 'Pickup',
  customer_id INTEGER,
  CONSTRAINT orders_pk PRIMARY KEY (order_id),
  CONSTRAINT orders_fk FOREIGN KEY (customer_id)
  REFERENCES customers(customer_id)
);
CREATE Items table
CREATE TABLE items
( item_id VARCHAR,
  item_name VARCHAR,
  item_price NUMERIC,
  CONSTRAINT items_pk PRIMARY KEY (item_id)
);
CREATE OrderItems table
CREATE TABLE ordersitems
( order_id INTEGER,
  item_id VARCHAR,
  CONSTRAINT ordersitems_fk1 FOREIGN KEY (order_id)
  REFERENCES orders(order_id),
  CONSTRAINT ordersitems_fk2 FOREIGN KEY (item_id)
  REFERENCES items(item_id)
);
INSERT VALUES
INSERT INTO customers(customer_id, customer_name, customer_location)
VALUES
(200301,'Jack','Ryde'),
(200306,'Richard','Winyard'),
(200307,'Michael','North Sydney'),
(200308,'David','Rhodes'),
(200309,'Julian','Winyard');

INSERT INTO orders(order_id, order_date, order_type, customer_id)
VALUES
(1,'2016-06-22','Delivery',200301),
(2,'2016-06-23','Pickup',200301),
(3,'2016-06-24','Pickup',200306),
(4,'2016-06-12','Delivery',200307),
(5,'2016-03-12','Delivery',200307),
(6,'2016-04-12','Delivery',200307),
(7,'2016-06-03','Delivey',200309),
(8,'2016-07-22','Delivey',200309),
(9,'2017-07-22','Pickup',200308),
(25,'2017-06-22','Delivey',200308),
(10,'2017-03-22','Delivery',200301),
(11,'2016-06-12','Pickup',200301),
(12,'2018-06-11','Pickup',200306),
(13,'2018-02-22','Delivery',200307),
(14,'2018-07-16','Pickup',200308),
(15,'2018-06-22','Pickup',200308),
(16,'2019-06-26','Pickup',200309),
(17,'2019-06-27','Delivery',200309),
(18,'2019-08-22','Delivery',200309),
(19,'2019-06-02','Delivery',200309),
(20,'2020-03-04','Pickup',200308),
(21,'2020-05-02','Pickup',200308),
(22,'2020-05-22','Pickup',200309),
(23,'2020-04-22','Delivery',200309),
(24,'2020-03-22','Delivery',200309);

INSERT INTO items(item_id, item_name, item_price)
VALUES
('pz213','Cheeze Pizza',10.00),
('pz214','Chicken Pizza',14.00),
('sd211','Green Salad',8.00),
('sd210','Chicken Salad',10.50);

INSERT INTO ordersitems(order_id, item_id)
VALUES
(1,'pz213'),
(1,'pz214'),
(1,'sd211'),
(2,'sd211'),
(2,'pz214'),
(3,'pz214'),
(3,'sd211'),
(4,'sd211'),
(4,'pz214'),
(5,'sd210'),
(6,'pz213'),
(9,'sd210'),
(9,'pz213'),
(6,'pz214'),
(6,'pz213'),
(7,'pz214'),
(7,'pz213'),
(8,'pz214'),
(8,'pz213'),
(9,'pz214'),
(9,'pz213'),
(10,'pz213'),
(10,'pz214'),
(10,'sd211'),
(11,'sd211'),
(11,'pz214'),
(12,'pz214'),
(12,'sd211'),
(13,'sd211'),
(13,'pz214'),
(14,'sd210'),
(14,'pz213'),
(15,'sd210'),
(15,'pz213'),
(16,'pz214'),
(16,'pz213'),
(17,'pz214'),
(17,'pz213'),
(18,'pz214'),
(18,'pz213'),
(19,'pz214'),
(19,'pz213'),
(20,'sd210'),
(20,'pz213'),
(21,'sd210'),
(21,'pz213'),
(22,'pz214'),
(22,'pz213'),
(23,'pz214'),
(23,'pz213'),
(24,'pz214'),
(24,'pz213');
The SELECT Statement
The SELECT statement is what we need to query data from tables. SELECT statement uses many clauses for a flexible data retrieval. SQL statement clauses are many hence will cover the most commonly used ones below:

Connect to the Hospital database and let’s start querying data.
SELECT and FROM clause:
SELECT *
FROM doctor;
SELECT doctorfname, doctorsuburb
FROM doctor;
DISTINCT clause:
SELECT DISTINCT doctorsuburb
FROM doctor;
ORDER BY clause:
SELECT doctorfname, doctorsuburb
FROM doctor
ORDER BY doctorsuburb;
SELECT doctorfname, doctorsuburb
FROM doctor
ORDER BY doctorsuburb DESC;
WHERE clause:
SELECT *
FROM doctor
WHERE doctorsuburb = 'Rhodes';
SELECT *
FROM doctor
WHERE doctorsuburb = 'Rhodes' or doctorsuburb = 'Medowbank';
SELECT *
FROM doctor
WHERE doctorsuburb != 'Ryde';
Aggregate functions:
SELECT COUNT(doctorid)
FROM doctor;
SELECT doctorsuburb, COUNT(doctorid) as Numofdoctors
FROM doctor
GROUP BY doctorsuburb;
Connect to the PizzaRestaurant database and let’s query more data.
LIMIT clause:
SELECT *
FROM orders
LIMIT 5;
SELECT *
FROM orders
LIMIT 5 OFFSET 3;
SELECT *
FROM orders
ORDER BY order_date DESC
LIMIT 5 OFFSET 3;
FETCH clause:
SELECT *
FROM orders
FETCH FIRST ROW ONLY;
SELECT *
FROM orders
FETCH FIRST 3 ROW ONLY;
SQL JOINs
Let’s create a small database to help understand SQL JOINs.
CREATE DATABASE Colors;
CREATE TABLE LeftTable
(
ColorId INTEGER,
ColorName VARCHAR);

CREATE TABLE RightTable
(
ColorId INTEGER,
ColorName VARCHAR);

INSERT INTO LeftTable
VALUES (1,'White'),(2,'Green'),(3,'Yellow');

INSERT INTO RightTable
VALUES (1,'Brown'),(2,'Green'),(3,'Yellow'),(4,'Blue');
INNER JOIN:
 SELECT lt.ColorName AS LeftColor, rt.ColorName AS RightColor
 FROM LeftTable lt
 INNER JOIN RightTable rt ON lt.ColorName=rt.ColorName;
INNER JOIN

LEFT JOIN:
SELECT lt.ColorName AS LeftColor, rt.ColorName AS RightColor
FROM LeftTable lt
LEFT JOIN RightTable rt ON lt.ColorName=rt.ColorName;
LEFT JOIN

RIGHT JOIN:
SELECT lt.ColorName AS LeftColor, rt.ColorName AS RightColor
FROM LeftTable lt
RIGHT JOIN RightTable rt ON lt.ColorName=rt.ColorName;
RIGHT JOIN

FULL OUTER JOIN:
SELECT lt.ColorName AS LeftColor, rt.ColorName AS RightColor
FROM LeftTable lt
FULL OUTER JOIN RightTable rt ON lt.ColorName=rt.ColorName;
FULL OUTER JOIN

Input/Output
Create sql file in the current working directory
echo 'select * from secretcodes' > myquery.sql
Execute the file in psql
\i myquery.sql
Output all query results to file
\o myqueryoutput.txt
Let’s practice SQL JOINs using the PizzaRestaurant Database:
Query the total number of orders per customer

SELECT c.customer_name, COUNT(o.customer_id)
FROM customers c, orders o
WHERE c.customer_id = o.customer_id
GROUP BY c.customer_name;
Query the total price of orders per customer

SELECT c.customer_name, SUM(t.item_price)
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
INNER JOIN ordersitems ot ON o.order_id = ot.order_id
INNER JOIN items t ON ot.item_id = t.item_id
GROUP BY c.customer_name;
Query the total price of orders for customer ‘Julian’

SELECT c.customer_name, SUM(t.item_price)
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
INNER JOIN ordersitems ot ON o.order_id = ot.order_id
INNER JOIN items t ON ot.item_id = t.item_id
WHERE c.customer_name = 'Julian'
GROUP BY c.customer_name;
Query the total price of orders for customers having purchase total above $90.00

SELECT c.customer_name,SUM(t.item_price)
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
INNER JOIN ordersitems ot ON o.order_id = ot.order_id
INNER JOIN items t ON ot.item_id = t.item_id
GROUP BY c.customer_name
Having SUM(t.item_price) > 90.00;