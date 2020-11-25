MVC means that view and model do not talk to each other.
__init__.py is automatically run when the module it is in is imported
every table in your database gets a model
jsonify does not know how to take an object and convert it to json

Kahoot Questions

Q1: CREATE ROLE jack PASSWORD 'jack' LOGIN;
A1: Can login only

Q2: CREATE ROLE dan PASSWORD 'dan' LOGIN CREATEDB;
A2: Both login and create db

Q3: CREATE ROLE sam PASSWORD 'sam' LOGIN CREATEDB CREATEROLE;
A3: Can Login, Create Database and Create role

Q4: CREATE ROLE kaz PASSWORD 'kaz' LOGIN SUPERUSER;
A4: Can Login, Create Database and Create role

Q5: CREATE ROLE kaz PASSWORD 'kaz' SUPERUSER;
A5: Create Database and Create role

Q6: CREATE ROLE sal PASSWORD 'sal' LOGIN SUPERUSER;
A6: sal can drop a database she does not own

Q7: How can you list all the roles in the psql server
A7: \du

Q8: How to connect a specific role to a database in psql server?
A8: \c database_name role_name







Connect to ec2 instance
```
ssh -i ~/.ssh/Term3Week4Day11.pem ubuntu@52.91.70.92
```

check the status of postgresql
```
sudo systemctl status postgresql
```

connect to postgresql
```
sudo apt-get update
```

connect to postgresql
```
sudo apt-get install postgresql
```



```
sudo apt-get update
```




```
sudo apt-get install postgresql -y
```

show where config file is located
```
sudo -u postgres psql
```


```
show config_file;

```

```
cd /etc/postgresql/12/main/postgresql.conf
```




```
sudo vim postgresql.conf


ALTER ROLE postgres WITH PASSWORD 'QK_cSqG,q8uUFz-F';
```

```
psql --host=52.91.70.92 --port=5432 --username=postgres --dbname=library_api --password
```

psql: error: could not connect to server: could not connect to server: Connection refused
        Is the server running on host "52.91.70.92" and accepting
        TCP/IP connections on port 5432?


Timing out means check the security group.
Super quick error means you got past the security group



```


```
sudo vim postgresql.conf
```

```
change listen_addresses from localhost to all (*)
listen_addresses = '*'
```

```
sudo systemctl status postgresql
```

```
sudo systemctl stop postgresql
```


```
sudo systemctl start postgresql
```

```
psql --host=52.91.70.92 --port=5432 --username=postgres --dbname=library_api --password
```

```
ALTER ROLE postgres WITH PASSWORD 'QK_cSqG,q8uUFz-F';
```

Gives different error


psql: error: could not connect to server: FATAL:  no pg_hba.conf entry for host "124.148.176.30", user "postgres", database "library_api", SSL on
FATAL:  no pg_hba.conf entry for host "124.148.176.30", user "postgres", database "library_api", SSL off



Think about it like a building with a club you want to go in to.
There's a door to get into the building - that is aws security inbound groups
Then there is a door to get into the club - config file
Finally there is a bouncer who checks if you are on the list - pg_hba.conf


```
sudo -u postgres psql
```

```



```
sudo vim pg_hba.conf
```


in pg_hba.conf its deny by default
also you can do explicit denies

add 
```
host    all    all    0.0.0.0/0    md5
```

```
sudo systemctl restart postgresql
```


```
pip3 install python-dotenv
```

```
git push --force
```


MVC pattern which stands for Model, View, Controller is a good way to split up code
Flask is unopinated which means we can structure our code anyway we want


Lesson Requirements

A fork of this git repo
A Postrgres database created named ‘library_api’ with a user ‘app’ that has password ‘Testing1’
Modular Programming
Lets begin by taking a look at a simple Flask application which consists of a single file named main.py.

from flask import Flask, request, jsonify
app = Flask(__name__)
import psycopg2

connection = psycopg2.connect(
    database="library_api",
    user="app",
    password="Testing1",
    host="localhost"
)

cursor = connection.cursor()

cursor.execute("create table if not exists books (id serial PRIMARY KEY, title varchar);")
connection.commit()

