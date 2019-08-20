# Bright.md exercise

## Create a micro-service with the following:

- A User rest Resource that allows clients to create, read, update, delete a user or a list of users.

- You can use a database of your choice but it's also fine to just use a map or dictionary in memory to keep track of users by their ids.

- Use structured logging

- Add Metrics (such as dropwizard, codahale, or prometheus to time routes)

- Write unit tests for the service.

- Generate a code coverage report (for Java you can use the jacoco-maven-plugin for unit test coverage).

- If you are using Java take a look at: https://www.dropwizard.io/1.3.5/docs/getting-started.html

- The user JSON can just be id, first name, last name, zip code, and email address. If Java, the User class should be immutable.

- You can use Java, GoLang, or Python for this exercise. 

### Usage:

- ensure virtual environment is Python 3.7+
- install requirements `pip install -r requirements.txt`
- export PYTHONPATH=./
- run application `make run`
- run in debug mode `make debug`
- run tests `make test`
- I've included a postman collection since I ran out of time to get full coverage on the api tests

### Resources:
https://dev.to/rhymes/logging-flask-requests-with-colors-and-structure--7g1
