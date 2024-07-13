import pandas as pd
import streamlit as st


author_sentiment = pd.read_csv('data_preparation/author_sentiment.csv')
sorted_authors = author_sentiment.sort_values(by='Number_of_Reviews', ascending=False)


st.title('Author Sentiment Analysis')

author_list = sorted_authors['authors'].tolist()
selected_author = st.selectbox('Select an author:', author_list)

if selected_author:
    avg_sentiment = sorted_authors[sorted_authors['authors'] == selected_author]['Average_Sentiment'].values[0]
    num_reviews = sorted_authors[sorted_authors['authors'] == selected_author]['Number_of_Reviews'].values[0]
    st.write(f'The average sentiment for author **{selected_author}** is **{avg_sentiment:.2f}**, '
             f'based on **{num_reviews}** reviews.')
