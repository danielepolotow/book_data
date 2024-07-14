import pandas as pd


book_details = pd.read_csv('books_details.csv')

book_details = book_details.drop_duplicates(subset=['text'], keep='first')
book_details = book_details[book_details['profileName'].notna() & book_details['authors'].notna()]

quantiles = book_details['sentiment'].quantile([0.2, 0.4, 0.6, 0.8])


def classify_sentiment(sentiment):
    if sentiment <= quantiles[0.2]:
        return 'very bad'
    elif sentiment <= quantiles[0.4]:
        return 'bad'
    elif sentiment <= quantiles[0.6]:
        return 'neutral'
    elif sentiment <= quantiles[0.8]:
        return 'good'
    else:
        return 'very good'


book_details['sentiment_class'] = book_details['sentiment'].apply(classify_sentiment)

book_details = book_details[book_details['review'].str.len() >= 50]


def normalize_authors(authors):
    if isinstance(authors, list):
        return ', '.join(authors)  # This joins list entries with commas
    return authors


book_details['authors'] = book_details['authors'].apply(normalize_authors)


def calculate_percentage(group):
    total = len(group)
    percentages = group['sentiment_class'].value_counts(normalize=True) * 100
    return pd.Series({
        'very bad': percentages.get('very bad', 0),
        'bad': percentages.get('bad', 0),
        'neutral': percentages.get('neutral', 0),
        'good': percentages.get('good', 0),
        'very good': percentages.get('very good', 0)
    })


author_sentiment_distribution = book_details.groupby('authors').apply(calculate_percentage).reset_index()

author_sentiment_distribution.to_csv('author_sentiment_distribution.csv', index=False)
