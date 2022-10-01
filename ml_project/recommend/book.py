import numpy as np
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

books = pd.read_csv('Books.csv')
users = pd.read_csv('Users.csv')
ratings = pd.read_csv('Ratings.csv')
######## Popularity Based Recommender System
ratings_with_name = ratings.merge(books,on='ISBN')
total_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
total_rating_df.rename(columns={'Book-Rating':'num_ratings'},inplace=True)
avg_df_rating = ratings_with_name.groupby('Book-Title').mean()['Book-Rating'].reset_index()
avg_df_rating.rename(columns={'Book-Rating':'avg_rating'},inplace=True)
popular_data = total_rating_df.merge(avg_df_rating,on='Book-Title')
popular_data = popular_data[popular_data['num_ratings']>=150].sort_values('avg_rating',ascending=False)
popular_data = popular_data.merge(books,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Image-URL-M','num_ratings','avg_rating']]
    
######## Collaborative Filtering Based Recommender System
x = ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 150
padhe_likhe_users = x[x].index
filtered_rating = ratings_with_name[ratings_with_name['User-ID'].isin(padhe_likhe_users)]
y = filtered_rating.groupby('Book-Title').count()['Book-Rating']>=40
famous_books = y[y].index
final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]
popular_books = final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')
popular_books.fillna(0,inplace=True)
similarity_scores = cosine_similarity(popular_books)
similarity_scores.shape
def recommend(book_name):
    index = np.where(popular_books.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:10]
    main_data = []
    for i in similar_items:
        temp_list = []
        temp_data_df = books[books['Book-Title'] == popular_books.index[i[0]]]
        temp_list.extend(list(temp_data_df.drop_duplicates('Book-Title')['Book-Title'].values))
        temp_list.extend(list(temp_data_df.drop_duplicates('Book-Title')['Book-Author'].values))
        temp_list.extend(list(temp_data_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        main_data.append(temp_list)
    return main_data
pickle.dump(popular_data,open('popular_books.pkl','wb'))
books.drop_duplicates('Book-Title')
pickle.dump(,open('fiilter_books.pkl','wb'))
pickle.dump(all_books,open('books.pkl','wb'))
pickle.dump(similarity_scores,open('similarity_scores.pkl','wb'))