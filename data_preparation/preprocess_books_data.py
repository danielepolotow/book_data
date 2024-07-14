import pandas as pd


def preprocess_books_data(file_path):
    books_data = pd.read_csv(file_path)

    books_data['authors'] = books_data['authors'].apply(
        lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else [x])

    books_data_exploded = books_data.explode('authors')

    books_data_exploded.to_csv('processed_data/preprocessed_books_data.csv', index=False)


preprocess_books_data('../original_data/books_data.csv')

