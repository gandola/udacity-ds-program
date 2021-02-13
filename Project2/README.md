# Disaster Response Pipeline Project

### Project Motivation
Normally, in disaster scenarios there is to quickly classify messages coming from the various sources.
This allows humanitarian organization to have better and faster responses.

This Web App that allows users to classify automatically messages coming from disaster scenarios using a simple RandomForest 
classification model.

There are two more pages that allow users to verify the training data by:
- Genre
- Category

### Structure
- **data/**: Contains code to store, load messages internally.
- **models/**: Contains the code for models.
- **app/**: Contains all the code for the WebApplication.
- **resources/**: Notebooks used to support the development.

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

### Run Tests:
    `python test`
