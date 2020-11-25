PostgreSQL Python
It is the time to connect to PostgreSQL server using Python. Now is the time to write some code that will connect to a database and run some SQL queries interacting with that database. We need a database adapter. Psycopg is the most popular PostgreSQL database adapter for the Python programming language. View psycopg2 documentation and install like any other Python package.

'''
pip install psycopg2
'''




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




CREATE a Database in PostgreSQL server
'''
CREATE DATABASE mypythondatabase;
'''
Connect to the Psycopg
To connect to a PostgreSQL database, you need to structure your code as below:

'''
import psycopg2

try:   
    # Connect to the PostgreSQL database
    # Execute SQL Queries

except (Exception, psycopg2.Error) as error :
    # Error Handling

finally:
    # Close PostgreSQL database connection
'''

1- Connect to the PostgreSQL database

'''
import psycopg2

try:
    connection = psycopg2.connect(user = "jamaldiab",
                                  password = "<password>",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "mypythondatabase")
'''

Here we use the connect() function to create a new databse session. Pass the function parameters as a connection string as above.

2- Execute SQL Statements

'''
    cursor = connection.cursor()

    my_query = '''CREATE TABLE Patient(
        PatientId INTEGER PRIMARY KEY,
        PatientFName VARCHAR,
        PatientLName VARCHAR,
        PatientSuburb VARCHAR
        );'''
    
    cursor.execute(my_query)
    
    cursor.close()

    connection.commit()
'''

3- Error Handling

'''
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
'''

3- Close PostgreSQL database connection
'''
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
'''
4- Putting All the pieces together

'''
import psycopg2

try:
    connection = psycopg2.connect(user = "jamaldiab",
                                  password = "<password>",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "mypythondatabase")
                                  
    print("PostgreSQL connection is open")
    
    cursor = connection.cursor()

    my_query = '''CREATE TABLE Patient(
        PatientId INTEGER PRIMARY KEY,
        PatientFName VARCHAR,
        PatientLName VARCHAR,
        PatientSuburb VARCHAR
        );'''
    
    cursor.execute(my_query)
    
    print("PostgreSQL Patient table created")
    
    connection.commit()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
'''

Execute Python code and then connect to mypythondatabase PostgreSQL database to confirm table Patient is created.

Congratulations! You have just created your first PostgreSQL table using python.

# Let’s create a full database using Python

'''
import psycopg2

try:
    connection = psycopg2.connect(user = "jamaldiab",
                                  password = "<password>",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "mypythondatabase")

    print("PostgreSQL connection is open")

    cursor = connection.cursor()
    
    my_query = (
        '''
        CREATE TABLE Patient(
            PatientId INTEGER PRIMARY KEY,
            PatientFName VARCHAR,
            PatientLName VARCHAR,
            PatientSuburb VARCHAR
            )
            ''',
        '''
        CREATE TABLE Doctor(
            DoctorId INTEGER PRIMARY KEY,
            DoctorFName VARCHAR,
            DoctorLName VARCHAR,
            DoctorSuburb VARCHAR
            )
            ''',
        '''
        INSERT INTO Patient
        VALUES (201901,'Jack','D','Rhodes'),
        (201902,'Dan','J','Ryde'),
        (201903,'Rachel','K','Medowbank'),
        (201904,'Karen','L','Rhodes')
        ''',
        '''
        INSERT INTO Doctor
        VALUES (201,'SAM','K','Medowbank'),
        (202,'Mac','B','Rhodes'),
        (303,'Randy','L','Ryde'),
        (404,'Hans','N','Silverwater'),
        (406,'Dan','K','Medowbank'),
        (413,'Mars','B','Rhodes'),
        (423,'Roshan','L','Rhodes'),
        (408,'Brian','N','Silverwater')
        '''    
        )

    for query in my_query:
            cursor.execute(query)
    
    print("PostgreSQL query executed")

    connection.commit()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
'''

# Let’s query our database using Python

'''
import psycopg2

try:
    connection = psycopg2.connect(user = "jamaldiab",
                                  password = "<password>",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "mypythondatabase")

    print("PostgreSQL connection is open\n")

    cursor = connection.cursor()
    
    my_query = (
        '''
        SELECT *
        FROM patient
        '''   
        )
    
    cursor.execute(my_query)

    print("The query retrieved", cursor.rowcount, "records\n")
    
    print("All records are:\n")
    row = cursor.fetchall()
    print(row)

    print("\nThe records are:\n")
    for r in row:
        print(r)

    connection.commit()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("\nPostgreSQL connection is closed")
'''

Database in the Cloud - EC2
Let’s create our first database in the cloud.

1- Create an AWS EC2 Instance
AWS Ubuntu EC2

Quick Reminder: You need a key pair so you can SSH to your EC2 instance. Keep in a safe place. You may want to change access persmissions to avoid any AWS connectivity issues.

'''
chmod 700 [file_name].pem
'''
2- SSH Into EC2 Instance
'''
ssh -i CCC.pem ubuntu@54.198.227.1
'''