@app.route("/books", methods=["GET"])
def book_index():
    #Return all books
    sql = "SELECT * FROM books"
    cursor.execute(sql)
    books = cursor.fetchall()
    return jsonify(books)

@app.route("/books", methods=["POST"])
def book_create():
    #Create a new book
    sql = "INSERT INTO books (title) VALUES (%s);"
    cursor.execute(sql, (request.json["title"],))
    connection.commit()

    sql = "SELECT * FROM books ORDER BY ID DESC LIMIT 1"
    cursor.execute(sql)
    book = cursor.fetchone()
    return jsonify(book)

@app.route("/books/<int:id>", methods=["GET"])
def book_show(id):
    #Return a single book
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@app.route("/books/<int:id>", methods=["PUT", "PATCH"])
def book_update(id):
    #Update a book
    sql = "UPDATE books SET title = %s WHERE id = %s;"
    cursor.execute(sql, (request.json["title"], id))
    connection.commit()

    sql = "SELECT * FROM books WHERE id = %s"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@app.route("/books/<int:id>", methods=["DELETE"])
def book_delete(id):
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    
    if book:
        sql = "DELETE FROM books WHERE id = %s;"
        cursor.execute(sql, (id,))
        connection.commit()

    return jsonify(book)




In this file we are doing alot of different things. We are initiating the Flask application, connecting to the database, defining our routes and writing logic for our routes all in the same file.

Think about if we want to add in even more routes or do more complex operations such as authentication. This file is going to get very messy and hard to maintain very very quickly!

Remember when we write our functions we want to follow the single responsibility principle. This principle essentail boils down to a function should only do one thing and it should do that one thing really well.

We can also apply this principle to the files which hold our code. Basically we can break apart our code into seperate files which are solely responsible for a certain part of our application. This is known as modularization.

Now there are many different ways and patterns we can follow when modularizing code which we will talk about a little later. But before we dive into that lets just apply this concept by using our own logic.

Remember at the moment we have this file structure:

- main.py
Looking at code we have the first thing that comes to mind is moving the database connection and table creation into it’s own file named database.py.

import psycopg2

connection = psycopg2.connect(
    database="library_api",
    user="app",
    password="Testing1",
    host="localhost"
)

cursor = connection.cursor()

cursor.execute("create table if not exists books (id serial PRIMARY KEY, title varchar);")
connection.commit()
Now that is split out we can just import what we need into main.py.

from flask import Flask, request, jsonify
app = Flask(__name__)
from database import cursor, connection
And when we run our application……yep it still works!

So now our file structure looks like this:

- main.py
- database.py
Flask Blueprints
The next logical piece that looks like it could be split out into a separate file is all of our routes and functions decorated with those routes.

However if you take a look at one of the functions.

@app.route("/books", methods=["GET"])
def book_index():
    #Return all books
    sql = "SELECT * FROM books"
    cursor.execute(sql)
    books = cursor.fetchall()
    return jsonify(books)
It looks like we will need access to the app variable within our new file. Now we could pass around the app variable from file to file but this is actually considered bad practice.

Instead Flask gives us the ability to create what is known as a blueprint. You can think of a blueprint as code which describes how to construct a part of your application. This will make more sense once we use one.

Lets create a new file named books.py. This is where we will move all of our routes and functions to.

@app.route("/books", methods=["GET"])
def book_index():
    #Return all books
    sql = "SELECT * FROM books"
    cursor.execute(sql)
    books = cursor.fetchall()
    return jsonify(books)

@app.route("/books", methods=["POST"])
def book_create():
    #Create a new book
    sql = "INSERT INTO books (title) VALUES (%s);"
    cursor.execute(sql, (request.json["title"],))
    connection.commit()

    sql = "SELECT * FROM books ORDER BY ID DESC LIMIT 1"
    cursor.execute(sql)
    book = cursor.fetchone()
    return jsonify(book)

