from pandas.api.types import is_numeric_dtype

def fill_nans_with_mean(df, columns):
    """
    Fills the given columns NaN values with the mean of the column.
    """
    for col in columns:
        if col in df.columns:
            df[col].fillna((df[col].mean()), inplace=True)
    return df

def fill_nans_with_mode(df, columns):
    """
    Fills the given columns NaN values with the mode of the column.
    """
    for col in columns:
        if col in df.columns:
            df[col].fillna((df[col].mode()), inplace=True)
    return df

def find_numeric_columns_with_nans(df):
    """
    Returns all numeric columns that have NaN values.
    """
    cols_with_nans = [] 
    for col in df.columns:
        if is_numeric_dtype(df[col]) and df[col].isnull().values.any():
            cols_with_nans.append(col) 
    return cols_with_nans


def clean_price(df):
    """
    Cleans price field column and casts to float type. 
    """
    return df['price'].str.replace(',', '').str.replace('$', '').astype(float)

def create_pricing_groups(df):
    """
    Create 5 pricing groups.
    - low: < 25q
    - medium-low: >= 25q and < 40q
    - medium: >= 40q and < 65q
    - medium-high:  >= 65q and < 75q
    - high: > 75q
    """
    quantiles = df.price.quantile([0.25, 0.40, 0.65, 0.75])
    q25 = quantiles.iloc[0]
    q40 = quantiles.iloc[1]
    q65 = quantiles.iloc[2]
    q75 = quantiles.iloc[3]
    return df['price'].apply(lambda price: price_range(price, q25, q40, q65, q75))
    
def price_range(price, q25, q40, q65, q75):
    """
    Given a price and the repecting price quantiles it returns a string with the pricing group.
    """
    if (price > 0 and price < q25):
        return 'low'
    elif (price >= q25 and price < q40):
        return 'medium_low'
    elif (price >= q40 and price < q65):
        return 'medium'
    elif (price >= q65 and price < q75):
        return 'medium_high'
    elif (price >= q75):
        return 'high' 
    return None

def get_model_coefs(model, X):
    """
    Gets the given model coeficients in a dictionary.
    """
    coef_dict = {}
    for coef, feat in zip(model.coef_,X.columns):
        coef_dict[feat] = coef
    return coef_dict