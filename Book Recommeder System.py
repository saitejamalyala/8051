import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Book Recommendation System", page_icon="📚", layout="wide")

st.write("## Feature Based Recommender System")

@st.cache_data
def load_data():
    return pd.read_csv("./books_clean.csv")

goodreads = load_data()


# catrgorical data columns: authors, language_code, publisher
# numerical data columns: average_rating, num_pages, ratings_count, text_reviews_count, years_since_publication

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler
import pickle

numerical_columns = ['average_rating', 'num_pages', 'ratings_count', 'text_reviews_count', 'years_since_publication']
categorical_columns = ['authors', 'language_code', 'publisher']
# calculate similarity between all books
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
features = ['average_rating', 'num_pages', 'ratings_count', 'text_reviews_count', 'years_since_publication']


# encoding categorical data
def encode_data(df:pd.DataFrame) -> pd.DataFrame:
       """ 
       This function encodes the categorical data in the dataframe.
       """
       # encoding authors column
       encoder = OrdinalEncoder()
       df[categorical_columns] = encoder.fit_transform(df[categorical_columns])

       # save the encoder
       with open('encoder.pkl', 'wb') as f:
              pickle.dump(encoder, f)
            
       return df

# scaling numerical data
def scale_data(df:pd.DataFrame) -> pd.DataFrame:
       """
       This function scales the numerical data in the dataframe.
       """

       scaler = MinMaxScaler()
       numerical_columns = ['average_rating', 'num_pages', 'ratings_count', 'text_reviews_count', 'years_since_publication']
       df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

       # save the scaler
       with open('scaler.pkl', 'wb') as f:
              pickle.dump(scaler, f)

       return df

@st.cache_data
def preprocess_data(df:pd.DataFrame) -> pd.DataFrame:
       df = encode_data(df)
       df = scale_data(df)
       return df

def get_original_data(df):
       """
       This function returns the original data from the scaled and encoded data.
       """
       # load the encoder
       with open('encoder.pkl', 'rb') as f:
              encoder = pickle.load(f)
       # load the scaler
       with open('scaler.pkl', 'rb') as f:
              scaler = pickle.load(f)
       # get the original data
       df[categorical_columns] = encoder.inverse_transform(df[categorical_columns])
       df[numerical_columns] = scaler.inverse_transform(df[numerical_columns])
       return df

@st.cache_data
def get_similarity_matrix(df:pd.DataFrame) -> pd.DataFrame:
       """
       Calculate similarity between all books in the dataset
       :param df: dataframe containing all books
       """
       # calculate similairity for each book
       #similarity_matrix = np.zeros((df.shape[0], df.shape[0]))
       features = df[['average_rating', 'num_pages', 'ratings_count', 'text_reviews_count', 'years_since_publication',]]# 'authors', 'language_code', 'publisher']]
       similarity_matrix = cosine_similarity(features)
       similarity_df = pd.DataFrame(similarity_matrix, index=df['bookID'].values, columns=df['bookID'].values)
       return similarity_df

pre_process_df = preprocess_data(goodreads)
similarity_df = get_similarity_matrix(pre_process_df)


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
       

def get_feature_based_rec(book_title:str, similarity_df:pd.DataFrame, goodreads:pd.DataFrame, n:int=10) -> pd.DataFrame:
       """
       book_title: the book name to query
       similarity_df: the similarity matrix
       goodreads: the goodreads dataset
       n: number of recommendations
       """

       book_title = get_closest_bookname(book_title, goodreads.copy(deep=True))
       st.write(f'Query Book Title:')

       book_id = goodreads[goodreads['title']==book_title]['bookID'].values[0]
       st.dataframe(goodreads[goodreads['bookID']==book_id])

       st.write("#### Recommended Books:")
       similar_books = similarity_df[book_id].sort_values(ascending=False)[1:n+1]
       similar_books = pd.DataFrame(similar_books).reset_index()
       similar_books.columns = ['bookID', 'similarity_score']
       similar_books = pd.merge(similar_books, goodreads, on='bookID', how='left')
       return similar_books

user_ip_book_title = st.text_input("Enter the book title", 'Daughter of Fortune')
user_ip_num_recommendations = st.slider("Select the number of recommendations", 1, 20, 5)


st.dataframe(get_feature_based_rec('Daughter of Fortune', similarity_df, goodreads, 10))
