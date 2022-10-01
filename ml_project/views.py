from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.contrib import messages
import numpy as np
import pickle

popular_books=pickle.load(open('C:/Users/ashis/OneDrive/Desktop/new_scrap/book_recommendation_system/ml_project/recommend/popular_books.pkl','rb'))
filter_books=pickle.load(open('C:/Users/ashis/OneDrive/Desktop/new_scrap/book_recommendation_system/ml_project/recommend/filter_books.pkl','rb'))
all_books=pickle.load(open('C:/Users/ashis/OneDrive/Desktop/new_scrap/book_recommendation_system/ml_project/recommend/all_books.pkl','rb'))
similarity_scores=pickle.load(open('C:/Users/ashis/OneDrive/Desktop/new_scrap/book_recommendation_system/ml_project/recommend/similarity_scores.pkl','rb'))
popular_books=popular_books[0:40]

def index( request):
	books = []
	titles 			= popular_books['Book-Title'].values.tolist()
	authors 		= popular_books['Book-Author'].values.tolist()
	images 			= popular_books['Image-URL-M'].values.tolist()
	total_ratings 	= popular_books['num_ratings'].values.tolist()
	avg_ratings 	= popular_books['avg_rating'].values.tolist()
	for i in range(0,len(popular_books)):
		temp_dict = {
			'title': titles[i],
			'author': authors[i],
			'image': images[i],
			'total_rating': total_ratings[i],
			'avg_rating': round(avg_ratings[i],2),
		}
		books.append(temp_dict)
		temp_dict = {}
	return render(request, 'ml_project/index.html', {'context':books})

def search(request):
	return render(request, 'ml_project/search.html')

def recommend_data(request):
	if request.method == 'POST':
		user_input = request.POST.get('user_input', False)
		index = np.where(filter_books.index==user_input)[0][0]
		similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:9]
		output = []
		for i in similar_items:
			item = []
			temp_df = all_books[all_books['Book-Title'] == filter_books.index[i[0]]]
			item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
			item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
			item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
			output.append(item)
			item=[]
	main_data=[]
	for i in range(0,len(output)):
		temp_dict = {
			'title': output[i][0],
			'author': output[i][1],
			'image': output[i][2]
		}
		main_data.append(temp_dict)
		temp_dict = {}
	return render(request, 'ml_project/search.html', {'main_data':main_data})