@app.route("/books/<int:id>", methods=["GET"])
def book_show(id):
    #Return a single book
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@app.route("/books/<int:id>", methods=["PUT", "PATCH"])
def book_update(id):
    #Update a book
    sql = "UPDATE books SET title = %s WHERE id = %s;"
    cursor.execute(sql, (request.json["title"], id))
    connection.commit()

    sql = "SELECT * FROM books WHERE id = %s"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@app.route("/books/<int:id>", methods=["DELETE"])
def book_delete(id):
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    
    if book:
        sql = "DELETE FROM books WHERE id = %s;"
        cursor.execute(sql, (id,))
        connection.commit()

    return jsonify(book)
But like we said before we shouldn’t import the app variable into this file. Instead lets setup a blueprint.

from database import cursor, connection
from flask import Blueprint, request, jsonify
books = Blueprint('books', __name__)

@books.route("/books", methods=["GET"])
def book_index():
    #Return all books
    sql = "SELECT * FROM books"
    cursor.execute(sql)
    books = cursor.fetchall()
    return jsonify(books)

@books.route("/books", methods=["POST"])
def book_create():
    #Create a new book
    sql = "INSERT INTO books (title) VALUES (%s);"
    cursor.execute(sql, (request.json["title"],))
    connection.commit()

    sql = "SELECT * FROM books ORDER BY ID DESC LIMIT 1"
    cursor.execute(sql)
    book = cursor.fetchone()
    return jsonify(book)

@books.route("/books/<int:id>", methods=["GET"])
def book_show(id):
    #Return a single book
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@books.route("/books/<int:id>", methods=["PUT", "PATCH"])
def book_update(id):
    #Update a book
    sql = "UPDATE books SET title = %s WHERE id = %s;"
    cursor.execute(sql, (request.json["title"], id))
    connection.commit()

    sql = "SELECT * FROM books WHERE id = %s"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@books.route("/books/<int:id>", methods=["DELETE"])
def book_delete(id):
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    
    if book:
        sql = "DELETE FROM books WHERE id = %s;"
        cursor.execute(sql, (id,))
        connection.commit()

    return jsonify(book)
Pretty easy. We just use the Blueprint() class from Flask to instantiate a new blueprint object and then use that in the exact same way we’d use app. You will also notice that these functions need acccess to our database so we had to import that file here as well.

Now to actually make our blueprint work with our app we need to register our blueprint in main.py.

from flask import Flask
app = Flask(__name__)
from books import books
app.register_blueprint(books)
And when we run our app….it still works!

Now our file structure looks like this:

- main.py
- database.py
- books.py
We are really starting to modularize! Another cool thing when we create or register a blueprint is that we can define a url prefix. Which is just an additional pattern to be matched in the url when using the blueprint. This comes in really handy when we have a bunch of routes that have the same beginning in their url.

For example all of the routes for our books resource begin with /books. Lets move that out of all of our routes and instead have it defined on our blueprint.

#books.py

from database import cursor, connection
from flask import Blueprint, request, jsonify
books = Blueprint('books', __name__, url_prefix="/books")

@books.route("/", methods=["GET"])
def book_index():
    #Return all books
    sql = "SELECT * FROM books"
    cursor.execute(sql)
    books = cursor.fetchall()
    return jsonify(books)

@books.route("/", methods=["POST"])
def book_create():
    #Create a new book
    sql = "INSERT INTO books (title) VALUES (%s);"
    cursor.execute(sql, (request.json["title"],))
    connection.commit()

    sql = "SELECT * FROM books ORDER BY ID DESC LIMIT 1"
    cursor.execute(sql)
    book = cursor.fetchone()
    return jsonify(book)

@books.route("/<int:id>", methods=["GET"])
def book_show(id):
    #Return a single book
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@books.route("/<int:id>", methods=["PUT", "PATCH"])
def book_update(id):
    #Update a book
    sql = "UPDATE books SET title = %s WHERE id = %s;"
    cursor.execute(sql, (request.json["title"], id))
    connection.commit()

    sql = "SELECT * FROM books WHERE id = %s"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    return jsonify(book)

@books.route("/<int:id>", methods=["DELETE"])
def book_delete(id):
    sql = "SELECT * FROM books WHERE id = %s;"
    cursor.execute(sql, (id,))
    book = cursor.fetchone()
    
    if book:
        sql = "DELETE FROM books WHERE id = %s;"
        cursor.execute(sql, (id,))
        connection.commit()

    return jsonify(book)
