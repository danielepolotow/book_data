import pandas as pd
import streamlit as st
from utils.sentiment_to_stars import sentiment_to_stars, display_stars


author_sentiment = pd.read_csv('data_preparation/author_sentiment.csv')
books_data = pd.read_csv('data_preparation/preprocessed_books_data.csv')
reviews_data = pd.read_csv('data_preparation/relevant_reviews_per_author.csv')

sorted_authors = author_sentiment.sort_values(by='Number_of_Reviews', ascending=False)


st.title('Author Sentiment Analysis')

author_list = ['Choose an author'] + sorted_authors['authors'].tolist()
selected_author = st.selectbox('Select an author:', author_list)

if selected_author != 'Choose an author':
    avg_sentiment = sorted_authors[sorted_authors['authors'] == selected_author]['Average_Sentiment'].values[0]
    num_reviews = sorted_authors[sorted_authors['authors'] == selected_author]['Number_of_Reviews'].values[0]

    stars = sentiment_to_stars(avg_sentiment)
    star_visual = display_stars(stars)

    st.markdown(f"### {star_visual}")
    st.markdown(f"""
    <div style='font-size: 20px;'>
        The average sentiment for author <b>{selected_author}</b> is <b>{avg_sentiment:.2f}</b>, based on <b>{num_reviews}</b> reviews.
    </div>
    """, unsafe_allow_html=True)

    author_reviews = reviews_data[reviews_data['authors'] == selected_author]
    positive_reviews = author_reviews[author_reviews['sentiment_class'] == 'positive']
    negative_reviews = author_reviews[author_reviews['sentiment_class'] == 'negative']

    if not positive_reviews.empty:
        with st.expander("Positive Reviews"):
            for index, review in positive_reviews.iterrows():
                st.write(f"**{review['profileName']}** wrote:")
                st.write(f"**Summary:** {review['summary']}")
                st.write(f"**Review:** {review['text']}")
    else:
        st.warning("No relevant positive reviews for this author.")

    if not negative_reviews.empty:
        with st.expander("Negative Reviews"):
            for index, review in negative_reviews.iterrows():
                st.write(f"**{review['profileName']}** wrote:")
                st.write(f"**Summary:** {review['summary']}")
                st.write(f"**Review:** {review['text']}")
    else:
        st.warning("No relevant negative reviews for this author.")

    author_books = books_data[books_data['authors'] == selected_author]
    author_books = author_books.dropna(subset=['image', 'infoLink'])
    author_books = author_books[author_books['image'].apply(lambda x: isinstance(x, str) and x.strip() != '')]
    author_books = author_books[author_books['infoLink'].apply(lambda x: isinstance(x, str) and x.strip() != '')]

    if not author_books.empty:
        st.write("### Books by this author:")
        author_books = author_books.head(9)
        columns = 3
        for index in range(0, len(author_books), columns):
            cols = st.columns(columns)
            for col, (_, row) in zip(cols, author_books.iloc[index:index + columns].iterrows()):
                col.image(row['image'], width=100)
                col.markdown(
                    f"[More about this book]({row['infoLink']})")
    else:
        st.write("No books found for this author.")

