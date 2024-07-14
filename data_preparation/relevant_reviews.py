import pandas as pd


book_details = pd.read_csv('processed_data/books_details.csv')

book_details = book_details.drop_duplicates(subset=['text'], keep='first')

book_details = book_details[book_details['profileName'].notna() & book_details['authors'].notna()]

sentiment_threshold_high = book_details['sentiment'].quantile(0.90)
sentiment_threshold_low = book_details['sentiment'].quantile(0.10)


def classify_sentiment(sentiment):
    if sentiment >= sentiment_threshold_high:
        return 'positive'
    elif sentiment <= sentiment_threshold_low:
        return 'negative'
    else:
        return 'neutral'


book_details['sentiment_class'] = book_details['sentiment'].apply(classify_sentiment)

book_details = book_details[(book_details['sentiment_class'] != 'neutral') & (book_details['review'].str.len() >= 50)]


def get_relevant_reviews(group):
    top_reviews = group[group['sentiment_class'] == 'positive'].nlargest(5, 'sentiment')
    bottom_reviews = group[group['sentiment_class'] == 'negative'].nsmallest(5, 'sentiment')

    return pd.concat([top_reviews, bottom_reviews]).drop_duplicates(subset=['profileName', 'Title', 'summary', 'text'])


relevant_reviews = book_details.groupby('authors').apply(get_relevant_reviews).reset_index(drop=True)

relevant_reviews = relevant_reviews[['profileName', 'Title', 'summary', 'text', 'authors', 'sentiment_class']]

if not relevant_reviews.empty:
    relevant_reviews.to_csv('processed_data/relevant_reviews_per_author.csv', index=False)
