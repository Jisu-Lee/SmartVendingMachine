import csv
import pandas as pd
import numpy as np
import math
from math import sqrt
import pickle

DEFAULT_PARTICLE_PATH = 'w_matrix.pkl'

def pearson_correlation(person1,person2, dataset):
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

# use pearson_correlation for find n-most similar user
def most_similar_users(person,number_of_users, dataset):
	# returns the number_of_users (similar persons) for a given specific person.
	scores = [(pearson_correlation(person,other_person, dataset),other_person) for other_person in dataset if  other_person != person ]
	
	# Sort the similar persons so that highest scores person will appear at the first
	scores.sort()
	scores.reverse()
	user_list = []
	for item in scores:
		user_list.append(int(item[1]))
	return user_list[0:number_of_users]

def build_w_matrix(adjusted_ratings):
	# define weight matrix
	w_matrix_columns = ['Cos_1', 'Cos_2', 'weight']
	w_matrix=pd.DataFrame(columns=w_matrix_columns)

	distinct_cosmetics = np.unique(adjusted_ratings['Cos_id'])

	i = 0
	# for each Cos_1 in all cosmetics
	for Cos_1 in distinct_cosmetics:
		# extract all users who rated Cos_1
		user_data = adjusted_ratings[adjusted_ratings['Cos_id'] == Cos_1]
		distinct_users = np.unique(user_data['User_id'])
		
		# record the ratings for users who rated both Cos_1 and Cos_2
		record_row_columns = ['User_id', 'Cos_1', 'Cos_2', 'rating_adjusted_1', 'rating_adjusted_2']
		record_Cos_1_2 = pd.DataFrame(columns=record_row_columns)
		# for each customer C who rated Cos_1
		for c_userid in distinct_users:
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
			paired_Cos_1_2 = record_Cos_1_2[record_Cos_1_2['Cos_2'] == Cos_2]
			sim_value_numerator = (paired_Cos_1_2['rating_adjusted_1'] * paired_Cos_1_2['rating_adjusted_2']).sum()
			sim_value_denominator = np.sqrt(np.square(paired_Cos_1_2['rating_adjusted_1']).sum()) * np.sqrt(np.square(paired_Cos_1_2['rating_adjusted_2']).sum())
			sim_value_denominator = sim_value_denominator if sim_value_denominator != 0 else 1e-8
			sim_value = sim_value_numerator / sim_value_denominator
			w_matrix = w_matrix.append(pd.Series([Cos_1, Cos_2, sim_value], index=w_matrix_columns), ignore_index=True)
		
	i = i + 1

	return w_matrix

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

# make recommendations with content-based
def recommendCB(userID, w_matrix, adjusted_ratings, rating_mean, amount=10):
	distinct_cosmetics = np.unique(adjusted_ratings['Cos_id'])
	user_ratings_all_cosmetics = pd.DataFrame(columns=['Cos_id', 'rating'])
	user_rating = adjusted_ratings[adjusted_ratings['User_id']==userID]
	
	# calculate the ratings for all cosmetics that the user hasn't rated
	i = 0
	for Cos in distinct_cosmetics:
		user_rating = user_rating[user_rating['Cos_id']==Cos]
		if user_rating.shape[0] > 0:
			rating_value = user_ratings_all_cosmetics.loc[i, 'rating'] = float(user_rating.iloc[0, Cos])
		else:
			rating_value = user_ratings_all_cosmetics.loc[i, 'rating'] = predict(userID, Cos, w_matrix, adjusted_ratings, rating_mean)
		user_ratings_all_cosmetics.loc[i] = [Cos, rating_value]

		i = i + 1

	# select top 10 cosmetics rated by the user
	recommendations = user_ratings_all_cosmetics.sort_values(by=['rating'], ascending=False).head(amount)
	return recommendations

