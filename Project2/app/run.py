import json
import sys
from os.path import dirname, join, abspath

from flask import Flask
from flask import render_template, request
from sklearn.externals import joblib

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from data.dao_sqlite import SQLiteDao
from common.utils import tokenize

app = Flask(__name__, static_url_path='/static')

# Data Access Object
dao = SQLiteDao('sqlite:///../data/DisasterResponse.db')

# load model
model = joblib.load("../models/classifier.pkl")


@app.route('/countsByGenre')
def counts_by_genre():
    """
    Gets number of message by genre API.
    """
    genre_names, genre_counts = dao.get_counts_by_genre()
    data = {
        'genre_names': genre_names,
        'genre_counts': genre_counts
    }
    return json.dumps(data)


@app.route('/countsByCategory')
def counts_by_category():
    """
    Gets number of message by category.
    """
    categories, values = dao.get_counts_by_category()
    data = {
        'categories': categories,
        'values': values
    }
    return json.dumps(data)


# web page that handles user query and displays model results
@app.route('/classify')
def classify():
    """
    API that allows to classify a message given by request param named "query"
    @return: classification results.
    """
    # save user input in query
    query = request.args.get('query', '')

    df = dao.get_all_messages()

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'classify.html',
        query=query,
        classification_result=classification_results
    )


@app.route('/genres')
def genres_page():
    return render_template('genres.html')


@app.route('/categories')
def categories_page():
    return render_template('categories.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
