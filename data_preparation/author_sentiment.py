import pandas as pd
import ast
from textblob import TextBlob
from tqdm import tqdm


book_data = pd.read_csv('../data/books_data.csv')
book_rating = pd.read_csv('../data/Books_rating.csv')

book_data['authors'] = book_data['authors'].fillna('[]')
book_data['authors'] = book_data['authors'].apply(ast.literal_eval)
merged_data = pd.merge(book_rating, book_data[['Title', 'authors']], on='Title', how='left')


def concatenate_reviews(row):
    return (row['summary'] if pd.notna(row['summary']) else '') + ' ' + (row['text'] if pd.notna(row['text']) else '')


tqdm.pandas(desc="Concatenating reviews")
merged_data['review'] = merged_data.progress_apply(concatenate_reviews, axis=1)


def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


tqdm.pandas(desc="Calculating sentiment")
merged_data['sentiment'] = merged_data['review'].progress_apply(get_sentiment)

merged_data = merged_data.explode('authors')

author_sentiment = merged_data.groupby('authors').agg(
    Average_Sentiment=('sentiment', 'mean'),
    Number_of_Reviews=('sentiment', 'size')
).reset_index()


author_sentiment.to_csv('author_sentiment.csv', index=False)

merged_data.to_csv('books_details.csv', index=False)

