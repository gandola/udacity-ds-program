import sys
import re
import pandas as pd 
import pickle

from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

def load_data(database_filepath, table_name='categorized_messages'):
    """
    Loads data from the given database file and given table.
    @param database_filename database file to store the data.
    @param table_name where the data shall be stored.
    @returns a tuple (X,Y,ColsNames) where X is the messages Y are the categories and a list with all column
    names that represents the categories.
    """
    conn_str='sqlite:///{}'.format(database_filepath)
    engine = create_engine(conn_str)
    try:
        df = pd.read_sql('SELECT * FROM {}'.format(table_name), engine)
        print(df.shape)
        category_cols = [col for col in df.columns.tolist() if col not in ['id', 'message','original', 'genre']]
        X = df.message.values
        Y = df[category_cols]
        return (X, Y, category_cols)
    except Exception as e:
        print('Unable to load data from [{}] database.'.format(database_filepath))
        raise e
    finally:
        engine.dispose()
        print('DB: [{}] engine disposed.'.format(database_filepath))

def tokenize(text):
    """
    Tokenizes the given text appling the following transformations:
    - Clean non-alphanumeric chars
    - All chars are lowered 
    - All words are trimmed
    - Lemmatizing
    @param text to be tokenized.
    """
    # remove all non-alphanumeric data.
    text = re.sub('[\W_]+',' ', text)
    
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])
    parameters={}
    cv =  GridSearchCV(pipeline, param_grid=parameters)
    return cv

def evaluate_model(model, X_test, Y_test, category_names):
    """
    Uses the given model to predict with the given test data and logs the metrics per category.
    @param model to be evaluated.
    @param X_test test messages dataset.
    @param Y_test test categories dataset.
    @param category_names list with all categories.
    """
    y_pred = model.predict(X_test)
    _display_categories_report(y_pred, Y_test)

def save_model(model, model_filepath):
    """
    Saves the given model into the given filepath.
    @param model to be stored.
    @param model_filepath location to store the model 
    """
    fo = open(model_filepath, "wb")
    try:
        pickle.dump(model, fo)
        print("Model saved with success!")
    except Exception as e:
        print('Unable to save model at [{}].'. format(model_filepath))
        raise e
    finally:
        fo.close()

def _display_categories_report(y_pred, y_test):
    """
    Displays the classification report of each category predicted.
    
    @param y_pred predicted categories.
    @param y_test categories tested.
    """
    for idx, col in enumerate(y_test):
        print("Category: " + col)
        print(classification_report(y_test[col], y_pred[:, idx]))

def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()