def recommend_hybrid(user_id, similar_user_num, content_num, dataset):
	user_id = int(user_id)
	similar_user = most_similar_users(user_id, similar_user_num, dataset["ub_dataset"])
	print('\nmost similar user : ', similar_user)
	cb_dataset = dataset['cb_dataset']
	cb_dataset = cb_dataset[cb_dataset['User_id'].isin(similar_user)]
	ratings_training = cb_dataset.sample(frac=1.0)
	ratings_test = cb_dataset.drop(ratings_training.index)
	
	# calculate adjusted ratings based on training data
	rating_mean = ratings_training.groupby(['Cos_id'], as_index = False, sort = False).mean().rename(columns = {'rating': 'rating_mean'})[['Cos_id','rating_mean']]
	adjusted_ratings = pd.merge(ratings_training,rating_mean,on = 'Cos_id', how = 'left', sort = False)
	adjusted_ratings['rating_adjusted']=adjusted_ratings['rating']-adjusted_ratings['rating_mean']
	# replace 0 adjusted rating values to 1*e-8 in order to avoid 0 denominator
	adjusted_ratings.loc[adjusted_ratings['rating_adjusted'] == 0, 'rating_adjusted'] = 1e-8

	# run the function to build similarity matrix
	w_matrix = build_w_matrix(adjusted_ratings)

	# run the evaluation
	#eval_result = binary_eval(ratings_test, w_matrix, adjusted_ratings, rating_mean)
	#print('Evaluation result - precision: %f, recall: %f' % eval_result)

	# get a recommendation list for a given user
	recommended_cosmetics = recommendCB(2, w_matrix, adjusted_ratings, rating_mean)
	return recommended_cosmetics[0:content_num]

def change_id_to_name(cosmetic_name, cosmetic_cid, recommended_item):
	recommended_cid = recommended_item['Cos_id']

	recommended_name = []
	for cos_id in recommended_cid:
		recommended_name.append(cosmetic_name[cosmetic_cid.index(cos_id)])
	return recommended_name

def define_lisset(similarCos, similarUser, allRating):
	uid_list = []
	cid_list = []
	cname_list = []
	rating_uid_list = []
	rating_cid_list = []
	rating_score_list = []

	
	for i in range(len(similarUser)):
		uid_list.append(int(similarUser[i]["id"]))
	
	for i in range(len(similarCos)):
		cid_list.append(int(similarCos[i]["id"]))
		cname_list.append(similarCos[i]["name"])

	for i in range(len(allRating)):
		rating_uid_list.append(int(allRating[i]["user_id"]))
		rating_cid_list.append(int(allRating[i]["cosmetic_id"]))
		rating_score_list.append(float(allRating[i]["rating"]))

	dataset = {"uid_list" : uid_list,"cname_list" : cname_list, "cid_list" : cid_list, "rating_uid_list" : rating_uid_list, "rating_cid_list" : rating_cid_list, "rating_score_list" : rating_score_list}
	return dataset

def define_dataset(user_uid, cosmetic_cid, rating_uid, rating_cid, rating_score):
	ub_dataset = {}
	uid_list = []
	cid_list = []
	score_list = []
	print(user_uid)
	print(cosmetic_cid)
	k = 0
	for i in range(len(rating_uid)):
		if((rating_uid[i] in user_uid) and (rating_cid[i] in cosmetic_cid)):
			uid_list.append(rating_uid[i])
			cid_list.append(rating_cid[i])
			score_list.append(rating_score[i])
			k = k+1
			if(rating_uid[i] not in ub_dataset):
				ub_dataset[rating_uid[i]] = {rating_cid[i]:rating_score[i]}
			else:
				dicItem = dict(ub_dataset.get(rating_uid[i]))
				dicItem[rating_cid[i]] = rating_score[i]
				ub_dataset[rating_uid[i]] = dicItem

	cb_dataset = pd.DataFrame({'User_id' : uid_list, 'Cos_id' : cid_list, 'rating' : score_list})
	dataset = {'ub_dataset' : ub_dataset, 'cb_dataset' : cb_dataset}
	return dataset

def read_csv_and_make_list_dict_dataset(rating_file_name):
	name_list = []
	dataset = []
	rinputFile = open(rating_file_name,'r')
	rFile = csv.reader(rinputFile)
	
	for i,lines in enumerate(rFile):
		if i is 0:
			for line in lines:
				name_list.append(line)
		else:
			dic_item = {}
			for i,line in enumerate(lines):
				dic_item[name_list[i]] = line
			dataset.append(dic_item)
	
	rinputFile.close()
	return dataset

user_id = "1"
similar_user_num = 4
content_num = 3

