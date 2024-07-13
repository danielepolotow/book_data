import pandas as pd
import streamlit as st


def sentiment_to_stars(sentiment):
    # Normalize sentiment from -1 to 1 into a 0 to 5 scale
    stars = (sentiment + 1) * 2.5
    return round(stars)


def display_stars(stars):
    full_stars = int(stars)
    half_star = 1 if stars - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    stars_str = '★' * full_stars + '☆' * empty_stars
    if half_star:
        stars_str = stars_str[:-1] + '⭒' + '☆' * (empty_stars - 1)
    return stars_str


author_sentiment = pd.read_csv('data_preparation/author_sentiment.csv')
sorted_authors = author_sentiment.sort_values(by='Number_of_Reviews', ascending=False)


st.title('Author Sentiment Analysis')

author_list = ['Choose an author'] + sorted_authors['authors'].tolist()
selected_author = st.selectbox('Select an author:', author_list)

if selected_author != 'Choose an author':
    avg_sentiment = sorted_authors[sorted_authors['authors'] == selected_author]['Average_Sentiment'].values[0]
    num_reviews = sorted_authors[sorted_authors['authors'] == selected_author]['Number_of_Reviews'].values[0]

    # Convert sentiment to stars
    stars = sentiment_to_stars(avg_sentiment)
    star_visual = display_stars(stars)

    # Display stars
    st.markdown(f"### {star_visual}")
    st.write(
        f'The average sentiment for author **{selected_author}** is **{avg_sentiment:.2f}**, based on **{num_reviews}** reviews.')

