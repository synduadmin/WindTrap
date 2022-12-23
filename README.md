# Disclaimer
I'm running a project on digital ocean, and since I need a consolidated logger for a micro-service architecture, and the current log collection plugins were not working for me, I decided to write my own. WindTrap is cloud-agnostic, and can be deployed on all major cloud platforms that support Mongodb, Postgres, Flask, and Python. Using this software allows you to save about 2 days of implementation, and reduce your reliablity on 3rd party services.

# WindTrap
WindTrap is a simple service that can be used to collect events from multiple services and store them in a database, for logging and error resolution, as well as collecting events used later for reporting, data science and machine learning capabilities.

You can use WindTrap to collect events from the web or from a daemon process in your system. Windtrap stores the events in a MongoDB, PostgreSQL db, or to the standard output (which can be log collected for devops and monitoring). All events are sent as JSON objects; It is very easy to query json objects in MongoDB and Postgres, and PG provides extensive support for querying JSON objects.

For example:

```
log=> select distinct data->'host' from log;
```

WindTrap is written in PYTHON, uses the Flask micro-web service framework, and is deployed using Gunicorn on DigitalOcean. Data is inserted into both MongoDB and PostgreSQL databases - you can comment out the db that is irrelevant for you.

Similar guidelines on deploying flask apps on digital ocean can be found here : https://docs.digitalocean.com/tutorials/app-deploy-flask-app/

Since WindTrap relies on JSON and JSONB data types, it requires psycopg2 extensions, which prevents using psycopg2-binary. This means that you need to install the psycopg2 library on your system.


# Why do we need WindTrap?
A common problem in microservice oriented architecture is a the collection of log records into a centralized location.

If the microservices are not connected to a central log collection system, then it is difficult to monitor the health of the system. WindTrap provides a simple way to collect events from multiple services and store them in a database.

When events are collected, the timestamp and timezone of the logger are added to the event; It makes it easier to analyze all system events using a single time zone.
The logger also adds the http headers of the request, which can be used to identify the client, and the user-agent of the client, as well as attempted hacks.

# Why save the data in a database, instead of using Datadog, Elastic, or one of the other tools we have out there?

We live in the age of Data Science. Traditional architectures harvested log data using ETL/ELT and after a delayed period of time, the data was available for analysis. Using WindTrap saves you development of ETL Pipelines on top of your log files (at least while prototyping a system)

Logs are important. Having them collected inside your project, having full ownership and the freedom to customize, reduces your dependency on 3rd party service provider and reduces your projects' cyber attack surface. WindTrap doesn't rely on log4j or any similar library, so if you choose to use it in your application, the risks are reduced.

Postgres is free to use, and costs nothing. Deploying this microservice on a humble server in one of the cloud provider is cheap. You can create this running service in around $10 and 10 minutes.

# What is the format of the events?
Log events are stored in a simple data format which consists of:
1. event_timestamp timestamp with time zone
2. data jsonb
3. status integer
(See log.sql for the DDL required to create the table)

# How to use it?

1. Set up a virtual environment and install the requirements

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
WindTrap uses psycopg2 extension to support JSONB data type. This means that you need to install the psycopg2 library on your system.

2. If you choose to keep logging to both mongo and postgres, leave both functions in place. If you want to use WindTrap with a single database, remove the irrelevant function from the code.

3. Edit the .env file to set the database connection parameters that identify your databases, for both Mongo and Postgres.

4. Create the github repository which will hold your code, and push the code to the repository.

5. Define an app on DigitalOcean, and set the deployment method to Github. Set the branch to main, and the directory to the directory where you have the code. Pay attention that in order to run an app using gunicorn, you must add a "run command" to your app configuration:
   
```
   gunicorn --worker-tmp-dir /dev/shm app:app
```

A full tutorial on deploying flask apps on digital ocean can be found here : https://docs.digitalocean.com/tutorials/app-deploy-flask-app/

6. Set up the database. You can use the log.sql file to create the table in your PG database.

7. Start logging by making http POST calls to your new service. I set up a service function in my apps, which is included in test.py

```

def log_to_api(json):    
    # localhost
    API_ENDPOINT = "http://127.0.0.1:8000/log"
    
    # Sending a post request and saving response as response object
    r = requests.post(url = API_ENDPOINT, json = json)

    # extracting response text 
    return r
    
log_msg = {"app":"middleware", "event":"upgrade completed", "severity":"info"}

r = log_to_api(log_msg)
print(r)

```





