import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def vectorize(text):
    df_main = pd.read_csv('df_main.csv')
    X_train = df_main['clean_text']
    cv = CountVectorizer(ngram_range=(1, 6), max_df=1.0, min_df=5)
    cv_train_features = cv.fit_transform(X_train)
    vectorized_text = cv.transform(text)
    return vectorized_text

