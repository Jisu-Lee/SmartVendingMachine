import pandas as pd
import numpy as np
import math
from math import sqrt
import pickle

def define_dataset(user_uid, cosmetic_cid, rating_uid, rating_cid, rating_score):
    ub_dataset = {}
    uid_list = []
    cid_list = []
    score_list = []

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
    similar_user = most_similar_users(user_id, similar_user_num, dataset['ub_dataset'])
    
    cb_dataset = dataset['cb_dataset']
    cb_dataset = cb_dataset[cb_dataset['User_id'].isin(similar_user)]
    ratings_training = cb_dataset.sample(frac=0.7)
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
    eval_result = binary_eval(ratings_test, w_matrix, adjusted_ratings, rating_mean)
    print('Evaluation result - precision: %f, recall: %f' % eval_result)

    # get a recommendation list for a given user
    recommended_cosmetics = recommendCB(2, w_matrix, adjusted_ratings, rating_mean)
    return recommended_cosmetics[0:content_num]

def change_id_to_name(cosmetic_name, cosmetic_cid, recommended_item):
    recommended_cid = recommended_item['Cos_id']

    recommended_name = []
    for cos_id in recommended_cid:
        recommended_name.append(cosmetic_name[cosmetic_cid.index(cos_id)])
    return recommended_name

def define_listset(similarUser, similarCos, allRating):
	uid_list = []
	cid_list = []
	rating_uid_list = []
	rating_cid_list = []
	rating_score_list = []

	k = 0
	for i in range(len(similarUser)):
		uid_list.append(similarUser[i]["id"])
	
	for i in range(len(similarCos)):
		cid_list.append(similarCos[i]["id"])

	for i in range(len(allRating)):
		rating_uid_list.append(allRating[i]["user_id"])
		rating_cid_list.append(allRating[i]["cosmetic_id"])
		rating_score_list.append(allRating[i]["rating"])

	dataset = {'uid_list' : uid_list, 'cid_list' : cid_list, "rating_uid_list" : rating_uid_list, "rating_cid_list" : rating_cid_list, "rating_score_list" : rating_score_list}
	return dataset
