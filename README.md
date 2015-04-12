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

##### Definitions
We should define a few terms before getting into how to use datums

* A **reporter file** is a JSON file that contains all the **report**s for a given day. These files should be located in your Dropbox/Apps/Reporter-App folder. 
* A **report** comprises a **snapshot** and all the **response**s collected by Reporter when you make a report.
* A **snapshot** contains the information that the Reporter app automatically collects when you make a report, things like the weather, background noise, etc.
* A **response** is the answer you enter for a question.

Every **report** will have one **snapshot** and _n_ **response**s associated with it, and every **reporter file** will have _m_ **report**s associated with it, depending on how many times you make reports throughout the day.

## Adding questions and reports
When you first set datums up, you'll probably want to add all the questions and reports in your Dropbox Reporter folder. To do this
```python
>>> from datums.pipeline import add
>>> import glob
>>> import json
>>> all_reporter_files = glob.glob('/path/to/reporter/folder/', '*.json'))
>>> for file in all_reporter_files:
...    with open(os.path.expanduser(file), 'r') as f:
...        day = json.load(f)
...    # Add questions first because reports need them
...    for question in day['questions']:
...        add.add_question(question)
...    for report in day['snapshots']:
...        add.add_report(report)
```

To add the reports from a single file
```python
>>> from datums.pipeline import add
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> for report in day['snapshots']:
...    add.add_report(report)
```

And to add a single report within a file
```python
>>> from datums.pipeline import add
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> report = day['snapshots'][1]  # the second report in the file
>>> add.add_report(report)
```

## Updating reports

If you make a change to one of your Reporter files, or if Reporter makes a change to one of those files, you can also update your reports. If a new report has been added the file at `/path/to/file`, the update will create it in the database.

To update all reports in all the files in your Dropbox Reporter folder
```python
>>> from datums.pipeline import update
>>> import glob
>>> import json
>>> all_reporter_files = glob.glob('/path/to/reporter/folder/', '*.json'))
>>> for file in all_reporter_files:
...    with open(os.path.expanduser(file), 'r') as f:
...        day = json.load(f)
...    for report in day['snapshots']:
...        update.update_report(report)
```

To update all the reports in a single file
```python
>>> from datums.pipeline import update
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> for report in day['snapshots']:
...    update.update_report(report)
```

You can also update an individual report within a file with
```python
>>> from datums.pipeline import update
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> report = day['snapshots'][1]  # the second report in the file
>>> update.update_report(report)
```
#### Changing a Report
While it's possible to change your response to a question from Python, it's not recommended. Datums won't overwrite the contents of your files, and you will lose the changes that you make the next time you update the reports in that file. If you make changes to a file itself, you may run into conflicts if Reporter tries to update that file.

If you do need to change your response to a question, I recommend that you do so from the Reporter app. The list icon in the top left corner will display all of your reports, and you can select a report and make changes. If you have 'Save to Dropbox' enabled, the Dropbox file containing that report will be updated when you save your changes; if you don't have 'Save to Dropbox' enabled, the file containing the report will be updated the next time you export. Once the file is updated, you can follow the steps above to update the reports in that file in the database.

## Deleting reports

Deleting reports from the database is the same. You can delete all reports with
```python
>>> from datums.pipeline import delete
>>> import glob
>>> import json
>>> all_reporter_files = glob.glob('/path/to/reporter/folder/', '*.json'))
>>> for file in all_reporter_files:
...    with open(os.path.expanduser(file), 'r') as f:
...        day = json.load(f)
...    for report in day['snapshots']:
...        delete.delete_report(report)
```

or delete the reports in a single file from the database with
```python
>>> from datums.pipeline import delete
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> for report in day['snapshots']:
...    delete.delete_report(report)
```

And to delete a single report within a file
```python
>>> from datums.pipeline import delete
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> report = day['snapshots'][1]  # the second report in the file
>>> delete.delete_report(report)
```

### Deleting questions

You can also delete questions from the database. Note that this will delete any responses associated with the question as well.

```python
>>> from datums.pipeline import delete
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> question in day['questions'][0]
>>> delete.delete_question(question)
```