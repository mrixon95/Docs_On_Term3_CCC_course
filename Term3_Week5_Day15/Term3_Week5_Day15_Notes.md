sudo apt update

python --version

pip3 --version

sudo apt install python3-pip

git --version

export JWT_SECRET_KEY=michaelrixon



See environment variables
```
env
```


```
python3 -m flask db upgrade
```

```
python3 -m flask db-custom seed
```

```
python3 -m flask run -h 0.0.0.0
```


http://3.87.93.151:5000/books





This lesson requires this repo.

Deployment Intro
We have a Flask application which we would like to deploy to the cloud. In this case that is to an AWS EC2 instance. Before we setup any CI/CD pipleline we first need to know the steps necessary that we need to automate.

So lets do everything manually in the beginning and then automate in the end.

First off we are going to need two differenct EC2 instances. One for our database and the other for our Flask application. Remember if we can separate the pieces of our application it is a good thing. That is because we can now indvidually control the resources and security each piece needs.

So lets get our database up and running first. There are minimum hardware requirements when running a Postgres database. Most noteably is the 2GB of RAM. Which means we cannot use a micro instance. Instead use a t2.small EC2 instance running on the latest version of Ubuntu.

Once that is running SSH into the instance so that we can install Postgres.

Setup Postgres on the EC2 instance.

Now that Postgres is setup lets create an EC2 instance to run our application.

Setup an EC2 instance to run the Flask application.

We will test all of this has worked by trying to create the database tables from the EC2 instance that has our Flask application on it.

python3 -m flask db upgrade
No errors, which is a good sign. And if we check the tables with pgAdmin…yep they are there!

Even though this is production lets seed our database to see if we can get some data coming through the api.

python3 -m flask db-custom seed
And finally lets run our flask application so that it will accept any IP connection.

python3 -m flask run -h 0.0.0.0
Ok it is running.

Load

Now I just need to visit the publice IP address of the EC2 instance in the browser specifying port 5000.

Load

Connection timeout!

Hmmm….oh yea I need to update the security group running flask to allow incoming port 5000 connections for any IP address!

Load

Now if I refresh the browser….

Load

It works! I just don’t have a route setup for / so lets try going to /books instead.

Load

Load Testing
Ok so our current setup isn’t the best. What would happen if we exited SSH? Would flask still run?

What if flask crashes will it restart automatically?

Before we answer those questions lets look at another one first. At the moment we have made a pretty big assumption. That assumption is that since our flask application is up and running any and all users will be able to use it successfully and without issue.

However reality is a little different.

Remember our computers only have a finite number of resources availble in CPU and RAM but each request made to API is going to need to take some amount of those resources. Also it depends on how the code was written if your computer will fully utilise the resources available or will it bottleneck itself.

One strategy to test the different scenarios of users actually using our API is through load testing.

“Load testing generally refers to the practice of modeling the expected usage of a software program by simulating multiple users accessing the program concurrently.” -Wikipedia

So basically we just send out API requests to simulate real user load. We could do that by getting hundreds or thousands of our friends (you have a thousand friends right?), to all make requests at the same time. But that probably isn’t feasbile.

Instead we are going to fake the traffic by automating it. We could write this script ourselves but there is actually a very cool Python package out there made specifically for load testing named locust.

Since we will be using locust to test out our Flask application it makes sense to install the configuration for locust with the app as well. The default file name for locust is locustfile.py but you can name it something else if you’d like. You would just need to specify the correct file when running locust. We will stick to locustfile.py for now.

touch locustfile.py
And now to install locust.

pip install locust
The focus of this lesson isn’t to teach you how to use locust but we will go over the below code:

from locust import HttpUser, task, between
from faker import Faker
import uuid
import random
import time

