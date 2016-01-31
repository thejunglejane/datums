#!/bin/bash
REPORTER_PATH=$HOME/Dropbox/Apps/Reporter-App

# Get yesterday's date
YESTERDAY=$(date -v -1d +"%Y-%m-%d")
# Add the reports from the file dated yesterday to the database
datums --add $REPORTER_PATH/$YESTERDAY-reporter-export.json
