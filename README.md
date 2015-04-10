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
export REPORTER_PATH=<your Reporter Dropbox path here>
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
The datums.pipeline module allows you to add, update, and delete individual and bulk reports. 

##### Bulk
When you first set datums up, you'll probably want to add all the reports in your Dropbox folder. To do this
```python
>>> from datums import pipeline
>>> from datums.pipeline import add
>>> add.bulk_add_reports(pipeline.all_reporter_files)
```

`pipeline.all_reporter_files` is a list of all the JSON files in the `REPORTER_PATH` specified in your .env. If you make a change to one of those files, or if Reporter makes a change to one of those files, you can also update all your reports in bulk. If a new report has appeared, the bulk update will create it in the database, too.
```python
>>> from datums import pipeline
>>> from datums.pipeline import update
>>> add.bulk_update_reports(pipeline.all_reporter_files)
```

And, the same with bulk deleting reports. You can just tear down the database with `base.database_teardown()`, or you can bulk delete all reports with
```python
>>> from datums import pipeline
>>> from datums.pipeline import delete
>>> add.bulk_delete_reports(pipeline.all_reporter_files)
```

You can also pass a single filename, or your own list of filenames, to `add.bulk_add_reports()`. Because each file contains _n_ reports for a given day, this is still a bulk operation.

##### Individual
To add, update, or delete individual reports, datums expects a dictionary

```python
>>> from datums import pipeline
>>> from datums.pipeline import update
>>> first_file = pipeline.all_reporter_files[0]
>>> with open(first_file, 'r') as f:
...     reports = json.load(f)
>>> first_snapshot = reports['snapshots'][0]
>>> update.add_report(first_snapshot)
```

# TODO: define the terms: report, report file, snapshot, response, question