class QuickstartUser(HttpUser):
    wait_time = between(1,4)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.books = []
        self.faker = Faker()
        self.token = None
    
    def on_start(self):
        id = str(uuid.uuid4())
        while self.token == None:
            try:
                self.client.post(
                    "/auth/register", 
                    json={"email": f"test{id}@test.com", "password":"secret"}
                )
                response = self.client.post(
                    "/auth/login", 
                    json={"email": f"test{id}@test.com", "password":"secret"}
                )
                self.token = response.json()["token"]
            except:
                time.sleep(3)
    
    @task
    def index_page(self):
        self.client.get("/books/")
    
    @task(3)
    def create_book(self):
        if self.token:
            response = self.client.post(
                "/books/",
                json={ "title": self.faker.catch_phrase() },
                headers={ "Authorization": f"Bearer {self.token}"}
            )
            if response.status_code < 400:
                self.books.append(response.json()["id"])
    
    @task(2)
    def update_book(self):
        if len(self.books) > 0 and self.token:
            book_id = random.choice(self.books)
            self.client.put(
                f"/books/{book_id}", 
                json={ "title": self.faker.catch_phrase() },
                headers={ "Authorization": f"Bearer {self.token}"}
            )
    
    @task(2)
    def delete_book(self):
        if len(self.books) > 0 and self.token:
            book_id = random.choice(self.books)
            response = self.client.delete(
                f"/books/{book_id}",
                headers={ "Authorization": f"Bearer {self.token}"}
            )
            if response.status_code < 400:
                self.books.remove(book_id)
So whenever we run our load test we will tell locust how many users we would like to fake. For each user locust will create an object based on our class.

The on_start() method will be called once for each new user created. This is why we are registering a new user and logging them in to receive our JWT. From there locust will call the methods we have decorated with @task at random. We can make a task more likely to be selected by assigning them a weight. For example a normal task has a weight of 1 if we were to modify this like we did create_book, we gave it @task(3), that means this task is 3 times more likely to be selected.

The last important piece in our class is the wait_time attribute. This tells locust how long to wait before running another another task. We have chosen to give it a between value of 1 and 4. Which means locust will wait between 1 and 4 seconds before it runs another task for this user.

Now that is all setup we just need to run the locust command from our flask application directory.

I will be running this command from my local machine and not an ec2 instance

locust
Load

By default locust will accept connections from any ip address (0.0.0.0) on port 8089. So I will visit that in the browser.

Load

Now just enter the details of your load test and start running! I will be using 200 total users which will spawn every 4 seconds.

Load

Ok so everything is running now, and yep new users and books are being created. Wait holy crap is the response time climbing above 30 seconds!

Load

Wait I am getting errors now too!

Load

But everything was working before! What the heck happened?

This is why load testing is so valuable. It allows up to mimic network load so we can see when things start to fail with either really slow response times or other types of errors.

Keep in mind at some point you application will fail. No one has 100% uptime. This is a truth we all need to accept. Even services in AWS only offer 4, 9’s (99.99%) of availability in a given year. That equates to 52 minutes and 35 seconds of downtime.

Once we accept this we can start planning for how we are going to deal with these failures when they occur.

Logging
Before we can deal with any failure though we must first know when it occured and what the failure was. At the moment we were able to see the error because we were ssh’d into the machine running the flask server.

But is someone always going to be watching this?

No they are not!

So now we are going to need to come up with a solution for how we will track these errors. Now there are a whole bunch of different solutions available to us. We could send out an email everytime something happens. Maybe we start sending logs to a centralised repository with sophisticated reporting and charts. But lets start from the basics. And that is we would like to write all the errors that occur in a file so that we can go back through them later.

Python actually has a logging module within its standard library.

Flask already uses this module so we just need to tap into it as well. Lets create another file that will hold all of our custom logging setup.

touch log_handlers.py
We will be using the TimedRotatingFileHandler class from Pythons logging module to create a log that will also auto rotate everyday.

import os
import logging
from logging.handlers import TimedRotatingFileHandler

