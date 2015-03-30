from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import os


DATUMS_MODEL_PATH = os.environ['DATUMS_MODEL_PATH']
DATUMS_DB = os.environ['DATUMS_DB']  # postgres engine string
REPORTER_PATH = os.environ['REPORTER_PATH']

execfile(DATUMS_MODEL_PATH)  # Load table classes

# Gather all Reporter reports
report_files = [file for file in os.listdir(
    REPORTER_PATH) if file.endswith('.json')]

initial_report_file = os.path.join(REPORTER_PATH, report_files[0])
initial_report = json.load(open(initial_report_file))

# Map response type ids to response types
response_type_ids = {0: 'tokens', 1: 'multiple choice', 2: 'yes/no',
                     3: 'location', 4: 'people', 5: 'number'}

question_response_types = {}
for question in initial_report['questions']:
    question_response_types[str(question['prompt'])] = question['questionType']


# Initialize database engine
engine = create_engine('postgresql://jsa@localhost:5432/datums', echo=False)
# Initialize session
Session = sessionmaker(bind=engine)


# Add questions to the database
for k, v in question_response_types.items():
    question_dict = {'prompt': k, 'response_type_id': v,
                     'response_type': response_type_ids[v]}
    new_question = Question(question_dict)

    session = Session()
    session.add(new_question)
    session.commit()
