import pandas as pd
from sqlalchemy import create_engine

from .dao import Dao


class SQLiteDao(Dao):
    """
    SQLLite implementation of Data Access Object.
    """

    def __init__(self, connection_str):
        super().__init__(connection_str)
        self.engine = create_engine(self.connection_str)
        self.messages_table = "categorized_messages"
        self.cachedMessages = None

    def get_all_messages(self, ignore_cached=False):
        if self.cachedMessages is None or ignore_cached:
            self.cachedMessages = pd.read_sql_table(self.messages_table, self.engine)
        return self.cachedMessages

    def store_messages(self, df):
        self.cachedMessages = df
        self.cachedMessages.to_sql(self.messages_table, self.engine, index=False)

    def get_counts_by_genre(self):
        df = self.get_all_messages()
        results = df.groupby('genre').count()['message']

        genre_names = []
        genre_counts = []
        for index, value in results.items():
            genre_names.append(index)
            genre_counts.append(value)

        return genre_names, genre_counts

    def get_counts_by_category(self):
        df = self.get_all_messages()
        category_cols = [col for col in df.columns.tolist() if col not in ['id', 'message', 'original', 'genre']]
        cat_df = df[category_cols]
        results = cat_df[cat_df == 1].count()

        categories = []
        values = []
        for index, value in results.items():
            categories.append(index)
            values.append(value)

        return categories, values

    def __del__(self):
        if self.engine:
            self.engine.dispose()
