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