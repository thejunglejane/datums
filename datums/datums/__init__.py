from . import datums
import glob
import os


REPORTER_PATH = os.environ['REPORTER_PATH']

all_reporter_files = glob.glob(
    os.path.join(os.path.expanduser(REPORTER_PATH), '*.json'))