import csv
import pandas as pd
import numpy as np
import math
from math import sqrt
import pickle
from dataSet_testRecommend import dataset

debug_mode = True
load_existing_w_matrix = False

if debug_mode == True:
	DEFAULT_PARTICLE_PATH = 'w_matrix_debug.pkl'
else:
	DEFAULT_PARTICLE_PATH = 'w_matrix.pkl'

ratings = pd.read_csv("newratings.csv", encoding='"ISO-8859-1"')

if debug_mode == True:
	ratings = ratings[(ratings['Cos_id'] < 100) & (ratings['User_id'] < 100)]

def define_dataset():
	dataset = {}
	rinputFile = open('newratings.csv','r',encoding='"UTF-8')
	rFile = csv.reader(rinputFile)

	for i,line in enumerate(rFile):
		if(i is not 0):
			if(line[0] not in dataset):
				dataset[line[0]] = {line[1]:float(line[2])}
			else:
				dicItem = dict(dataset.get(line[0]))
				dicItem[line[1]] = float(line[2])
				dataset[line[0]] = dicItem

	rinputFile.close()
	return dataset

def pearson_correlation(person1,person2):

	# To get both rated items
	both_rated = {}
	for item in dataset[person1]:
		if item in dataset[person2]:
			both_rated[item] = 1
			
	number_of_ratings = len(both_rated)
	
	# Checking for number of ratings in common
	if number_of_ratings == 0:
		return 0

	# Add up all the preferences of each user
	person1_preferences_sum = sum([dataset[person1][item] for item in both_rated])
	person2_preferences_sum = sum([dataset[person2][item] for item in both_rated])

	# Sum up the squares of preferences of each user
	person1_square_preferences_sum = sum([pow(dataset[person1][item],2) for item in both_rated])
	person2_square_preferences_sum = sum([pow(dataset[person2][item],2) for item in both_rated])

	# Sum up the product value of both preferences for each item
	product_sum_of_both_users = sum([dataset[person1][item] * dataset[person2][item] for item in both_rated])

	# Calculate the pearson score
	numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/number_of_ratings)
	denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum,2)/number_of_ratings) * (person2_square_preferences_sum -pow(person2_preferences_sum,2)/number_of_ratings))
	if denominator_value == 0:
		return 0
	else:
		r = numerator_value/denominator_value
		return r 

def most_similar_users(person,number_of_users):
	# returns the number_of_users (similar persons) for a given specific person.
	person = str(person)
	scores = [(pearson_correlation(person,other_person),other_person) for other_person in dataset if  other_person != person ]
	
	# Sort the similar persons so that highest scores person will appear at the first
	scores.sort()
	scores.reverse()
	user_list = []
	
	for item in scores:
		user_list.append(int(item[1]))
	return user_list[0:number_of_users]

ratings_training = ratings.sample(frac=0.7)
ratings_test = ratings.drop(ratings_training.index)

# calculate adjusted ratings based on training data
rating_mean = ratings_training.groupby(['Cos_id'], as_index = False, sort = False).mean().rename(columns = {'rating': 'rating_mean'})[['Cos_id','rating_mean']]
adjusted_ratings = pd.merge(ratings_training,rating_mean,on = 'Cos_id', how = 'left', sort = False)
adjusted_ratings['rating_adjusted']=adjusted_ratings['rating']-adjusted_ratings['rating_mean']
# replace 0 adjusted rating values to 1*e-8 in order to avoid 0 denominator
adjusted_ratings.loc[adjusted_ratings['rating_adjusted'] == 0, 'rating_adjusted'] = 1e-8

