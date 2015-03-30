from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sqlalchemy
import json
import os


REPORTER_PATH = os.path.expanduser('~/Dropbox/Apps/Reporter-App/')
execfile(os.path.expanduser('~/Workspace/datums/models/db.py'))

# Gather all Reporter reports
report_files = [file for file in os.listdir(
    REPORTER_PATH) if file.endswith('.json')]

# Initialize database engine
engine = create_engine('postgresql://jsa@localhost:5432/datums', echo=False,
                       pool_size=100, max_overflow=0)
# Initialize session
Session = sessionmaker(bind=engine)


# Load prompts and response types from questions table
session = Session()
response_types = {str(k): v for k, v in session.query(
    Question.prompt, Question.response_type_id)}
session.commit()


def add_response(record, snapshot):
    '''Given a resonse record, create table instances for that record and
    insert them into the Reporter database.'''
    response_dict = {'snapshot_id': snapshot,
                     'question_prompt': str(record['questionPrompt'])}
    if response_types[response_dict['question_prompt']] in [0, 4]:
        response_dict['response'] = ['Nothing']
    elif response_types[response_dict['question_prompt']] == 1:
        response_dict['response'] = record['answeredOptions']
    elif response_types[response_dict['question_prompt']] == 2:
        response_dict['response'] = record['answeredOptions']
    elif response_types[response_dict['question_prompt']] == 3:
        response_dict['response'] = [str(record['locationResponse']['text'])]
    elif response_types[response_dict['question_prompt']] == 5:
        response_dict['response'] = [int(record['numericResponse'])]

    # Handle common null problem with tokens
    try:
        record['tokens']
    except KeyError:
        pass
    else:
        response_dict['response'] = [
            str(''.join(c for c in i['text'] if ord(c) < 128)) for i in record['tokens']]

    new_response = Response(response_dict)

    # Open a new session
    session = Session()
    session.add(new_response)
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:  # skip records that already exist
        pass


# Add new report records to the database
for report_file in report_files:
    report = os.path.join(REPORTER_PATH, report_file)
    report = json.load(open(report))

    for snapshot in report['snapshots']:
        for response in snapshot['responses']:
            add_response(response, str(snapshot['uniqueIdentifier']))
