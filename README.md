### NOTE: IN DEVELOPMENT

Datums is a PostgreSQL pipeline for [Reporter](http://www.reporter-app.com/). Datums will insert records from the Dropbox folder that contains your exported Reporter data into PostgreSQL.

> ["Self-tracking is only useful if it leads to new self-knowledge and—ultimately—new action."](https://medium.com/buster-benson/how-i-track-my-life-7da6f22b8e2c)

# Installation

To install datums, clone this repository and run the setup script
```
$ git clone https://github.com/thejunglejane/datums.git
$ cd datums
$ python setup.py install
```

# Configuration
Rename the .env-example file to .env and fill in your information.

```
export REPORTER_PATH=<your reporter path here>
export DATABASE_URI=postgresql://<your postgres user here>@localhost:5432/datums
export LOG_FILENAME=<your log filename here>
```
If you're not using a tool like [autoenv](https://github.com/kennethreitz/autoenv), you'll need to source the .env after filling in your information.

### Setup the Database
To create the datums database, first ensure that you have postgres installed and that the server is running locally. To create the database
```
$ createdb datums --owner=username
```
where `username` is the output of `whoami`. You're obviously free to name the database whatever you want, just make sure that `DATABASE_URI` refers to the right database.

To setup the schema in the database
```python
>>> from datums.models import base
>>> base.database_setup(base.engine)
```

and to tear down the database (if you ever need to)
```python
>>> from datums.models import base
>>> base.database_teardown(base.engine)
```

The schema is defined in the datums.models module.
[DATA MODEL]

### Populate the Database
The datums.pipeline module allows you to add, update, and delete individual and bulk reports. When you first set datums up, you'll probably want to add all the reports in your Dropbox folder. To do this
```python
>>> from datums import pipeline
>>> from datums.pipeline import add
>>> add.bulk_add_reports(pipeline.all_reporter_files)
```