# function of building the item-to-item weight matrix
def build_w_matrix(adjusted_ratings, load_existing_w_matrix):
	# define weight matrix
	w_matrix_columns = ['Cos_1', 'Cos_2', 'weight']
	w_matrix=pd.DataFrame(columns=w_matrix_columns)

	# load weight matrix from pickle file
	if load_existing_w_matrix:
		with open(DEFAULT_PARTICLE_PATH, 'rb') as input:
			w_matrix = pickle.load(input)
		input.close()

	# calculate the similarity values
	else:
		distinct_cosmetics = np.unique(adjusted_ratings['Cos_id'])

		i = 0
		# for each Cos_1 in all cosmetics
		for Cos_1 in distinct_cosmetics:

			if i%10==0:
				print(i , "out of ", len(distinct_cosmetics))

			# extract all users who rated Cos_1
			user_data = adjusted_ratings[adjusted_ratings['Cos_id'] == Cos_1]
			distinct_users = np.unique(user_data['User_id'])
			distinct_users = list(set(distinct_users).intersection(similar_user_list))
			
			# record the ratings for users who rated both Cos_1 and Cos_2
			record_row_columns = ['User_id', 'Cos_1', 'Cos_2', 'rating_adjusted_1', 'rating_adjusted_2']
			record_Cos_1_2 = pd.DataFrame(columns=record_row_columns)
			# for each customer C who rated Cos_1
			for c_userid in distinct_users:
				print('build weight matrix for customer %d, Cos_1 %d' % (c_userid, Cos_1))
				# the customer's rating for Cos_1
				c_Cos_1_rating = user_data[user_data['User_id'] == c_userid]['rating_adjusted'].iloc[0]
				# extract cosmetics rated by the customer excluding Cos_1
				c_user_data = adjusted_ratings[(adjusted_ratings['User_id'] == c_userid) & (adjusted_ratings['Cos_id'] != Cos_1)]
				c_distinct_cosmetics = np.unique(c_user_data['Cos_id'])

				# for each Cos rated by customer C as Cos=2
				for Cos_2 in c_distinct_cosmetics:
					# the customer's rating for Cos_2
					c_Cos_2_rating = c_user_data[c_user_data['Cos_id'] == Cos_2]['rating_adjusted'].iloc[0]
					record_row = pd.Series([c_userid, Cos_1, Cos_2, c_Cos_1_rating, c_Cos_2_rating], index=record_row_columns)
					record_Cos_1_2 = record_Cos_1_2.append(record_row, ignore_index=True)

			# calculate the similarity values between Cos_1 and the above recorded cosmetics
			distinct_Cos_2 = np.unique(record_Cos_1_2['Cos_2'])
			# for each Cos 2
			for Cos_2 in distinct_Cos_2:
				print('calculate weight Cos_1 %d, Cos_2 %d' % (Cos_1, Cos_2))
				paired_Cos_1_2 = record_Cos_1_2[record_Cos_1_2['Cos_2'] == Cos_2]
				sim_value_numerator = (paired_Cos_1_2['rating_adjusted_1'] * paired_Cos_1_2['rating_adjusted_2']).sum()
				sim_value_denominator = np.sqrt(np.square(paired_Cos_1_2['rating_adjusted_1']).sum()) * np.sqrt(np.square(paired_Cos_1_2['rating_adjusted_2']).sum())
				sim_value_denominator = sim_value_denominator if sim_value_denominator != 0 else 1e-8
				sim_value = sim_value_numerator / sim_value_denominator
				w_matrix = w_matrix.append(pd.Series([Cos_1, Cos_2, sim_value], index=w_matrix_columns), ignore_index=True)
			
		i = i + 1

		# output weight matrix to pickle file
		with open(DEFAULT_PARTICLE_PATH, 'wb') as output:
			pickle.dump(w_matrix, output, pickle.HIGHEST_PROTOCOL)
		output.close()

	return w_matrix

dataset = define_dataset()
similar_user_list = most_similar_users(2,20)

# run the function to build similarity matrix
w_matrix = build_w_matrix(adjusted_ratings, load_existing_w_matrix)