Now if we ever need to move our books resource to a different url it will be easy since we only have to make that change in one place rather than several!

MVC
Ok so everything is split up, nice and modular now but it feels like we are going to run into a problem if our app continues to grow. At the moment we have just been naming stuff, kinda just off the cuff.

Also what if we start having more and more endpoints inside our application. It would be nice to group all of those files together based on functionality. And more importantly have some guidelines in place for what exactly that functionality is. Like what is it suppose to do and what is too much.

Developers have experienced this problem many times when modularizing their own code. And from that different patterns have been created on how to split up your code, what to name your files when you do split it up and what exactly each sections responsibility is.

We will take a look at the MVC pattern which stands for Model, View, Controller.

Before we dive into MVC and how the pattern works I want to clarify that Flask in unopinionated, meaning we can strucutre our code in any way we want. If you were to google different flask applications you’d probably see a bunch of different ways those developers have chosen to split up their code. The reason we are going to use MVC isn’t because it is necessarily the best way to modularize a flask application.

However the MVC pattern is extremely popular and something that you will most certainly run into. For example the other popular web framework Django is based off of the MVC pattern with a slight twist.

So understanding this pattern is very helpful when moving into other frameworks.

Here is how a pure MVC based implementation is suppose to function.

MVC

So from this diagram when a http request comes in from the right the first thing that happens is the route is pattern matched.

Those routes are attached directly to different controllers. Based on the match a controller is called.

The controllers main job is business logic. However if the controller needs to access or manipulate the database it must use a model. The model is the only object with a direct connection to the database.

Also if the controller needs to do something more than just reply with plain text such as with HTML, it hands off the responsibility of creating that HTML to an object known as the view.

If the view needs information from the database to perform its job, such as creating a nice HTML table of orders, the controller must first use a model to get that information and then the controller hands that information to the view to use. The view and model never talk directly!

Finally it is the controllers responsibility to put together the HTTP response and send it back to the user.

So in our MVC model each abstraction has clear responsibilities. The model interacts with the database, the view assembles the information that will be given back to the user and the controller is additonal logic and the glue between thew view and model.

So lets modify our flask application a bit to fit this pattern.

First we will create a new directory named controllers so our file structure now looks like this:

* controllers
- books.py
- database.py
- main.py
Now that we have that directory we will move our books.py into the controllers directory and rename that file to books_controller.py.

So now it should look like this:

* controllers
    - books_controller.py
- database.py
- main.py
The next thing we are going to do is create a file in the controllers directory that will import all of the controllers we would like registered on the application.

We will name this file as __init__.py. This is a Python convention for packages. Packages are just groupings of modules.

* controllers
    - __init__.py
    - books_controller.py
- database.py
- main.py
Now lets fill out the __init__.py file.

from controllers.books_controller import books

registerable_controllers = [
    books
]
Nice! The last thing to do is to import the registerable_controllers variable into our main.py and register all the controllers!

from flask import Flask
app = Flask(__name__)
from controllers import registerable_controllers

for controller in registerable_controllers:
    app.register_blueprint(controller)
Awesome! We have now grouped together our Blueprints which have routes within them as controllers. This way if we ever want to add in new routes or modify existing ones they should be much each to find and manage!

Object Relational Mapping
Ok our controllers are done but if we take a peek inside of the books controller we can see that we are using a database connection directly in the controller! According to our MVC pattern this is a big no no.

Instead we need to abstract this connection and any queries we would like to do on the database into a model. But before we do that lets talk about a concept known as object relational mapping or ORM for short.

An ORM is used for converting data between incompatible systems. For example at the moment we have a Python application which has data types such as string, int, float, boolean, etc and we also have a database which stores information in its own data types like varchar, date, time, etc.

So an ORM lets us easily convert Python data types into the appropriate Postgres data types and vice versa. The package that we have currently been using for our database connection and manipulation isn’t really an ORM. Instead its main purpose is a Python database adapter to allow us to connect to a database and when we pull information out it makes a best guess for the most appropriate data type in Python.