log_dir = os.path.join(os.getcwd(), 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_handler = TimedRotatingFileHandler(os.path.join(log_dir, '_current.log'), when="midnight")
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
Now that this is all setup we need to add it to the application but only if the environment value is set to “production”. We don’t really need to log in development mode since we will actively be monitoring during that time and we don’t need it during testing as well. So in our main.py file we will add the handler just after loading the app configuration.

app.config.from_object("default_settings.app_config")

if app.config["ENV"] == "production":
    from log_handlers import file_handler
    app.logger.addHandler(file_handler)
Now we will have logs in production when errors are thrown. Lets add this to our GIT repo so that we can pull it down in our ec2 instance. Before that though we need to add the logs directory to our .gitignore.

logs/*
#on local machine
git add .
git commit -m "adding in logging capabilities to production"
git push
#on ec2 instance
git pull
If we run locust again and start receiving errors we can see that those errors are now being written into a log!

Error Investigation Deep Dive
So everything is deployed and errors are being logged right now but shouldn’t we be fixing the error we are receiving? Yes we should.

Lets take a look at the error we have been getting once more API calls start coming in.

sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30 (Background on this error at: http://sqlalche.me/e/13/3o7r)
If we follow the link given in this error SQLAlchemy lets us know that:

This is possibly the most common runtime error experienced, as it directly involves the work load of the application surpassing a configured limit.

Which is exactly what is happening to us. Only when our server is put under a heavy workload does this error occur.

Basically what is happening here is that our application is trying to create a maximum of 10 database connections at any given time. However we are exceeding that limit because of the heavy load.

If you Google this error you will receive some StackOverflow advice about increasing the max number of connections in the QueuePool by setting a configuration value in Flask but is this really the answer? What if we go to 1000 users will we run into our issue again?

So StackOverflow may have the correct answer (decision pending) but we need to look at this at a deeper level and truly understand the issue since we are trying to be the best developers we can be.

Why is it that 100 users is fine but 200 is not? Also how is it that 100 users if fine but we just saw that we have a max of 10 connections to the database?

According the SQLAlchemy docs connections to the database remain open and are re-used where appropriate. Basically everytime you connect to the database there is a time cost. So to speed everything up SQLAlchemy will make a decision to keep database connections open so when another API call comes in, it can reuse that connection. That is why 10 connections can service 100 users. Once one API call is done using the connection it is given to an incoming, waiting API call.

So it looks like this error occurs when there are to many backlogged API requests trying to get a database connection.

Now that we understanding this, where is the bottlneck occurring that is throwing this error? Is it the:

Database not responding fast enough (slow queries)
API requests not releasing connections once they are finished
Application not processing API requests quick enough, so they are getting log jammed
From our load testing we saw a spike in the time it took to respond to requests, which means the 3rd option in our list is a likely canidate for the issue. So then how can we speed up our application? Before we answer that question we need to understand how our instance is actually running our app.

Remember whenever we execute our script that is creating a new process. A process is given its own section of resources by the operating system, like a memory address and call stack. What this means is that if one process fails it shouldn’t interfere with other processes running on our computer. For example whenever Google Chrome locks up we still have the ability to use our mouse and keyboard to shut it down forcefully. If the Chrome process failing effected other processes such as they keyboard and mouse then everything would freeze.

That wouldn’t be good!

Lets check out the Flask process with top while locust is sending it requests from 50 users to see how it is running.

top -o PID
Ok looks like there is only a single process running our Flask application which is to be expected.

Load

And it is using up a good amount of the CPU. At the moment mine is taking up 72%. According to locust the average response time is also 600ms for an API request.

What if we were to run our flask application on a t2.medium instance insead of a micro? According to the AWS docs they have the same speed CPU in them at 3.3 GHz. So our application shouldn’t see a performance boost right?

Give it a try: setup the application again on a t2.medium and run locust against it with 50 users.

Interesting our repsonse time is still averaging 600ms but our CPU usage is significantly lower at 14%. Lets try blasting this one with 200 users as well.

Ok its running……and running…..and running…..what the heck we are not get the error we had before! Also during the load test on our t2.micro we were seeing response times upwards of 35 seconds during the user spawning phase but on the t2.medium is isn’t getting above 12 seconds. What the heck is going on. The CPU has the exact same speed!

That is because the t2.medium CPU has 2 cores where the t2.micro has 1. So how exactly is Flask taking advantage of this extra core and how does it work? Well that is with threads.

In our past Python programs we have been using a single thread, that means our code is blocking. As soon as you hear the word blocking you immediately think that it must be bad. But that is not true. Blocking code just means that it must finish before the next line of code can be processed. Think about a long running loop. No code after the loop will run before the the loop finishes. Which means the loop is blocking the execution of the next line of code.

This is normally how we want our applications to behave because most likely code further down the file needs the result of other code previous code.

But what if you didn’t need to wait for one some code to finish before you ran the next bit. For example the HTTP requests coming into our Flask application are unique. We don’t need the result from a prior HTTP request to start processing another one. Actually this would be bad thing if we did have to wait.

If one user made an API request that took 5 seconds to complete then all other HTTP requests would need to wait for that one to finish before they got their response!

So how do we make certain parts of our code non-blocking or asynchronous. Well that is through the use of threads. A process can have as many threads as it likes. But depending on the CPU the code running in those threads may run concurrently, in parallel or a bit of both.

A CPU can only make a single calculation at a time so even if we are using threads each part of our program really isn’t running at the same time. Instead our CPU will do part of the code on 1 thread then switch to the next and so on until the code on a thread is completely executed. The switching between completing these different pieces of code in different threads is happening so fast that it gives the illusion that both threads are executing at the same time. That is known as concurrency.

Multi-core CPU’s can actually perform multiple calculations at the same time. For example a 2 core CPU can execute 2 threads in parallel. So no switch back and forth is necessary. However if you were to run 4 threads on a 2 core CPU then 2 threads would be run concurrently on each core but those 2 thread would run in parralell to the other 2 threads running concurrently in the other core.

I know another mind explosion.

By default Flask breaks up incoming HTTP into threads. We can actually view the threads being created via top if we know the PID of the flask process.

top -p <PID> -H
Load

You can see for my Flask application it was running 3 threads at this time. So thats why our t2.medium was able to process incoming HTTP requests faster than our t2.micro. It wasn’t because the CPU was going any faster but because it was able to divide the work between its 2 cores.

So it looks like our bottleneck that was giving us an error really was how fast our API requests were being processed.

Web Server Gateway Interface
Threads are awesome and can really speed up our application by taking advantage of multi-core CPU’s but they are not without limitations. For example if a single thread were to truly crash not just raise an exception.

Such as running out of memory, cyclical function call (functions calling each other forever), etc. Then it would actually crash the whole process.

Lets simulate a process crash by creating a route in our auth_controller.py.

@auth.route("/crash", methods=["GET"])
def auth_crash():
    import os
    os._exit(1)
Now GIT commit that code, push it up to GitHub and then pull in down on your ec2 instance. Ok start up the Flask application and start sending requests via locust.

Everything should be running nice and smoot but if we go to GET /auth/crash in our browsers we see an error screen.

Load

Not only that but our entire Flask application stopped running! So our entire API is down! Crap, one bad request in a thread was able to stop the whole process.

So what is the solution? We definitely don’t want our entire API to go down.

Wait didn’t we say before that processes are isolated from each other? So what if we could run multiple Flask processes? But wait that wouldn’t really work right because each time we run flask run it is getting bound to a port. So the different processes would be running on different ports which still isn’t a good thing.

Looks like we have ran into one of the limitations of the Flask dev server. Actually it is recommended you don’t use the Flask dev server in production. Because it is less secure, not as stable and was never meant to handle large traffic volume.

Have you not been paying attention to the warning we have been receiving everytime we start it up in production mode.

Load

Really the Flask development server is there as a convience for when we are developing and not suppose to be used in production.

Instead we will use a production ready HTTP server that implements the Web Server Gateway Interface or WSGI for short.

Before we chose our web server we need to understand what the WSGI exactly is.

Our Flask application should only be concerned about how to process and generate a response to a given HTTP request. It should not be concerned with how that HTTP request was received in the first place. It shouldn’t care about any of the networking stuff such as IP addresses and ports.

That should be the responsibility of a different application (HTTP web server). But if we split up this functionality into two separate components those components need a common interface to be able to talk with one another.

This is why PEP 333 was created to define the WSGI. Which is either a simple function or class init that has 2 parameters, environ & start_response. Super simple!

Now we don’t have to worry about creating this interface because Flask already does that for us, which is awesome.

All we need to do is choose a WSGI compliant HTTP web server. Currently one of the most popular is gunicorn.

So we will be using that in our production deployment. First we need to install it.

pip install gunicorn
Now all we need to do is run gunicorn and tell it how it can create new instances of our applications.

gunicorn -b 0.0.0.0 "main:create_app()"
We can see gunicorn starting up.

Load

The interesting this is that it says it has booted something called a worker with a process id of 67064.

If we take a look at the processes running via top we can see that gunicorn actually has 2 processes! One is the master process and the other is known as a worker. The worker process is responsible for running our Flask application. The master processs job is to give different workers different HTTP requests based on load and if a worker is terminated the master will restart that process.

Give it a try: kill the worker process that gunicorn has created. What happens?

We can actually tell gunicorn how many workers we would like. But it really just all depends on the cores we have in our computer. You won’t get any benefit out of running 20 workers if you CPU only has 2 cores (concurrency vs parallelism). So the best formula to use when specifying to gunicorn how many workers it should create is CPU core + 1.

Because our t2.medium instance has two cores we would run gunicorn with 3 workers.

gunicorn -b 0.0.0.0 -w 3 "main:create_app()"
Systemd
Wow we have been solving alot of different problems but we have finally arrived at our last one.

The problem is what if our gunicorn master process goes down?

Well because all the workers are child processes of the master process that means all of the workers will also close.

Which means we are right back where we started! Also at the moment we have been running gunicorn as a foreground process instead of a background process, that means if we exit ssh then gunicorn will also shut down.

Another consideration is if we do run gunicorn as a background process how will it get the environment variables necessary for our flask application to run?

Also what if we take a backup of our instance. It would be nice if when we booted up the backup our Flask application automatically started as well.

After considering all of these requirements the best solution would be to allow systemd to manage gunicorn for us.

Systemd is the default init system for most major Linux distributions. An init system is the very first process that is started by your operation system. This process then starts up and manages all other necessary processes.

Basically if systemd were to ever crash then all other processes on your computer would crash as well since systemd is the parent to everything else.

This makes systemd a great choice for managing gunicorn for us.

sudo touch /etc/systemd/system/flaskapi.service
sudo vim /etc/systemd/system/flaskapi.service
Inside of this file we will create a new unit

[Unit]
Description=Gunicorn managing flask application
After=network.target
This tells systemd we want to start this service after the network is connected. Which makes sense because it will be booting an HTTP server.

Next we will create the service.

[Unit]
Description=Gunicorn managing flask application
After=network.target

[Service]
EnvironmentFile=/home/ubuntu/.env
User=ubuntu
WorkingDirectory=/home/ubuntu/ccc-03-14
ExecStart=/home/ubuntu/.local/bin/gunicorn -b 0.0.0.0:5000 -w 3 "main:create_app()"
Restart=always
The EnvironmentFile is where will will define the environment variables necessary to run this service. We will run it as the ubuntu User from the WorkingDirectory path by using the command in the ExecStart value. Finally we let systemd know that if this programs exits for any reason we want it to Restart always.

Finally we add the last section.

[Unit]
Description=Gunicorn managing flask application
After=network.target

[Service]
EnvironmentFile=/home/ubuntu/.env
User=ubuntu
WorkingDirectory=/home/ubuntu/ccc-03-14
ExecStart=/home/ubuntu/.local/bin/gunicorn -b 0.0.0.0:5000 -w 3 "main:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
This is basically telling systemd we would like this service to be start automatically on boot if we enable it. Once you’ve done this save the file.

Before w start up our service we need to create that .env file for our environment variables.

vim /home/ubuntu/.env
In the file just declare the variables as normal (export is not required).

FLASK_ENV=production
JWT_SECRET_KEY=reallysecretstuff
DB_URI=postgresql+psycopg2://flask:ducksandpumpkins@ec2-100-27-11-88.compute-1.amazonaws.com/flask_app_db
Save the file.

Awesome now to reload the sysemd configuration.

sudo systemctl daemon-reload
Our service should now be available.

sudo systemctl status flaskapi
Load

Sweet it found it! Now to start it up.

sudo systemctl start flaskapi
And then check the status again.

Load

Looks like it is working, if we go to GET /books in the browser…..yep it is working!

Finally if we would like this service to be started when the instance starts up we just need to enable it.

sudo systemctl enable flaskapi
Now try stopping your ec2 instance and check the endpoint….yep it isn’t working since the instance is stopped.

And start it back up again and check it (the IP address might have changed)……holy cow it works!