# calculate the predicted ratings
def predict(User_id, Cos_id, w_matrix, adjusted_ratings, rating_mean):
	# fix missing mean rating which was caused by no ratings for the given Cos
	# mean_rating exists for Cos_id
	if rating_mean[rating_mean['Cos_id'] == Cos_id].shape[0] > 0:
		mean_rating = rating_mean[rating_mean['Cos_id'] == Cos_id]['rating_mean'].iloc[0]
	# mean_rating does not exist for Cos_id(which may be caused by no ratings for the Cos)
	else:
		mean_rating = 2.5

	# calculate the rating of the given Cos by the given user
	user_other_ratings = adjusted_ratings[adjusted_ratings['User_id'] == User_id]
	user_distinct_cosmetics = np.unique(user_other_ratings['Cos_id'])
	sum_weighted_other_ratings = 0
	sum_weghts = 0
	for Cos_j in user_distinct_cosmetics:
		if rating_mean[rating_mean['Cos_id'] == Cos_j].shape[0] > 0:
			rating_mean_j = rating_mean[rating_mean['Cos_id'] == Cos_j]['rating_mean'].iloc[0]
		else:
			rating_mean_j = 2.5
		# only calculate the weighted values when the weight between Cos_1 and Cos_2 exists in weight matrix
		w_Cos_1_2 = w_matrix[(w_matrix['Cos_1'] == Cos_id) & (w_matrix['Cos_2'] == Cos_j)]
		if w_Cos_1_2.shape[0] > 0:
			user_rating_j = user_other_ratings[user_other_ratings['Cos_id']==Cos_j]
			sum_weighted_other_ratings += (user_rating_j['rating'].iloc[0] - rating_mean_j) * w_Cos_1_2['weight'].iloc[0]
			sum_weghts += np.abs(w_Cos_1_2['weight'].iloc[0])

	# if sum_weights is 0 (which may be because of no ratings from new users), use the mean ratings
	if sum_weghts == 0:
		predicted_rating = mean_rating
	# sum_weights is bigger than 0
	else:
		predicted_rating = mean_rating + sum_weighted_other_ratings/sum_weghts

	return predicted_rating

# evaluate the learned recommender system on test data by converting the ratings to negative and positive
def binary_eval(ratings_test, w_matrix, adjusted_ratings, rating_mean):
	# predict all the ratings for test data
	ratings_test = ratings_test.assign(predicted_rating = pd.Series(np.zeros(ratings_test.shape[0])))
	for index, row_rating in ratings_test.iterrows():
		predicted_rating = predict(row_rating['User_id'], row_rating['Cos_id'], w_matrix, adjusted_ratings, rating_mean)
		ratings_test.loc[index, 'predicted_rating'] = predicted_rating
	tp = ratings_test.query('(rating >= 2.5) & (predicted_rating >= 2.5)').shape[0]
	fp = ratings_test.query('(rating < 2.5) & (predicted_rating >= 2.5)').shape[0]
	fn = ratings_test.query('(rating >= 2.5) & (predicted_rating < 2.5)').shape[0]

	# calculate the precision and recall
	precision = tp/(tp+fp)
	recall = tp/(tp+fn)
	return (precision, recall)

# run the evaluation
eval_result = binary_eval(ratings_test, w_matrix, adjusted_ratings, rating_mean)
print('Evaluation result - precision: %f, recall: %f' % eval_result)

# make recommendations
def recommend(userID, w_matrix, adjusted_ratings, rating_mean, amount=10):
	distinct_cosmetics = np.unique(adjusted_ratings['Cos_id'])
	user_ratings_all_cosmetics = pd.DataFrame(columns=['Cos_id', 'rating'])
	user_rating = adjusted_ratings[adjusted_ratings['User_id']==userID]

	# calculate the ratings for all cosmetics that the user hasn't rated
	i = 0
	for Cos in distinct_cosmetics:
		user_rating = user_rating[user_rating['Cos_id']==Cos]
		if user_rating.shape[0] > 0:
			rating_value = user_ratings_all_cosmetics.loc[i, 'rating'] = user_rating.loc[0, Cos]
		else:
			rating_value = user_ratings_all_cosmetics.loc[i, 'rating'] = predict(userID, Cos, w_matrix, adjusted_ratings, rating_mean)
		user_ratings_all_cosmetics.loc[i] = [Cos, rating_value]

		i = i + 1

	# select top 10 cosmetics rated by the user
	recommendations = user_ratings_all_cosmetics.sort_values(by=['rating'], ascending=False).head(amount)
	return recommendations

# get a recommendation list for a given user

recommended_cosmetics = recommend(2, w_matrix, adjusted_ratings, rating_mean)
print(recommended_cosmetics)





