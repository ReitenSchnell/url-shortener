## Design assumptions
While designing the service, I assumed following:
1. Our service should generate a shorter and unique alias of an original URL.
2. The alias should have a constant length of 8 characters.
3. Every time an URL is shortened, the result should be different even for the same URL. In production-ready systems this constraint might be relaxed within a user scope.
4. It is very likely that our service will be read-heavy. We assume 10:1 ratio for reads and writes.

#### What could be improved
1. It might be good to have a mechanism for links expiration. Otherwise we will face unnecessary scaling issues on data storage layer (not to mention storage/backups costs). 
2. Such services as ours usually need some API keys issued to the users. This could be used to throttle users, detect and prevent service abuse. 

## How to run the service
Make sure you have following software installed:
- Python 3.5 with pip and virtualenv
- [Tox](https://tox.readthedocs.io/en/latest/) - could be installed by pip
- Docker-compose
- Docker

1. To run unit tests and code style check, hit `tox` command from the project root folder. 
2. To run the service, go to the project root folder and run `docker-compose up -d --build`.
3. When docker containers are built and started, the service could be accessed by `http://localhost:8000`
4. To run integration tests, hit `tox -e integration` command from the project root folder (the integration tests depends on docker container running)

## Design and implementation notes
### Basic system design
1. To encode the original URL, we compute an unique hash (SHA256) of the given URL. This hash is encoded into url-safe base-64 encoding for displaying. Using base64 encoding, an 8 letter long key would result in 64^8 possible strings. Let's assume it's enough for our task.
2. Since it is not possible to infer full URL from the short code, we will have to introduce a data storage into our system.
3. Our data model is key-value pairs (short code as key and original URL as value), therefore the most natural way of storing such data is Redis, working in persistence mode.
4. To resolve possible key duplications, we will check if the key is already taken and generate a new one, if needed.
5. Taking into account that the system should be designed for high load scenarios, the application logic was protected from possible cascading failures by a thin layer of circuit breaker in front of Redis calls.  
### Scaling strategy
Our performance tests showed that default Docker setup allows the service to handle ~400 requests per second (within the assumed read:write ratio).
The application was designed with shared-nothing approach in mind, so it could be easily scaled horizontally:
1. As a first step, we could deploy as many instances of the web application as we need and add a load balancer in front of them.
2. When storage performance becomes a bottleneck, we will introduce master/slave replication to Redis and add load balancer in front of redis slave nodes. After that, we change the application to perform read operations only from Redis slave nodes.
3. When storage volume/memory consumption becomes an issue, we could use partitioning on Redis. At this stage it will be especially important to have data expiration/purging mechanism implemented.
4. If our application starts having performance issues on write operations, we will add message queue to our design. It will allow to parallel URL shortening tasks, decoupling hash generation from writing to storage.


### Technology stack
Below is a brief list of all frameworks and libraries used in the project:
1. Interpreter:	Python version 3.5
2. Web framework: Bottle
3. Database: Redis (supposed to be used with persistence switched on)
4. Web server: Ngnix
5. Circuit breaker: pybreaker
6. Code linter: flake8
7. Unit/integration tests: pytest (with mocks for unit testing), WebTest
8. Coverage tool: pytest-cov
9. Build automation tool: tox
10. Local environments hosted by: docker with docker-compose
11. Performance testing: Gatling

### Project structure
- **infrastructure** folder - contains configuration files for nginx web server and uwsgi middleware along with the entrypoint script _run.sh_ for the application's docker container.
- **integration tests** folder - contains integration tests, that check main application's scenarios.
- **performance_tests** folder - contains Gatling script for running performance testing scenario.
- **shortener_api** folder - contains the application code.
- **tests** folder - folder for the unit tests. Its internal structure mirrors the structure of the code folder.
- **.flake8** - rules for code style check.
- **docker-compose.yaml** - description of project containers and their environment variables.
- **Dockerfile.api** - docker image description for application container.
- **MANIFEST.in** - specifies additional files for python package distribution.
- **requirements.txt** - application dependencies.
- **requirements-dev.txt** - development dependencies, required for running tests, style check, etc.
- **setup.py** - package distribution specification.
- **tox.ini** - build automation description, which includes all steps required for checking code quality.


