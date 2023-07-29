import streamlit as st
import pandas as pd

st.set_page_config(page_title="Book Recommendation System", page_icon="📚", layout="wide")

@st.cache_data()
def load_data():
    return pd.read_csv("./goodreads/books_clean.csv")


goodreads = load_data()

st.write("## 1. Simple Recommender System ")
user_ip_sim_criteria = st.radio("Select Similarity Criteria", ("authors", "publisher"))
user_ip_book_title = st.text_input("Enter the value for similarity criteria", 'Poor People')
user_ip_num_recommendations = st.slider("Select the number of recommendations", 1, 20, 5)


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

similarity_criteria = user_ip_sim_criteria
text_freq = TfidfVectorizer(stop_words='english')
text_matrix = text_freq.fit_transform(goodreads[similarity_criteria])

cosine_sim = linear_kernel(text_matrix, text_matrix)

# Build a 1-dimensional array with book titles
titles = goodreads['title']
indices = pd.Series(goodreads.index, index=goodreads['title'])

def get_closest_bookname(book_title:str, df:pd.DataFrame):
       """
       book_title: the book name to query
       df: the dataset to query
       """
       # if the book name is not in the dataset, return the closest book name
       if book_title not in df['title'].values:
              # check if the book_title is a substring of any book name              
              book_title = df[df['title'].apply(lambda x: x.lower()).str.contains(book_title.lower())]['title'].values
              if len(book_title) == 0:
                     return None
              else:
                     return book_title[0]
       else:
              return book_title
       
# Function that get book recommendations based on the cosine similarity score of book authors
def recommendations(title):
    title = get_closest_bookname(title, goodreads)

    if title is None:
        return pd.DataFrame()
    print(title)
    idx = indices[title]

    st.write("#### Selected Book:")
    st.dataframe(goodreads[goodreads['title'] == title])

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    st.write("#### Recommended Books:")
    return goodreads.iloc[book_indices]
st.write(recommendations(user_ip_book_title).head(user_ip_num_recommendations))