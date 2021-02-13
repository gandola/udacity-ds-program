import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def tokenize(text):
    """
    Tokenizes the given text applying the following transformations:
    - Clean non-alphanumeric chars
    - All chars are lowered
    - All words are trimmed
    - Lemmatizing
    @param text to be tokenized.
    """
    # remove all non-alphanumeric data.
    text = re.sub('[\\W_]+', ' ', text)

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok.lower().strip())
        clean_tokens.append(clean_tok)

    return clean_tokens
