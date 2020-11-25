### Developer Workbook - Database Systems. Term3 Assignment 1 T3A1

# Question 1

A database table in a relational database is like a grid with rows and columns. 
Each row is made up of a data record and in each column refers to a particular attribute that the records all have. The attribute has both a name and a data type.
Entries in a particular column are constrained to the datatype of the column's attribute and the column names cannot be duplicated in the same table. 

Tables can have an important feature called a Primary Key. Primary keys are both unique and not null, and are used as a way to uniquely identify a tuple/row in the table. 
They can consist of one or multiple columns. For example, a driver license number can uniquely identify a driver and a mobile number can uniquely identify a person who owns a mobile.
Therefore, driver license number and mobile number would be suitable as a primary key in a database for storing driver info or mobile phone info respectively.


# Question 2

The three possible relationships between entities in a relational database are one-to-one, one-to-many and many-to-many. 
One-to-one relationship: One record/row in a table can only be associated with one record/row in another table, and vice-versa.
For example, a student entity and a contact info entity would have a one-to-one relationship. Each student has only one contact info record and a contact info record
can only belong to one student.
One-to-many relationship: One record/row in a table can be associated with many records/rows in another table.
For example: a high-school entity and a student entity would have a one-to many relationship. A high-school may have many students enrolled. However, a student may only be enrolled in one high-school.

Many-to-many relationship: Many records/rows in a table can be associated with many records/rows in another table.
For example: a student entity could enrol in many different subjects. Like-wise, a single subject can have many different students enrolled in it.

Primary keys and foreign keys can be used to create a many-to many relationship between tables.

Now, a many-to-many relationship requires a joining/bridging table. This table is used to store a record for each combination of the other two tables.
In our case, this record is the combination of studentID and subjectID and this combination describes which student enrolled in which subject.
In our example, our joining table would contain two foreign keys which are studentID and courseID. Foreign keys values are constrained in that their value must already exist as a primary key value within another table.
The joining table (enrolment) will only accept a student ID and a subjectID combination if the studentID already exists as a primary key entry in the student table and the subjectID already exists as a primary key entry within the subject table.


# Question 3

Three types of constraints are check, not null and foreign key.

The check constraint limits the range of values that a particular attribute or set of attributes can have. This constraint ensures that the value entered must satisfy a logical, boolean expression. If the value does not satisfy the expression, it is not inserted into the table.
The constraint helps to ensure that bad data does not mistakenly get inserted into the database table. For example, a CHECK constraint could be that product prices in a supermarket are greater than 0.
No prices in the supermarket should be 0 or negative so this constraint makes sense. Any negative values would violate this constraint and cause an error. 

The not null constraint ensures that a particular column/attribute cannot have a null value in it. This means that the particular attribute for that column must always have a value.
For example, a social media website could ensure that records in a user table must always have a name by constraining the name attribute to be NOT NULL. 
This means that a record with the name attribute left empty would raise an error.

The foreign key constraint ensures that a value in one table must also appear in another table. The table with the foreign key is called the child table and the referenced table is called the parent table.  
The foreign key ensure referencial integrity when new records are inserted.
For example, a table called Order could have a foreign key constraint which refers to another table called Customer.
An order should always be made by an existing customer so the customerid in the order table should appear in the customerid column of the customer table.

# Question 4

Data types enforce data integrity by ensuring that all values in a particular column are of the same datatype and of a datatype that makes logical sense.
It would be wrong to have say a column for the customer's name but allow entries that are boolean or integers. A customer name entry of True or 1234 would clearly be an error and therefore should not be allowed.
Furthermore, datatypes can be used to constrain the range of numeric values. For example, the data type tiny int could be used for the attribute age in years.
Tiny int allows whole numbers from 0 to 255. No human has lived beyond 255 years so this data type makes sense.

Another way datatype enforce data integrity is by ensuring the same format is used. 
Without a common format, problems can occur. For example, in the US, the date is written in month/day/year form whereas in most other countries it is day/month/year. 
Sometimes the last 2 digits of the year are used as opposed to all 4 digits. 
In SQL, the data type DATETIME is formatted YYYY-MM-DD HH:MI:SS.
This ensures that all dates and times entered into the database table follow this format so that there are no formatting errors.


# Question 5

The CREATE TABLE keywords are apart of a Data Defintion Language (DDL) command which allows for creating a table.
Along with those keywords, we specify the name of the table and the column definitions. Each column has a name and a datatype.
For example. 
CREATE TABLE employees (
    id            INTEGER       PRIMARY KEY,
    first_name    VARCHAR(50)   not null,
    last_name     VARCHAR(75)   not null,
    dateofbirth   DATE
    city          VARCHAR(50)   not null,
    country       VARCHAR(50)   not null,
);

The UPDATE and SET keywords can be used as part of a Data Manipulation Language (DML) command which modifies existing records in a table if they satisfy a condition.
It is structured like this:
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;

An example could be setting the country value to be 'Australia' when the city value is either 'Sydney', 'Melbourne' or 'Gold Coast'.
The SQL command would be

UPDATE employees
SET country='Australia'
WHERE city IN ('Sydney', 'Melbourne', 'Gold Coast');


The DELETE operator is used along with a WHERE clause to remove particular records from a database.
For example. we may only want Australian employees in our database table and we therefore want to delete all employee records who are not from Australia.
Hence we could write
DELETE FROM employees
WHERE country != 'Australia'



### Question 6

The inner join is used on two tables (eg. table_one and table_two) and creates a new resulting table by finding all pairs of rows in table_one and table_two that satisfy the join condition.
Only when the join condition is satisfied will the column values of each matched pair in table_one and table_two be combined to form a result row.
The syntax looks like:

SELECT table_one.column_one, table_two.column_one...
FROM table_one
INNER JOIN table_two
ON table_one.common_field = table_two.common_field;

As can be seen from the syntax above, the INNER JOIN only occurs when the value of the attribute 'commonfield' in table_one is the same as the value of the attribute 'commonfield' in table_two.
When this is the case, the record from table_one and the record from table_two are joined and form a new record.
