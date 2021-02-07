import sys
import pandas as pd
from sqlalchemy import create_engine  

def load_data(messages_filepath, 
              categories_filepath, 
              messages_file_encoding="utf-8", 
              categories_file_encoding="utf-8"):
    """
    Loads data from the given CSV files using the given corresponding encoding.
    
    @param messages_filepath: Messages data CSV file path.
    @param categories_filepath: Categories data CSV file path.
    @param messages_file_encoding: Messages file encoding.
    @param categories_file_encoding: Categories file encoding.
    @returns Returns a pandas DataFrame with messages and categories merged by id.
    """
    messages_df = pd.read_csv(messages_filepath, encoding=messages_file_encoding)
    categories_df = pd.read_csv(categories_filepath, encoding=categories_file_encoding)
    return pd.merge(messages_df, categories_df, on=["id"], how="inner")

def clean_data(df):
    """
    Transforms the given raw data and returns a DataFrame cleaned, deduplicated 
    and with all categories expanded to actual columns.
    
    @param df: Raw dataframe read from the sources.
    @returns Returns a DataFrame cleaned.
    """
    # Resolve categories and expand them to actual columns.
    categories_df = _resolve_categories(df['categories'])
    df = df.drop(columns=['categories'])
    df = pd.concat([df, categories_df], axis=1)
    
    # drop duplicates
    df = _drop_duplicates(df)
    return df
    
def _resolve_categories(categories_df):
    """
    Given a Dataframe corresponding to the categories dataframe, parses and expands it to have a column per category 
    and the corresponding values.
    This method assumes that each category row is given in the format <category1>-<value1>;<category2>-<value2>;...
    
    @param df DataFrame contaning the column with the expected categories format.
    @returns a df with all categories as columns and the corresponding values.
    """
    categories = categories_df.str.split(';',expand=True)
    row = categories.iloc[0]
    category_colnames = row.apply(lambda colname: colname.split('-')[0])
    categories.columns = category_colnames
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda value: value.split('-')[1])
        # convert column from string to numeric
        categories[column] = categories[column].astype("int")
    return categories
        
def _drop_duplicates(df):
    """
    Drops all duplicates from the given DataFrame.
    
    @param df DataFrame contaning all messages to drop.
    @returns a df copy with all duplicates dropped.
    """
    rows_before = df.shape[0]
    df = df.drop_duplicates()
    rows_after = df.shape[0]
    print("Number of Rows: before:[{}], after:[{}], dropped_rows:[{}]"
           .format(rows_before, rows_after, (rows_before - rows_after)))
    return df
    
def save_data(df, database_filename, table_name='categorized_messages'):
    """
    Saves the given dataframe to the given database into the given table. 
    
    @param df DataFrame contaning all messages to store.
    @param database_filename database file to store the data.
    @param table_name where the data shall be stored.
    """
    conn_str='sqlite:///{}'.format(database_filename)
    engine = create_engine(conn_str)
    try:
        df.to_sql(table_name, engine, index=False) 
        print('Stored, columns:[{}], rows:[{}]!'.format(df.shape[1], df.shape[0]))
    except Exception as e:
        print('Unable to store the data into [{}] database.'. format(database_filename))
        raise e
    finally:
        engine.dispose()
        print('DB: [{}] engine disposed.'. format(database_filename))
    
def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()