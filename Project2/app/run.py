import sys
sys.path.append('../')

import json
import plotly
import pandas as pd

from flask import Flask
from flask import render_template, request
from sklearn.externals import joblib
from sqlalchemy import create_engine
from common.utils import tokenize

app = Flask(__name__, static_url_path='/static')

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('categorized_messages', engine)

# load model
model = joblib.load("../models/classifier.pkl")


@app.route('/countsByGenre')
def counts_by_genre():
    """
    Gets number of message by genre API.
    """
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    data = {
        'genre_names': genre_names,
        'genre_counts': genre_counts
    }
    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)


@app.route('/countsByCategory')
def counts_by_category():
    """
    Gets number of message by category.
    """
    category_cols = [col for col in df.columns.tolist() if col not in ['id', 'message', 'original', 'genre']]
    cat_df = df[category_cols]
    results = cat_df[cat_df == 1].count()

    categories = []
    values = []
    for index, value in results.items():
        categories.append(index)
        values.append(value)

    data = {
        'categories': categories,
        'values': values
    }
    return json.dumps(data)


# web page that handles user query and displays model results
@app.route('/classify')
def classify():
    # save user input in query
    query = request.args.get('query', '')

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'classify.html',
        query=query,
        classification_result=classification_results
    )


@app.route('/')
@app.route('/index')
def index():
    # save user input in query
    query = request.args.get('query', '')

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'base.html',
        query=query,
        classification_result=classification_results
    )


@app.route('/genres')
def genres_page():
    return render_template('genres.html')


@app.route('/categories')
def categories_page():
    return render_template('categories.html')


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
