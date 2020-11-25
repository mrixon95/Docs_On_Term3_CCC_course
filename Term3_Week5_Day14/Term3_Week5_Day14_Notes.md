Always use HTTPS
Bearer authentication is where a toekn is associated with a user
Json web token JWT is a bearer token
OAUTH - sign in with gmail, facebook etc.
Sign in with a 3rd party service, google redirects people to the website google
Finger print is a username and password

Everytime you create a model you need a schema to go with that model

First Kahoot

Q1. A python package that generates fake data for you
A1. Faker

Q2. To fix the issue of sending an empty title, best to 
A2. Use/Create validator classes

Q3. The __ is where you create an object without exposing its creation logic
A3. Factory Pattern

Q4. An intregration test us used to test that all the modules in our application when integrated work as expected
A4. True

Q5. Hooks that allow us to set things up and tear things down during tests are known as __
A5. Fixtures

 
Q6. __ fixtures will only run before and after all the tests in the module
A6. Class

Q7.  
A7.


Second Kahoot!
Q1. Python ORM
A1. SQLAlchemy

Q2. Flask comes with a nice command to load our Flask app into an interactive shell
A2. Flask shell

Q3. Which of the following is true?
>>> new_book = Book()
>>> new_book.title = "Great Expectations"
>>> db.session.add(new_book)
A3. Still need to run commit

Q4. Which of the following is true?
>>> book = Book.query.filter_by(id = 2).first()
>>> book.title = "Updated title"
>>> db.session.commit()
A4. existing record is updated


Q5. Serialization and Deserialization Python package is marshmallow
A5. Marshmallow

Q6. In Marshmallow we have the function _____ for serialization
A6. Dump

Q7. In Marshmallow we have the function _____ for deserialization
A7. Load

Q8. This will ____
>>> Book.query.all()

A8. View all records




```
DB_URI=postgresql+psycopg2://postgres:QK_cSqG,q8uUFz-F@52.91.5.95:5432/library_api
```
postgres:QK_cSqG,q8uUFz-F@52.91.5.95:5432/library_api

psql --username=postgres --host=52.91.5.95 --port=5432 --dbname=library_api --password



JWT token is made up of 3 parts, a header, payload and verify signature

Header: info about the token


Payload: data about the jwt


Verify signature: Hash of the header, payload and secret



import os
# We are going to have different configuration variables depending on whether
# whether we are in a testing, development or production environment

# We want a different db connection depending on whether we are testing or we are in development

# Robust configuration
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Inherit from Config
class DevelopmentConfig(Config):
    # Development environment specific configuration
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

environment = os.getenv("FLASK_ENV")

# Change the configurations depending on our Flask env

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()





# Factory pattern is where you create an object without exposing its creation logic
def create_app():
    app = Flask(__name__)
    app.config.from_object("default_settings.app_config")

    from database import init_db
    db = init_db(app)

    from flask_marshmallow import Marshmallow
    ma = Marshmallow(app)

    from commands import db_commands
    app.register_blueprint(db_commands)

    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)


    from marshmallow.exceptions import ValidationError

    # Custom error handler
    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return (jsonify(error.messages), 400)

    return app



# We are going to have different configuration variables depending on whether
# whether we are in a testing, development or production environment

# We want a different db connection depending on whether we are testing or we are in development

# Robust configuration

# Add validation rules to the schema


# we format the filename like test_*.py, it will be auto-discoverable by pytest.

```
python3 -m unittest discover -s tests -v
```



```
DB_URI=postgresql+psycopg2://postgres:QK_cSqG,q8uUFz-F@52.91.5.95:5432/library_api
```
postgres:QK_cSqG,q8uUFz-F@52.91.5.95:5432/library_api

psql --username=postgres --host=52.91.5.95 --port=5432 --dbname=library_api --password

QK_cSqG,q8uUFz-F
```
ssh -i ~/.ssh/Term3Week5Day15.pem ubuntu@52.91.5.95
```

```
sudo -i -u postgres psql
```

history 10




eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDYyMDYzMzQsIm5iZiI6MTYwNjIwNjMzNCwianRpIjoiMmYzMzljMjUtY2E5MS00MTM3LWFkMzgtZTA0MjFhNzllZmY0IiwiZXhwIjoxNjA2MjkyNzM0LCJpZGVudGl0eSI6IjUiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.MuizzOKy8MYtCQKnUOOC-oRWnRDBda13xsZ8UvTIjtw



{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDYyMDk1MzMsIm5iZiI6MTYwNjIwOTUzMywianRpIjoiZmQyZjc1MWUtNjkyMy00MjQyLTkwMmEtYzc5OTY3YWE5YWM4IiwiZXhwIjoxNjA2Mjk1OTMzLCJpZGVudGl0eSI6IjEiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ._ndxw1Rwa5Fx45ILpr7FMzsAO0x4lzejNpewuNTM7zU"
}


sudo vim /etc/postgresql/12/main/postgresql.conf

log_statement = all
log_destination = 'stderr'
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_min_error_statement = error

sudo systemctl restart postgresql