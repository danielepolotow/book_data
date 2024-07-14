import pandas as pd


book_details = pd.read_csv('processed_data/books_details.csv')

book_details = book_details.drop_duplicates(subset=['text'], keep='first')

book_details = book_details.dropna(subset=['User_id', 'profileName'])

sentiment_threshold_high = book_details['sentiment'].quantile(0.90)
sentiment_threshold_low = book_details['sentiment'].quantile(0.10)

book_details = book_details[book_details['text'].str.split().str.len() >= 100]


def classify_sentiment(sentiment):
    if sentiment >= sentiment_threshold_high:
        return 'high'
    elif sentiment <= sentiment_threshold_low:
        return 'low'
    else:
        return 'neutral'


book_details['sentiment_class'] = book_details['sentiment'].apply(classify_sentiment)

relevant_reviews = book_details[book_details['sentiment_class'] != 'neutral']

user_activity = relevant_reviews.groupby('User_id').size().reset_index(name='number_of_reviews')

active_users = user_activity[user_activity['number_of_reviews'] >= 10]

final_relevant_reviews = relevant_reviews.merge(active_users, on='User_id')

final_relevant_reviews = final_relevant_reviews.sort_values(by='number_of_reviews', ascending=False)

output_columns = ['User_id', 'profileName', 'number_of_reviews', 'Title', 'authors', 'summary', 'text', 'sentiment_class']
final_relevant_reviews = final_relevant_reviews[output_columns]

if not final_relevant_reviews.empty:
    final_relevant_reviews.to_csv('processed_data/relevant_user_reviews.csv', index=False)