#similarCos = [{"id": "109", "name": "test", "price": "76.2", "product_type": "SUNSCREEN", "rating": "4.9", "skintype": "dry"}, {"id": "110", "name": "Eye Paint Eye Shadow", "price": "76.2", "product_type": "SUNSCREEN", "rating": "4.9", "skintype": "dry"}, {"id": "102", "name": "Treatment Lip Shine", "price": "18.2", "product_type": "SUNSCREEN", "rating": "2", "skintype": "dry"}, {"id": "120", "name": "AMC Multicolour System Bronzing Powder", "price": "149.6", "product_type": "SUNSCREEN", "rating": "2.6", "skintype": "dry"}, {"id": "80", "name": "Natural Brow Shaper \u0026 hair Touch up", "price": "127.1", "product_type": "MOSITURIZER", "rating": "1.6", "skintype": "dry"}, {"id": "78", "name": "Metallic Long-Wear Cream Shadow", "price": "75.6", "product_type": "MOSITURIZER", "rating": "2.1", "skintype": "dry"}, {"id": "112", "name": "AMC Face Blush", "price": "144", "product_type": "SUNSCREEN", "rating": "2.1", "skintype": "dry"}, {"id": "82", "name": "Pot Rouge for Lips \u0026 Cheeks", "price": "121.7", "product_type": "MOSITURIZER", "rating": "2.8", "skintype": "dry"}, {"id": "63", "name": "Ink Eyeliner", "price": "106.9", "product_type": "MOSITURIZER", "rating": "1.5", "skintype": "dry"}, {"id": "75", "name": "Long-Wear Eye Pencil", "price": "12.6", "product_type": "MOSITURIZER", "rating": "1.8", "skintype": "dry"}, {"id": "106", "name": "Lip Palette", "price": "122.2", "product_type": "SUNSCREEN", "rating": "1.8", "skintype": "dry"}, {"id": "58", "name": "Hydrating Face Tonic", "price": "20", "product_type": "MOSITURIZER", "rating": "2.7", "skintype": "dry"}, {"id": "8", "name": "Nail File", "price": "91.3", "product_type": "CREAM", "rating": "3.2", "skintype": "dry"}, {"id": "7", "name": "Melt Away Cuticle Eliminator", "price": "14.6", "product_type": "CREAM", "rating": "2.2", "skintype": "dry"}, {"id": "40", "name": "EXTRA Repair Serum", "price": "22.1", "product_type": "CREAM", "rating": "1.9", "skintype": "dry"}, {"id": "70", "name": "Lip Color", "price": "97.5", "product_type": "MOSITURIZER", "rating": "2", "skintype": "dry"}, {"id": "93", "name": "Sheer Powder", "price": "90.1", "product_type": "SUNSCREEN", "rating": "1.1", "skintype": "dry"}, {"id": "95", "name": "Shimmer Brick", "price": "67", "product_type": "SUNSCREEN", "rating": "2.2", "skintype": "dry"}, {"id": "32", "name": "Creamy Matte Lip Color", "price": "38", "product_type": "CREAM", "rating": "2.1", "skintype": "dry"}, {"id": "84", "name": "Protective Face Lotion", "price": "138.3", "product_type": "MOSITURIZER", "rating": "2.5", "skintype": "dry"}, {"id": "81", "name": "No Smudge Mascara", "price": "76.5", "product_type": "MOSITURIZER", "rating": "3.6", "skintype": "dry"}, {"id": "39", "name": "EXTRA Repair Moisturizing Balm SPF 25", "price": "43.7", "product_type": "CREAM", "rating": "2.3", "skintype": "dry"}, {"id": "53", "name": "Foundation", "price": "142.2", "product_type": "MOSITURIZER", "rating": "1.8", "skintype": "dry"}, {"id": "104", "name": "Ultra Fine Eyeliner", "price": "145.7", "product_type": "SUNSCREEN", "rating": "2.6", "skintype": "dry"}, {"id": "109", "name": "Eye Paint Palette", "price": "53.6", "product_type": "SUNSCREEN", "rating": "1.8", "skintype": "dry"}, {"id": "24", "name": "Bronzing Powder", "price": "37.1", "product_type": "CREAM", "rating": "2.3", "skintype": "dry"}, {"id": "1", "name": "Handbag Holiday Cutile Oil", "price": "100.1", "product_type": "CREAM", "rating": "1.7", "skintype": "dry"}, {"id": "88", "name": "Rich Lip Color", "price": "107.9", "product_type": "MOSITURIZER", "rating": "2.5", "skintype": "dry"}, {"id": "41", "name": "EXTRA Soothing Balm", "price": "19.2", "product_type": "CREAM", "rating": "3", "skintype": "dry"}, {"id": "68", "name": "Lathering Tube Soap", "price": "63.6", "product_type": "MOSITURIZER", "rating": "3.9", "skintype": "dry"}, {"id": "113", "name": "AMC Multicolour System Powder FB Matte", "price": "53.4", "product_type": "SUNSCREEN", "rating": "2.8", "skintype": "dry"}, {"id": "96", "name": "Shimmer Lip Gloss", "price": "78.5", "product_type": "SUNSCREEN", "rating": "2.5", "skintype": "dry"}, {"id": "99", "name": "Soothing Cleansing Oil", "price": "121.6", "product_type": "SUNSCREEN", "rating": "3.6", "skintype": "dry"}, {"id": "107", "name": "Bronzer/Blush Duo", "price": "122", "product_type": "SUNSCREEN", "rating": "2.6", "skintype": "dry"}, {"id": "15", "name": "Angle Eye Shadow", "price": "83.1", "product_type": "CREAM", "rating": "1.9", "skintype": "dry"}, {"id": "36", "name": "EXTRA Balm Rinse", "price": "146.2", "product_type": "CREAM", "rating": "2.9", "skintype": "dry"}, {"id": "54", "name": "Gentle Curl Eye Lash Curler", "price": "23.7", "product_type": "MOSITURIZER", "rating": "1.6", "skintype": "dry"}, {"id": "86", "name": "Retractable Lip", "price": "58.2", "product_type": "MOSITURIZER", "rating": "1.9", "skintype": "dry"}, {"id": "117", "name": "Body Pigment Powder Pearl", "price": "43.3", "product_type": "SUNSCREEN", "rating": "2.9", "skintype": "dry"}, {"id": "43", "name": "Eye Blender", "price": "139.3", "product_type": "CREAM", "rating": "1.6", "skintype": "dry"}, {"id": "4", "name": "Horse Power Nail Fertilizer", "price": "149.1", "product_type": "CREAM", "rating": "3.2", "skintype": "dry"}, {"id": "25", "name": "Brush Cleaning Spray", "price": "81.6", "product_type": "CREAM", "rating": "2.3", "skintype": "dry"}, {"id": "14", "name": "Stiletto Stick Hydrating Heel Balm", "price": "114.4", "product_type": "CREAM", "rating": "2.8", "skintype": "dry"}, {"id": "79", "name": "Nail Lacquer", "price": "35.6", "product_type": "MOSITURIZER", "rating": "1.6", "skintype": "dry"}, {"id": "30", "name": "Cream Shadow", "price": "17.3", "product_type": "CREAM", "rating": "2.7", "skintype": "dry"}, {"id": "3", "name": "Hardwear P.D. Quick Top Coat", "price": "41.3", "product_type": "CREAM", "rating": "1.6", "skintype": "dry"}, {"id": "83", "name": "Powder", "price": "79", "product_type": "MOSITURIZER", "rating": "0.9", "skintype": "dry"}, {"id": "89", "name": "Sheer Color Cheek Tint", "price": "145.2", "product_type": "MOSITURIZER", "rating": "1.9", "skintype": "dry"}]
#similarUser = [{"birthyear": "1995", "gender": "male", "id": "1", "name": "Leland", "pw": "9771", "skintype": "dry", "user_id": "Leland"},{"birthyear": "1996", "gender": "male", "id": "89", "name": "Broderick", "pw": "1061", "skintype": "dry", "user_id": "Broderick"}, {"birthyear": "1991", "gender": "male", "id": "58", "name": "Jody", "pw": "1922", "skintype": "dry", "user_id": "Jody"}, {"birthyear": "1998", "gender": "male", "id": "79", "name": "Jaylin", "pw": "7845", "skintype": "dry", "user_id": "Jaylin"}, {"birthyear": "1991", "gender": "male", "id": "83", "name": "Randolph", "pw": "1611", "skintype": "dry", "user_id": "Randolph"}, {"birthyear": "1995", "gender": "male", "id": "68", "name": "Alexandre", "pw": "6852", "skintype": "dry", "user_id": "Alexandre"}, {"birthyear": "1997", "gender": "female", "id": "36", "name": "Hernan", "pw": "8164", "skintype": "dry", "user_id": "Hernan"}, {"birthyear": "1992", "gender": "male", "id": "24", "name": "Jayden", "pw": "7623", "skintype": "dry", "user_id": "Jayden"}, {"birthyear": "1995", "gender": "male", "id": "75", "name": "Kegan", "pw": "6139", "skintype": "dry", "user_id": "Kegan"}, {"birthyear": "1998", "gender": "male", "id": "41", "name": "Daron", "pw": "9906", "skintype": "dry", "user_id": "Daron"}, {"birthyear": "1997", "gender": "female", "id": "82", "name": "Giancarlo", "pw": "8880", "skintype": "dry", "user_id": "Giancarlo"}, {"birthyear": "1996", "gender": "male", "id": "96", "name": "Darrien", "pw": "9965", "skintype": "dry", "user_id": "Darrien"}, {"birthyear": "1994", "gender": "female", "id": "80", "name": "Titus", "pw": "5014", "skintype": "dry", "user_id": "Titus"}, {"birthyear": "1995", "gender": "male", "id": "15", "name": "Rasheed", "pw": "1410", "skintype": "dry", "user_id": "Rasheed"}, {"birthyear": "1995", "gender": "male", "id": "39", "name": "Augustus", "pw": "6719", "skintype": "dry", "user_id": "Augustus"}, {"birthyear": "1990", "gender": "male", "id": "4", "name": "Kellen", "pw": "1903", "skintype": "dry", "user_id": "Kellen"}, {"birthyear": "1996", "gender": "male", "id": "63", "name": "Auston", "pw": "9079", "skintype": "dry", "user_id": "Auston"}, {"birthyear": "1998", "gender": "female", "id": "93", "name": "Jerrell", "pw": "9834", "skintype": "dry", "user_id": "Jerrell"}, {"birthyear": "1997", "gender": "male", "id": "30", "name": "Rusty", "pw": "2889", "skintype": "dry", "user_id": "Rusty"}, {"birthyear": "1998", "gender": "female", "id": "3", "name": "Efren", "pw": "7497", "skintype": "dry", "user_id": "Efren"}, {"birthyear": "1994", "gender": "female", "id": "88", "name": "Brant", "pw": "2147", "skintype": "dry", "user_id": "Brant"}, {"birthyear": "1995", "gender": "female", "id": "53", "name": "Galen", "pw": "9368", "skintype": "dry", "user_id": "Galen"}, {"birthyear": "1992", "gender": "male", "id": "32", "name": "Trayvon", "pw": "6084", "skintype": "dry", "user_id": "Trayvon"}, {"birthyear": "1994", "gender": "female", "id": "25", "name": "Khari", "pw": "6047", "skintype": "dry", "user_id": "Khari"}, {"birthyear": "1992", "gender": "female", "id": "54", "name": "Najee", "pw": "1753", "skintype": "dry", "user_id": "Najee"}, {"birthyear": "1995", "gender": "male", "id": "1", "name": "Leland", "pw": "9771", "skintype": "dry", "user_id": "Leland"}, {"birthyear": "1991", "gender": "female", "id": "7", "name": "Ted", "pw": "8066", "skintype": "dry", "user_id": "Ted"}, {"birthyear": "1995", "gender": "male", "id": "14", "name": "Misael", "pw": "5178", "skintype": "dry", "user_id": "Misael"}, {"birthyear": "1998", "gender": "male", "id": "86", "name": "Kelton", "pw": "8502", "skintype": "dry", "user_id": "Kelton"}, {"birthyear": "1994", "gender": "female", "id": "70", "name": "Storm", "pw": "3101", "skintype": "dry", "user_id": "Storm"}, {"birthyear": "1995", "gender": "male", "id": "81", "name": "Cristobal", "pw": "7973", "skintype": "dry", "user_id": "Cristobal"}, {"birthyear": "1998", "gender": "male", "id": "78", "name": "Isidro", "pw": "8873", "skintype": "dry", "user_id": "Isidro"}, {"birthyear": "1992", "gender": "female", "id": "43", "name": "Silas", "pw": "8804", "skintype": "dry", "user_id": "Silas"}, {"birthyear": "1995", "gender": "female", "id": "99", "name": "Layne", "pw": "7783", "skintype": "dry", "user_id": "Layne"}, {"birthyear": "1998", "gender": "female", "id": "8", "name": "Unknown", "pw": "7859", "skintype": "dry", "user_id": "Unknown"}, {"birthyear": "1994", "gender": "female", "id": "84", "name": "Dalvin", "pw": "1482", "skintype": "dry", "user_id": "Dalvin"}, {"birthyear": "1995", "gender": "male", "id": "40", "name": "Benny", "pw": "9200", "skintype": "dry", "user_id": "Benny"}, {"birthyear": "1999", "gender": "male", "id": "95", "name": "Carlo", "pw": "4785", "skintype": "dry", "user_id": "Carlo"}]
similarUser = read_csv_and_make_list_dict_dataset("small_users.csv")
similarCos = read_csv_and_make_list_dict_dataset("small_products.csv")
allRating = read_csv_and_make_list_dict_dataset("small_ratings.csv")
print("ratingFIle : ", allRating)

listset = define_lisset(similarCos,similarUser,allRating)
print("listset : ", listset)
dataset = define_dataset(listset["uid_list"], listset["cid_list"], listset["rating_uid_list"], listset["rating_cid_list"], listset["rating_score_list"])
print("dataset : ", dataset)
recommended_id = recommend_hybrid(user_id,similar_user_num,content_num,dataset)
print('\n', recommended_id)

recommended_name = change_id_to_name(listset["cname_list"], listset["cid_list"], recommended_id)
print('\nrecommend item : ', recommended_name)