So while we are moving our database code out of the controller to follow the MVC pattern, lets also implement an ORM to make our lives even easier in the future whenever we need to query the database.

The ORM we will be using is SQLAlchemy, which at the time of this lesson is the most popular Python ORM.

First off we will need to install the SQLAlchemy package. There is actually an extension package for SQLAlchemy, aimed directly at use within a flask application.

pip install flask-sqlalchemy
Ok now we have the package installed lets setup it up in our database.py file.

We do have a decision to make though. It looks like according to the docs for Flask SQLAlchmey to work it needs the main app instance. But we just said passing around the app instance isn’t the greatest idea.

So instead what we will do is create function which will take the app as an argument, that we we don’t have to import app into our database file.

from flask_sqlalchemy import SQLAlchemy

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://app:Testing1@localhost:5432/library_api"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    return db  
Ok so we setup our function that takes in the application instance and in the function we are setting a couple of configuration values on the application (we will come back into configuration in more detail later). But the thing to notice here is that SQLAlchemy is looking for a connection string that is broken down like this:

database+adapter://user:password@host:port/dbname
From there we create a new instance of SQLAlchemy and return it from the function.

Now we just need to call this function in main.py

from flask import Flask
app = Flask(__name__)

from database import init_db
db = init_db(app)

from controllers import registerable_controllers

for controller in registerable_controllers:
    app.register_blueprint(controller)
Sweet we have our ORM with the database connection! However when we are dealing with an ORM we need to be explicit about the mapping. This is where our model is going to come into play.

So lets create a new directory named models and inside that directory we will create a file named Book.py.

* controllers
    - __init__.py
    - books_controller.py
- database.py
- main.py
* models
    - Book.py
Now that we have that directory and file setup lets fill out the Book.py file.

Flask SQLAlchemy using the SQLAlchemy declaritive api, so if you’d like to know everything it is capable of doing please refer to those.

We will just go over the common use case.

First off we need to import our database from main.py since that is holding all the Flask SQLAlchemy goodness we need.

from main import db
Next we need to delcare a class with the name of our model which inherits from the Model class on db. The convention for naming a model is to use the singular version of the name of the table we will be accessing. So since the table is named books…..yep our model will be name Book. However SQLAlchemy will look for a table name with the exact name of the class, just in lowercase, so we will need to set the __tablename attribute to tell SQLAlchemy which table we would like it to connect to.

from main import db

class Book(db.Model):
    __tablename__ = "books"
Ok looking good. The next thing we need to do is define the mapping inside of this class. Basically we need to map every column we’d like to access in our database to an attribute on the class.

The way we do that is like this:

from main import db

class Book(db.Model):
    __tablename__ = "books"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
Awesome now this is setup lets give it a try in our book_controller.

I am going to comment out all the other routes except for book_index so we can just focus on one thing at a time. I won’t show the other functions in the examples just yet.

from models.Book import Book
from main import db
from flask import Blueprint, request, jsonify
books = Blueprint('books', __name__, url_prefix="/books")

@books.route("/", methods=["GET"])
def book_index():
    #Return all books
    pass
Ok so we have imported the model and db into our controller and removed the code inside our book_index function. Now we just need to figure out how to use the model.

Whenever it comes to messing around with elements we have setup in a Flask app. I like to experiment with them using the shell. Flask actually comes with a nice command to load our Flask app into an interactive shell session.

flask shell
Flask

Now that is started lets import the model so that we can play around with it. We will also need the database variable.

from model.Book import Book
from main import db
Now that we have the Book model available lets explore some different methods the ORM makes available.

If we want to add a record to the books table we just need an instance of Book with the attributes we’d like inserted. Then we need to hand that instance to the database.

Flask

We are not quite done yet though. Basically what we have done is stage the change. We haven’t actually added the new record to the database. To do that we still need to run commit().

Flask

Now our record is in the database. To view all of records we can create a query like this:

Flask

Nice! If we want to update a record we just need to retrieve it from the database, update the attributes we’d like and then commit.

Flask

Finally to delete a record we just call delete() instead of add()

Flask