-- Note that your key file name and EC2 instance public Ip are different
Note: For detailed instructions on how to create a Ubuntu AWS EC2 Instance, please refer CCC-Term2 AWS Lesson

3- Install PostgreSQL on EC2 Instance
'''
sudo apt install postgresql
'''
4- Start using PostgreSQL

'''
psql postgres
psql: error: could not connect to server: FATAL:  role "ubuntu" does not exist
'''

Oh no! Failed because psql has only one default master role called postgres and we are trying to connect using ubuntu user which does not exist in psql.

You can fix this in different ways:

Switch to postgres account

'''
sudo -i -u postgres
psql
'''

OR

Access psql without switching accounts
'''
sudo -u postgres psql
'''
Connect Python
'''
import psycopg2

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "postgres",
                                  host = "ec2-54-157-144-47.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "postgres")
'''

# Database in the Cloud - AWS RDS
Now is the time to create a database using AWS RDS. Amazon Relational Database Service (RDS) makes it easy to set up, operate, and scale a relational database in the cloud.

Login into AWS Educate and follow the steps:

1- Open AWS RDS Console and click Create database
AWS RDS

2- Choose a database creation method:
AWS RDS

3- Engine Options:
AWS RDS

4- Templates:
AWS RDS

5- Settings:
DB instance identifier: dbinstance_name
Master username: postgres or anyname
Master password: *******
Confirm password: *******
AWS RDS

6- Connectivity:
AWS RDS

7- Additional Connectivity Configuration:
Subnet group: Create new DB Subnet Group
Public Access: Yes
VPC security group: Create new
New VPC security group name: anyname
Availability Zone: No preference
Database port: 5432
AWS RDS

8- Additional Configuration:
AWS RDS

9- Create database
AWS RDS

10- Database Instance Created
AWS RDS

11- View Connectivity details
AWS RDS

12- View Configuration details
AWS RDS

13- Connect to the database
On the terminal on your local computer, use this command to connect to the database.

psql --host=[Endpoint] --port=5432 --username=[username] --password --dbname=[database name]
Example:

psql --host=mydbinstance.cudvrkh0olql.us-east-1.rds.amazonaws.com --port=5432 --username=jamaldiab --password --dbname=myfirstdb
Congratulations! You are in! Feel free to apply everything you have learned but this time in the cloud.

Example

import psycopg2

try:
    connection = psycopg2.connect(user = "jamaldiab",
                                  password = "<password>",
                                  host = "mydbinstance.cudvrkh0olql.us-east-1.rds.amazonaws.com",
                                  port = "5432",
                                  database = "myfirstdb")
                                  
    print("PostgreSQL connection is open")
    
    cursor = connection.cursor()

    my_query = (
        '''
        CREATE TABLE Patient(
            PatientId INTEGER PRIMARY KEY,
            PatientFName VARCHAR,
            PatientLName VARCHAR,
            PatientSuburb VARCHAR
            )
            ''',
        '''
        CREATE TABLE Doctor(
            DoctorId INTEGER PRIMARY KEY,
            DoctorFName VARCHAR,
            DoctorLName VARCHAR,
            DoctorSuburb VARCHAR
            )
            ''',
        '''
        INSERT INTO Patient
        VALUES (201901,'Jack','D','Rhodes'),
        (201902,'Dan','J','Ryde'),
        (201903,'Rachel','K','Medowbank'),
        (201904,'Karen','L','Rhodes')
        ''',
        '''
        INSERT INTO Doctor
        VALUES (201,'SAM','K','Medowbank'),
        (202,'Mac','B','Rhodes'),
        (303,'Randy','L','Ryde'),
        (404,'Hans','N','Silverwater'),
        (406,'Dan','K','Medowbank'),
        (413,'Mars','B','Rhodes'),
        (423,'Roshan','L','Rhodes'),
        (408,'Brian','N','Silverwater')
        '''    
        )

    for query in my_query:
            cursor.execute(query)
    
    print("PostgreSQL Patient table created")
    
    connection.commit()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
Note: The focus here is on the connectivity and not security. Keep in mind hardcoded passwords are not ideal. Consider secured connection methods such as using environmental variables. Also you can prompt the user for a password using getpass().

getpass() sample code:

import psycopg2
import getpass

myp = getpass.getpass("What is your database password: ")

try:
    connection = psycopg2.connect(user = "jamaldiab",
                                  password = myp,
                                  host = "mydbinstance.cudvrkh0olql.us-east-1.rds.amazonaws.com",
                                  port = "5432",
                                  database = "myfirstdb")
Environmental Variables sample Code:

.env

DB_NAME=myfirstdb
DB_USER=jamaldiab
DB_PASSWORD=<password>
DB_HOST=mydbinstance.cudvrkh0olql.us-east-1.rds.amazonaws.com
DB_PORT=5432
Python code

from dotenv import load_dotenv
load_dotenv()

import psycopg2
import os

try:
    connection = psycopg2.connect(user = os.getenv('DB_USER'),
                                  password = os.getenv('DB_PASSWORD'),
                                  host = os.getenv('DB_HOST'),
                                  port = os.getenv('DB_PORT'),
                                  database = os.getenv('DB_NAME'))