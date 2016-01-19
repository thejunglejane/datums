![datums_header](images/header.png)

[![Code Climate](https://codeclimate.com/github/thejunglejane/datums/badges/gpa.svg)](https://codeclimate.com/github/thejunglejane/datums)
 
Datums is a PostgreSQL pipeline for [Reporter](http://www.reporter-app.com/). Datums will insert records from the Dropbox folder that contains your exported Reporter data<sup>[1](#notes)</sup> into PostgreSQL.

> ["Self-tracking is only useful if it leads to new self-knowledge and—ultimately—new action."](https://medium.com/buster-benson/how-i-track-my-life-7da6f22b8e2c)

# Getting Started

## Create the Database

To create the datums database, first ensure that you have postgres installed and that the server is running locally. To create the database
```
$ createdb datums --owner=username
```
where `username` is the output of `whoami`. You're obviously free to name the database whatever you want, just make sure that when you declare the database URI below that it points to the right database.

## Installation

#### pip
```
$ pip install datums
```

datums relies on one environment variable, `DATABASE_URI`. I recommend creating a virtual environment in which this variable is stored, but you can also add it to your .bash_profile (or equivalent) to make it available in all sessions and environments.

Run the following command inside a virtual environment to make `DATABASE_URI` accessible whenever the environment is active, or outside of a virtual environment to make `DATABASE_URI` accessible only in your current Terminal session. To make `DATABASE_URI` available in all Terminal sessions and environments, add the following line to your .bash_profile (or equivalent)
```bash
export DATABASE_URI=postgresql://<your postgres user here>@localhost:5432/datums
```

#### GitHub

Alternatively, you can clone this repository and run the setup script
```
$ git clone https://github.com/thejunglejane/datums.git
$ cd datums
$ python setup.py install
```
You can rename the .env-example file in the repository's root to .env and fill in the `DATABASE_URI` variable information. You'll need to source the .env after filling in your information for the variable to be accessible in your session.

Note that the `DATABASE_URI` variable will only be available in your current Terminal session. If you would like to be able to use datums without sourcing the .env everytime, I recommend creating a virtual environment in which this variable is stored or adding the variable to your .bash_profile (or equivalent).

### Setup the Database

You should now have both the `datums` executable and Python library installed and ready to use.

Before adding any reports, you'll need to setup the database schema. The database schema is defined in the `models` module. Here's a picture

![data_model](images/data_model.png)

You can setup the database from the command line or from Python. From the command line, execute `datums` with the `--setup` flag.
```
$ datums --setup
```
or, from Python
```python
>>> from datums.models import base
>>> base.database_setup(base.engine)
```

You can also teardown the database, if you ever need to. This will remove all the tables from the database, but won't delete the database. To teardown the database from the command line, include the `--teardown` flag
```
$ datums --teardown
```
or, from Python
```python
>>> from datums.models import base
>>> base.database_teardown(base.engine)
```

# Adding, Updating, and Deleting
The `pipeline` module allows you to add, update, and delete reports and questions.

### Definitions
We should define a few terms before getting into how to use the pipeline.

* A **reporter file** is a JSON file that contains all the **snapshot**s and all the **question**s for a given day. These files should be located in your Dropbox/Apps/Reporter-App folder. 
* A **snapshot** comprises a **report** and all the **response**s collected by Reporter when you make a report.
* A **report** contains the information that the Reporter app automatically collects when you make a report, things like the weather, background noise, etc.
* A **response** is the answer you enter for a question.

Every **snapshot** will have one **report** and some number **response**s associated with it, and every **reporter file** will have some number **snapshot**s and some number of **question**s associated with it, depending on how many times you make reports throughout the day. 

If you add or delete questions from the Reporter app, different **reporter file**s will have different **question**s from day to day. When you add a new **reporter file**, first add the **question**s from that day. If there are no new **question**s, nothing will happen; if there is a new **question**, datums will add it to the database.

## Adding questions, reports, and responses

When you first set datums up, you'll probably want to add all the questions, reports, and responses in your Dropbox Reporter folder.

#### Command Line
To add all the Reporter files in your Dropbox Reporter folder from the command line, execute `datums` with the `--add` flag followed by the path to your Dropbox Reporter folder

```
$ datums --add "/path/to/reporter/folder/*.json"
```
Make sure you include the '*.json' at the end to exclude the extra files in that folder. 

To add the questions and reports from a single Reporter file, include the filepath after the `--add` flag instead of the directory's path
```
$ datums --add "/path/to/file"
```

#### Python
You can add all the Reporter files or a single Reporter file from Python as well.

```python
>>> from datums.pipeline import add
>>> import glob
>>> import json
>>> import os
>>> all_reporter_files = glob.glob(os.path.join('/path/to/reporter/folder/', '*.json'))
>>> for file in all_reporter_files:
...    with open(os.path.expanduser(file), 'r') as f:
...        day = json.load(f)
...    # Add questions first because reports need them
...    for question in day['questions']:
...        add.add_question(question)
...    for snapshot in day['snapshots']:
...        # Add report and responses
...        add.add_snapshot(snapshot)
```
```python
>>> from datums.pipeline import add
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> # Add questions first because reports need them
>>> for question in day['questions']:
...     add.add_question(question)
>>> for snapshot in day['snapshots']:
...    # Add report and responses
...    add.add_snapshot(snapshot)
```

You can also add a single snapshot from a Reporter file, if you need/want to
```python
>>> from datums.pipeline import add
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> report = day['snapshots'][n]  # where n is the index of the report
>>> add.add_report(report)
```

## Updating reports and responses

If you make a change to one of your Reporter files, or if Reporter makes a change to one of those files, you can also update your reports and responses. If a new snapshot has been added the file located at '/path/to/file', the update will create it in the database.

#### Command Line

To update all snapshots in all the files in your Dropbox Reporter folder

```
$ datums --update "/path/to/reporter/folder/*.json"
```
and to update all the snapshots in a single Reporter file
```
$ datums --update "/path/to/file"
```

#### Python
From Python
```python
>>> from datums.pipeline import update
>>> import glob
>>> import json
>>> import os
>>> all_reporter_files = glob.glob(os.path.join('/path/to/reporter/folder/', '*.json'))
>>> for file in all_reporter_files:
...    with open(os.path.expanduser(file), 'r') as f:
...        day = json.load(f)
...    for snapshot in day['snapshots']:
...        update.update_snapshot(snapshot)
```
```python
>>> from datums.pipeline import update
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> for snapshot in day['snapshots']:
...    update.update_snapshot(snapshot)
```

To update an individual snapshot within a snapshoter file with
```python
>>> from datums.pipeline import update
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> snapshot = day['snapshots'][n]  # where n is the index of the snapshot
>>> update.update_snapshot(snapshot)
```
#### Changing a Snapshot
> While it is possible to change your response to a question from Python, it's not recommended. Datums won't overwrite the contents of your files, and you will lose the changes that you make the next time you update the snapshots in that file. If you make changes to a file itself, you may run into conflicts if Reporter tries to update that file.

> If you do need to change your response to a question, I recommend that you do so from the Reporter app. The list icon in the top left corner will display all of your snapshots, and you can select a snapshot and make changes. If you have 'Save to Dropbox' enabled, the Dropbox file containing that snapshot will be updated when you save your changes; if you don't have 'Save to Dropbox' enabled, the file containing the snapshot will be updated the next time you export. Once the file is updated, you can follow the steps above to update the snapshots in that file in the database.

## Deleting reports and responses

Deleting reports and responses from the database is much the same. 

#### Command Line
You can delete all snapshots in your Dropbox Reporter folder with
```
$ datums --delete "/path/to/reporter/folder/*.json"
```
and the snapshots in a single file with
```
$ datums --delete "/path/to/file"
```

#### Python
```python
>>> from datums.pipeline import delete
>>> import glob
>>> import json
>>> import os
>>> all_reporter_files = glob.glob(os.path.join('/path/to/reporter/folder/', '*.json'))
>>> for file in all_reporter_files:
...    with open(os.path.expanduser(file), 'r') as f:
...        day = json.load(f)
...    for snapshot in day['snapshots']:
...        delete.delete_snapshot(snapshot)
```
```python
>>> from datums.pipeline import delete
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> for snapshot in day['snapshots']:
...    delete.delete_snapshot(snapshot)
```

To delete a single snapshot within a Reporter file
```python
>>> from datums.pipeline import delete
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> snapshot = day['snapshots'][n]  # where n is the index of the snapshot
>>> delete.delete_snapshot(snapshot)
```

## Deleting questions

You can also delete questions from the database. Note that this will delete any responses associated with the deleted question as well.

```python
>>> from datums.pipeline import delete
>>> import json
>>> with open('/path/to/file', 'r') as f:
...    day = json.load(f)
>>> question = day['questions'][n]  # where n is the index of the question
>>> delete.delete_question(question)
```

# Notes

1. This version of datums only supports JSON exports.

# Licensing

Datums is licensed under the MIT License, so please share, enjoy, and improve.

Copyright (c) 2015 Jane Stewart Adams

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