With out new knowledge about the ORM and different methods available to use lets fill out the book_index() function in the books_controller.

from models.Book import Book
from main import db
from flask import Blueprint, request, jsonify
books = Blueprint('books', __name__, url_prefix="/books")

@books.route("/", methods=["GET"])
def book_index():
    books = Book.query.all()
    return jsonify(books)
Aright now that we have this setup lets go to the /books route and……oh no an error!

Flask

Serialization & Deserialization
So the reason we have this error is because SQLAlchemy return a list of objects from the database and the jsonify() function doesn’t know how to convert and object to JSON.

Instead what it does know is how to take Python data types such as lists, tuples, dictionaries, numbers and strings and convert those to JSON.

To solve our problem we will need to run the objects through some type of process to create dictionary representations of what we wanted from the object so that it can actually be converted to a JSON string. This process is what is known as serialization. When we serialize an object we are generating a representation of what that object looks like in another data type (normally a string).

The process of deserialization is to take a representative piece of data and convert it back into the object it was representing. So in our case either taking a Python dictionary or string and converting it back into a SQLAlchemy object.

We could write up this process ourselves but just like before this seems like a problem other developers would have already run into so there is most likely a 3rd party package out there that will help us with this problem. The package that we are going to be using for serialization and deserialization is Marshmallow.

So lets get the Flask version installed.

pip install flask-marshmallow marshmallow-sqlalchemy
Now that we have that installed lets set it up.

First we need to setup Marshmallow with our Flask application in main.py

from flask import Flask
app = Flask(__name__)

from database import init_db
db = init_db(app)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

from controllers import registerable_controllers

for controller in registerable_controllers:
    app.register_blueprint(controller)
Now that is taken care of we will need to create a schema. Schemas are how we give SQLAlchemy to Marshallow for it to serialize and deserialize.

We will create a new directory to hold our schemas and a BookSchema.py, so our file structure will now look like this:

* controllers
    - __init__.py
    - books_controller.py
- database.py
- main.py
* models
    - Book.py
* schemas
    - BookSchema.py
And now to fill in BookSchema.py

from main import ma
from models.Book import Book

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

book_schema = BookSchema()
books_schema = BookSchema(many=True)
Pretty easy right. What we have just followed the docs to get this all setup.

What we did is tell Marshallow to automatically generate its schema based on the attributes from the SQLAlchemy model.

Then we created two different schema objects we will use. One for a single SQLAlchemy object and the other for a list of objects.

Now to put this in action in our books_controller.py. In Marshmallow we have a dump() method for serialization and load() for deserialization.

from models.Book import Book
from main import db
from schemas.BookSchema import book_schema, books_schema
from flask import Blueprint, request, jsonify
books = Blueprint('books', __name__, url_prefix="/books")

@books.route("/", methods=["GET"])
def book_index():
    books = Book.query.all()
    return jsonify(books_schema.dump(books))
And………..it works!

Now to just fill out the rest of our functions.

from models.Book import Book
from main import db
from schemas.BookSchema import book_schema, books_schema
from flask import Blueprint, request, jsonify
books = Blueprint('books', __name__, url_prefix="/books")

@books.route("/", methods=["GET"])
def book_index():
    #Retrieve all books
    books = Book.query.all()
    return jsonify(books_schema.dump(books))

@books.route("/", methods=["POST"])
def book_create():
    #Create a new book
    book_fields = book_schema.load(request.json)

    new_book = Book()
    new_book.title = book_fields["title"]
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify(book_schema.dump(new_book))

@books.route("/<int:id>", methods=["GET"])
def book_show(id):
    #Return a single book
    book = Book.query.get(id)
    return jsonify(book_schema.dump(book))

@books.route("/<int:id>", methods=["PUT", "PATCH"])
def book_update(id):
    #Update a book
    books = Book.query.filter_by(id=id)
    book_fields = book_schema.load(request.json)
    books.update(book_fields)
    db.session.commit()

    return jsonify(book_schema.dump(books[0]))

@books.route("/<int:id>", methods=["DELETE"])
def book_delete(id):
    #Delete a book
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return jsonify(book_schema.dump(book))

