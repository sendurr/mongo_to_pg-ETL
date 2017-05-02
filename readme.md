# Data Engineer Practical
Hello, Thank you very much again for applying to Gigster. We are very glad to see you have made it this far and genuinely hope you succeed in the following practical so we get to meet you in person soon.


# Instructions

## Intro
This practical's objective is to ETL data from a MongoDB into a Postgres DB using SQLAlchemy, a Python ORM tool and Alembic, SQLAlchemy’s migration tool. You will be assessed on the following criteria:

* Python proficiency
* Ability to explore an unfamiliar code base and contribute to it
* Ability to explore potentially unfamiliar tools and start using them

## Structure
The project is containerized in docker containers.  One container will be a MongoDB having two collections: gigs and users. One container will be an empty Postgres DB that the ETL will write to. A final container is a Python container where you will do your development in. The purpose of conainerizing is portability and being able to focus on the application rather than the server.

In the python container, under `data-engineer-practical` you will find the the main app: `gigsterpg` . The migrations live under `alembic` . Under `data-engineer-practical/gigsterpg/lib/pg` you will find two folders. `db` holds the “models”. The mapped classes that map a table to a Python object. The `sync` folder holds classes that have a `staticmethod` : `mongo_to_pg`  that extract data from a Mongo DB document and map it to a mapped class.

The entry point for code is `gigsterpg/cli.py` .

## Getting started


* Install docker and docker-compose on your machine.
* Download the practical tar file.
* `cd` into the practical folder extract it: `mkdir data_engineer_practical && tar -xf data_engineer_practical.tar.gzip -C data_engineer_practical/`
*  `cd` into the project root and run `docker-compose build`  if it is the first time upping the containers. After the first time you do not need to `build` . Then run `docker-compose up` .
* To attach to the Python container, `cd` into the root and run `docker-compose run gigster-data-practical bash` . Now you can start your development! be mindful the that the filesystem under `./data-engineer-practical` is volumized.
* To connect to your Postgres DB there are two choices:
  1. Not installing Postgres locally (preferred):
    * Attach to your Postgres container: `docker-compose exec pg bash`
    * run `psql postgres://future_gigster:password@pg:5432/data-practical`  (you may replace `pg` with `localhost`

  2. If you have Postgres locally on your machine:
    * run `psql postgres://future_gigster:password@localhost:5432/data-practical`
* Connecting to your Mongo container is similar, the name of the Mongo DB service is `mongo`

*Note* : There is code in `*/data-engineer-practical/gigsterpg/lib/pg/db/__init__.py` referred to and imported as simply `db` .

*Note* : There is a sample test module for the `skills`  table. The fixtures and setup needed for additional tests are in `conftest.py` . To test, run `pytest` in the project root. `pytest --cov` for test coverage.

## End goal
The end goal is to etl all the data from the MongoDB to Postgres DB with no errors. To run the etl job:


* `cd` into `*/data-practical/gigsterpg`
* run `python -m gigsterpg.cli`

*Note*: The code will fail as it stands. Debuggers are your friends here.

# Tasks

* Complete the `gig.py` mapped class to etl everything except the `upsert` field
* Complete the `user.py` mapped class to etl everything.
* Establish a many to one relationship between `gigs`  and `users` .
* Establish a many to many relationship between `users`  and `skills` .(HINT: use a join table, this means creating your own mapped class module for the join table. Try to include the sync module for the join table as part of the `sync.user` we have populated the skills table for you already.)
* Use `alembic` to create migrations as your schema changes.
* Use `git` to version control.
* Use `pytest` to test your code.


## Rubric


| Criteria                                                            | Points                         |
| ------------------------------------------------------------------- | ------------------------------ |
| Successful ETL run                                                  | 50                             |
| Many-to-many user-skill relationship                                | 30                             |
| One-to-many user-gig relationship                                   | 20                             |
| Tests                                                               | 20 x floor((Test Coverage)/80) |
| Use of Alembic for migrations                                       | 20                             |
| Proper use of containers                                            | 15                             |
| Documentation                                                       | 10                             |
| Flake8 passes                                                       | 10                             |
| Comments                                                            | 5                              |
| Good naming convention and readability                              | 5                              |
| No additional Tests                                                 | -100                           |


A normalized score, by 185, of at least 75% is a passing score.

*Notes*
* You should have all you need to complete the practical in your Python container, but feel free to install any favorite tools you might have.
* The Python debugger, `pdb` will be your friend.
* Feel free to PR often and iterate. An HQ engineer will review your code and provide you with feedback or any question you might have.

## Questions

Please do contact emin@gigster.com should you have any questions regarding the practical.

## Submission

Once you are happy with what you have built, please tar your practical folder  and email it to us: `tar  -czvf data_engineer_practical.tar.gzip PRACTICAL_FOLDER` where PRACTICAL_FOLDER is the folder where your practical is in; if you haven't renamed the folder it should be called `data_engineer_practical`. Best of luck!