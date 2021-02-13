class Dao:
    """
    Class that represents a generic data access object.
    """

    def __init__(self, connection_str):
        self.connection_str = connection_str

    def get_all_messages(self, ignore_cached=False):
        """
        Gets all messages from the underlying store
        @param ignore_cached if True ignores any cached data and hits the DB directly.
        @return: pandas Dataframe with all messages
        """
        pass

    def store_messages(self, df):
        """
        Stores the given pandas DataFrame into the underlying system.

        @param df: pandas DataFrame to be stored.
        """
        pass

    def get_counts_by_genre(self):
        """
        @return:a tuple including 2 arrays one with values other with genres.
        """
        pass

    def get_counts_by_category(self, df):
        """
        @return:a tuple including 2 arrays one with values other with categories.
        """
        pass
