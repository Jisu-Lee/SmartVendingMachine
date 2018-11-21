# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import socket
import logging
import algo

# related to recommendation algorithm
import csv
import pandas as pd
import numpy as np
import math
from math import sqrt
import pickle

from flask import Flask, request, render_template

from google.cloud import datastore


app = Flask(__name__)


@app.route('/list')
@app.route('/')
def list():
    return render_template('list.html')

@app.route('/favorite')
def favorite():
    
    ds = datastore.Client()

    queries = ds.query(kind='cosmetics')
    entities = queries.fetch(limit=10)
    fav_list = list(entities)
    
    fav_list = [{"id": "110", "name": "eye paint eye shadow", "price": "76.2", "product_type": "sunscreen", "rating": "4.9", "skintype": "dry"}, {"id": "100", "name": "sparkle eye shadow", "price": "111", "product_type": "sunscreen", "rating": "2.4", "skintype": "oily"}, {"id": "102", "name": "treatment lip shine", "price": "18.2", "product_type": "sunscreen", "rating": "2", "skintype": "dry"}, {"id": "103", "name": "tweezer", "price": "54.5", "product_type": "sunscreen", "rating": "2.8", "skintype": "oily"}, {"id": "26", "name": "buffing grains for face", "price": "24.2", "product_type": "cream", "rating": "2.9", "skintype": "oily"}, {"id": "119", "name": "amc bronzing powder", "price": "23.2", "product_type": "sunscreen", "rating": "2.4", "skintype": "sensitive"}, {"id": "98", "name": "shimmer wash eye shadow", "price": "20.3", "product_type": "sunscreen", "rating": "2.1", "skintype": "sensitive"}, {"id": "120", "name": "amc multicolour system bronzing powder", "price": "149.6", "product_type": "sunscreen", "rating": "2.6", "skintype": "dry"}, {"id": "105", "name": "vitamin enriched face base", "price": "121.6", "product_type": "sunscreen", "rating": "2.2", "skintype": "sensitive"}, {"id": "80", "name": "natural brow shaper \u0026 hair touch up", "price": "127.1", "product_type": "mositurizer", "rating": "1.6", "skintype": "dry"}]


    return render_template('favorite.html', fav_list=fav_list)

# local debugging    
@app.route('/recommand')
def recommand():
    '''
    ds = datastore.Client()
    # get user data
    user_id = 1 
    query = ds.query(kind='user')
    query.add_filter('id', '=', str(user_id))
    entity = query.fetch(limit=1)
    userInfo = list(entity)
    # get users with same skintype
    skintype = "dry"
    query = ds.query(kind='user')
    query.add_filter('skintype', '=', str(skintype))
    entity = query.fetch()
    similarUser = list(entity)
    # get cosmetics with same skintype
    query = ds.query(kind='cosmetics')
    query.add_filter('skintype', '=', str(skintype))
    entity = query.fetch()
    similarCos = list(entity)
    # get all rating data
    query = ds.query(kind='favorite')
    entity = query.fetch(limit=20)
    allRating = list(entity)
    '''
    
    user_id = 1
    similar_user_num = 5
    content_num = 3
    user_uid = [1,2,3,4,5,6,7,8,9,10]       # users with similar skintype

    cosmetic_name = ['a','b','c','d','e','f']   # cosmetic - name
    cosmetic_cid = [1,2,3,4,5,6]                # cosmetics with skintype
    cosmetic_ptype = 'Oily'                     # cosmetic - product_type
    # all info from ratings
    rating_uid =    [1,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15]   # rating - user_id
    rating_cid =    [1,2,3,1,2,3,8,4,1,5,2,5,3,6,5,1,3,2,8,2,2,1,3,1,9,7,5,8,3,9,5,8]               # rating - cosmetic_id
    rating_score =  [1.1,1.9,1.3,1.5,1.8,1.2,2.2,2.3,2.1,2.8,3.0,3.2,3.4,3.5,1.1,3.6,
                     3.1,4.1,4.7,4.6,4.3,5.0,3.1,4.6,0.5,5.0,1.1,1.2,1.3,1.4,1.5,2.2]               # rating - score

    dataset = algo.define_dataset(user_uid, cosmetic_cid, rating_uid, rating_cid, rating_score)

    while True:
        try:
            recommended_id = algo.recommend_hybrid(user_id,similar_user_num,content_num,dataset)
            break
        except ZeroDivisionError:
            app.logger.info("Oops!  That was no valid number.  Try again...")

    recommended_name = algo.change_id_to_name(cosmetic_name, cosmetic_cid, recommended_id)
    app.logger.info(recommended_name)

    # dummy data
    fav_list = [{"id": "110", "name": "eye paint eye shadow", "price": "76.2", "product_type": "sunscreen", "rating": "4.9", "skintype": "dry"}, {"id": "100", "name": "sparkle eye shadow", "price": "111", "product_type": "sunscreen", "rating": "2.4", "skintype": "oily"}, {"id": "102", "name": "treatment lip shine", "price": "18.2", "product_type": "sunscreen", "rating": "2", "skintype": "dry"}, {"id": "103", "name": "tweezer", "price": "54.5", "product_type": "sunscreen", "rating": "2.8", "skintype": "oily"}, {"id": "26", "name": "buffing grains for face", "price": "24.2", "product_type": "cream", "rating": "2.9", "skintype": "oily"}, {"id": "119", "name": "amc bronzing powder", "price": "23.2", "product_type": "sunscreen", "rating": "2.4", "skintype": "sensitive"}, {"id": "98", "name": "shimmer wash eye shadow", "price": "20.3", "product_type": "sunscreen", "rating": "2.1", "skintype": "sensitive"}, {"id": "120", "name": "amc multicolour system bronzing powder", "price": "149.6", "product_type": "sunscreen", "rating": "2.6", "skintype": "dry"}, {"id": "105", "name": "vitamin enriched face base", "price": "121.6", "product_type": "sunscreen", "rating": "2.2", "skintype": "sensitive"}, {"id": "80", "name": "natural brow shaper \u0026 hair touch up", "price": "127.1", "product_type": "mositurizer", "rating": "1.6", "skintype": "dry"}]
    userInfo = [{"birthyear": "1995", "gender": "male", "id": "1", "name": "Leland", "pw": "9771", "skintype": "dry", "user_id": "Leland"}]
    similarCos = [{"id": "110", "name": "Eye Paint Eye Shadow", "price": "76.2", "product_type": "SUNSCREEN", "rating": "4.9", "skintype": "dry"}, {"id": "102", "name": "Treatment Lip Shine", "price": "18.2", "product_type": "SUNSCREEN", "rating": "2", "skintype": "dry"}, {"id": "120", "name": "AMC Multicolour System Bronzing Powder", "price": "149.6", "product_type": "SUNSCREEN", "rating": "2.6", "skintype": "dry"}, {"id": "80", "name": "Natural Brow Shaper \u0026 hair Touch up", "price": "127.1", "product_type": "MOSITURIZER", "rating": "1.6", "skintype": "dry"}, {"id": "78", "name": "Metallic Long-Wear Cream Shadow", "price": "75.6", "product_type": "MOSITURIZER", "rating": "2.1", "skintype": "dry"}, {"id": "112", "name": "AMC Face Blush", "price": "144", "product_type": "SUNSCREEN", "rating": "2.1", "skintype": "dry"}, {"id": "82", "name": "Pot Rouge for Lips \u0026 Cheeks", "price": "121.7", "product_type": "MOSITURIZER", "rating": "2.8", "skintype": "dry"}, {"id": "63", "name": "Ink Eyeliner", "price": "106.9", "product_type": "MOSITURIZER", "rating": "1.5", "skintype": "dry"}, {"id": "75", "name": "Long-Wear Eye Pencil", "price": "12.6", "product_type": "MOSITURIZER", "rating": "1.8", "skintype": "dry"}, {"id": "106", "name": "Lip Palette", "price": "122.2", "product_type": "SUNSCREEN", "rating": "1.8", "skintype": "dry"}, {"id": "58", "name": "Hydrating Face Tonic", "price": "20", "product_type": "MOSITURIZER", "rating": "2.7", "skintype": "dry"}, {"id": "8", "name": "Nail File", "price": "91.3", "product_type": "CREAM", "rating": "3.2", "skintype": "dry"}, {"id": "7", "name": "Melt Away Cuticle Eliminator", "price": "14.6", "product_type": "CREAM", "rating": "2.2", "skintype": "dry"}, {"id": "40", "name": "EXTRA Repair Serum", "price": "22.1", "product_type": "CREAM", "rating": "1.9", "skintype": "dry"}, {"id": "70", "name": "Lip Color", "price": "97.5", "product_type": "MOSITURIZER", "rating": "2", "skintype": "dry"}, {"id": "93", "name": "Sheer Powder", "price": "90.1", "product_type": "SUNSCREEN", "rating": "1.1", "skintype": "dry"}, {"id": "95", "name": "Shimmer Brick", "price": "67", "product_type": "SUNSCREEN", "rating": "2.2", "skintype": "dry"}, {"id": "32", "name": "Creamy Matte Lip Color", "price": "38", "product_type": "CREAM", "rating": "2.1", "skintype": "dry"}, {"id": "84", "name": "Protective Face Lotion", "price": "138.3", "product_type": "MOSITURIZER", "rating": "2.5", "skintype": "dry"}, {"id": "81", "name": "No Smudge Mascara", "price": "76.5", "product_type": "MOSITURIZER", "rating": "3.6", "skintype": "dry"}, {"id": "39", "name": "EXTRA Repair Moisturizing Balm SPF 25", "price": "43.7", "product_type": "CREAM", "rating": "2.3", "skintype": "dry"}, {"id": "53", "name": "Foundation", "price": "142.2", "product_type": "MOSITURIZER", "rating": "1.8", "skintype": "dry"}, {"id": "104", "name": "Ultra Fine Eyeliner", "price": "145.7", "product_type": "SUNSCREEN", "rating": "2.6", "skintype": "dry"}, {"id": "109", "name": "Eye Paint Palette", "price": "53.6", "product_type": "SUNSCREEN", "rating": "1.8", "skintype": "dry"}, {"id": "24", "name": "Bronzing Powder", "price": "37.1", "product_type": "CREAM", "rating": "2.3", "skintype": "dry"}, {"id": "1", "name": "Handbag Holiday Cutile Oil", "price": "100.1", "product_type": "CREAM", "rating": "1.7", "skintype": "dry"}, {"id": "88", "name": "Rich Lip Color", "price": "107.9", "product_type": "MOSITURIZER", "rating": "2.5", "skintype": "dry"}, {"id": "41", "name": "EXTRA Soothing Balm", "price": "19.2", "product_type": "CREAM", "rating": "3", "skintype": "dry"}, {"id": "68", "name": "Lathering Tube Soap", "price": "63.6", "product_type": "MOSITURIZER", "rating": "3.9", "skintype": "dry"}, {"id": "113", "name": "AMC Multicolour System Powder FB Matte", "price": "53.4", "product_type": "SUNSCREEN", "rating": "2.8", "skintype": "dry"}, {"id": "96", "name": "Shimmer Lip Gloss", "price": "78.5", "product_type": "SUNSCREEN", "rating": "2.5", "skintype": "dry"}, {"id": "99", "name": "Soothing Cleansing Oil", "price": "121.6", "product_type": "SUNSCREEN", "rating": "3.6", "skintype": "dry"}, {"id": "107", "name": "Bronzer/Blush Duo", "price": "122", "product_type": "SUNSCREEN", "rating": "2.6", "skintype": "dry"}, {"id": "15", "name": "Angle Eye Shadow", "price": "83.1", "product_type": "CREAM", "rating": "1.9", "skintype": "dry"}, {"id": "36", "name": "EXTRA Balm Rinse", "price": "146.2", "product_type": "CREAM", "rating": "2.9", "skintype": "dry"}, {"id": "54", "name": "Gentle Curl Eye Lash Curler", "price": "23.7", "product_type": "MOSITURIZER", "rating": "1.6", "skintype": "dry"}, {"id": "86", "name": "Retractable Lip", "price": "58.2", "product_type": "MOSITURIZER", "rating": "1.9", "skintype": "dry"}, {"id": "117", "name": "Body Pigment Powder Pearl", "price": "43.3", "product_type": "SUNSCREEN", "rating": "2.9", "skintype": "dry"}, {"id": "43", "name": "Eye Blender", "price": "139.3", "product_type": "CREAM", "rating": "1.6", "skintype": "dry"}, {"id": "4", "name": "Horse Power Nail Fertilizer", "price": "149.1", "product_type": "CREAM", "rating": "3.2", "skintype": "dry"}, {"id": "25", "name": "Brush Cleaning Spray", "price": "81.6", "product_type": "CREAM", "rating": "2.3", "skintype": "dry"}, {"id": "14", "name": "Stiletto Stick Hydrating Heel Balm", "price": "114.4", "product_type": "CREAM", "rating": "2.8", "skintype": "dry"}, {"id": "79", "name": "Nail Lacquer", "price": "35.6", "product_type": "MOSITURIZER", "rating": "1.6", "skintype": "dry"}, {"id": "30", "name": "Cream Shadow", "price": "17.3", "product_type": "CREAM", "rating": "2.7", "skintype": "dry"}, {"id": "3", "name": "Hardwear P.D. Quick Top Coat", "price": "41.3", "product_type": "CREAM", "rating": "1.6", "skintype": "dry"}, {"id": "83", "name": "Powder", "price": "79", "product_type": "MOSITURIZER", "rating": "0.9", "skintype": "dry"}, {"id": "89", "name": "Sheer Color Cheek Tint", "price": "145.2", "product_type": "MOSITURIZER", "rating": "1.9", "skintype": "dry"}]
    similarUser = [{"birthyear": "1996", "gender": "male", "id": "89", "name": "Broderick", "pw": "1061", "skintype": "dry", "user_id": "Broderick"}, {"birthyear": "1991", "gender": "male", "id": "58", "name": "Jody", "pw": "1922", "skintype": "dry", "user_id": "Jody"}, {"birthyear": "1998", "gender": "male", "id": "79", "name": "Jaylin", "pw": "7845", "skintype": "dry", "user_id": "Jaylin"}, {"birthyear": "1991", "gender": "male", "id": "83", "name": "Randolph", "pw": "1611", "skintype": "dry", "user_id": "Randolph"}, {"birthyear": "1995", "gender": "male", "id": "68", "name": "Alexandre", "pw": "6852", "skintype": "dry", "user_id": "Alexandre"}, {"birthyear": "1997", "gender": "female", "id": "36", "name": "Hernan", "pw": "8164", "skintype": "dry", "user_id": "Hernan"}, {"birthyear": "1992", "gender": "male", "id": "24", "name": "Jayden", "pw": "7623", "skintype": "dry", "user_id": "Jayden"}, {"birthyear": "1995", "gender": "male", "id": "75", "name": "Kegan", "pw": "6139", "skintype": "dry", "user_id": "Kegan"}, {"birthyear": "1998", "gender": "male", "id": "41", "name": "Daron", "pw": "9906", "skintype": "dry", "user_id": "Daron"}, {"birthyear": "1997", "gender": "female", "id": "82", "name": "Giancarlo", "pw": "8880", "skintype": "dry", "user_id": "Giancarlo"}, {"birthyear": "1996", "gender": "male", "id": "96", "name": "Darrien", "pw": "9965", "skintype": "dry", "user_id": "Darrien"}, {"birthyear": "1994", "gender": "female", "id": "80", "name": "Titus", "pw": "5014", "skintype": "dry", "user_id": "Titus"}, {"birthyear": "1995", "gender": "male", "id": "15", "name": "Rasheed", "pw": "1410", "skintype": "dry", "user_id": "Rasheed"}, {"birthyear": "1995", "gender": "male", "id": "39", "name": "Augustus", "pw": "6719", "skintype": "dry", "user_id": "Augustus"}, {"birthyear": "1990", "gender": "male", "id": "4", "name": "Kellen", "pw": "1903", "skintype": "dry", "user_id": "Kellen"}, {"birthyear": "1996", "gender": "male", "id": "63", "name": "Auston", "pw": "9079", "skintype": "dry", "user_id": "Auston"}, {"birthyear": "1998", "gender": "female", "id": "93", "name": "Jerrell", "pw": "9834", "skintype": "dry", "user_id": "Jerrell"}, {"birthyear": "1997", "gender": "male", "id": "30", "name": "Rusty", "pw": "2889", "skintype": "dry", "user_id": "Rusty"}, {"birthyear": "1998", "gender": "female", "id": "3", "name": "Efren", "pw": "7497", "skintype": "dry", "user_id": "Efren"}, {"birthyear": "1994", "gender": "female", "id": "88", "name": "Brant", "pw": "2147", "skintype": "dry", "user_id": "Brant"}, {"birthyear": "1995", "gender": "female", "id": "53", "name": "Galen", "pw": "9368", "skintype": "dry", "user_id": "Galen"}, {"birthyear": "1992", "gender": "male", "id": "32", "name": "Trayvon", "pw": "6084", "skintype": "dry", "user_id": "Trayvon"}, {"birthyear": "1994", "gender": "female", "id": "25", "name": "Khari", "pw": "6047", "skintype": "dry", "user_id": "Khari"}, {"birthyear": "1992", "gender": "female", "id": "54", "name": "Najee", "pw": "1753", "skintype": "dry", "user_id": "Najee"}, {"birthyear": "1995", "gender": "male", "id": "1", "name": "Leland", "pw": "9771", "skintype": "dry", "user_id": "Leland"}, {"birthyear": "1991", "gender": "female", "id": "7", "name": "Ted", "pw": "8066", "skintype": "dry", "user_id": "Ted"}, {"birthyear": "1995", "gender": "male", "id": "14", "name": "Misael", "pw": "5178", "skintype": "dry", "user_id": "Misael"}, {"birthyear": "1998", "gender": "male", "id": "86", "name": "Kelton", "pw": "8502", "skintype": "dry", "user_id": "Kelton"}, {"birthyear": "1994", "gender": "female", "id": "70", "name": "Storm", "pw": "3101", "skintype": "dry", "user_id": "Storm"}, {"birthyear": "1995", "gender": "male", "id": "81", "name": "Cristobal", "pw": "7973", "skintype": "dry", "user_id": "Cristobal"}, {"birthyear": "1998", "gender": "male", "id": "78", "name": "Isidro", "pw": "8873", "skintype": "dry", "user_id": "Isidro"}, {"birthyear": "1992", "gender": "female", "id": "43", "name": "Silas", "pw": "8804", "skintype": "dry", "user_id": "Silas"}, {"birthyear": "1995", "gender": "female", "id": "99", "name": "Layne", "pw": "7783", "skintype": "dry", "user_id": "Layne"}, {"birthyear": "1998", "gender": "female", "id": "8", "name": "Unknown", "pw": "7859", "skintype": "dry", "user_id": "Unknown"}, {"birthyear": "1994", "gender": "female", "id": "84", "name": "Dalvin", "pw": "1482", "skintype": "dry", "user_id": "Dalvin"}, {"birthyear": "1995", "gender": "male", "id": "40", "name": "Benny", "pw": "9200", "skintype": "dry", "user_id": "Benny"}, {"birthyear": "1999", "gender": "male", "id": "95", "name": "Carlo", "pw": "4785", "skintype": "dry", "user_id": "Carlo"}]
    allRating = [{"cosmetic_id": "116", "rating": "1.9", "user_id": "46"}, {"cosmetic_id": "55", "rating": "4.3", "user_id": "27"}, {"cosmetic_id": "56", "rating": "4.1", "user_id": "1"}, {"cosmetic_id": "10", "rating": "4.1", "user_id": "13"}, {"cosmetic_id": "119", "rating": "2.1", "user_id": "34"}, {"cosmetic_id": "4", "rating": "2", "user_id": "40"}, {"cosmetic_id": "102", "rating": "1.3", "user_id": "44"}, {"cosmetic_id": "109", "rating": "0.6", "user_id": "32"}, {"cosmetic_id": "81", "rating": "1.2", "user_id": "31"}, {"cosmetic_id": "80", "rating": "2.7", "user_id": "18"}, {"cosmetic_id": "98", "rating": "2.4", "user_id": "25"}, {"cosmetic_id": "55", "rating": "2.5", "user_id": "36"}, {"cosmetic_id": "73", "rating": "2.1", "user_id": "16"}, {"cosmetic_id": "116", "rating": "1", "user_id": "20"}, {"cosmetic_id": "104", "rating": "0.1", "user_id": "9"}, {"cosmetic_id": "58", "rating": "1", "user_id": "46"}, {"cosmetic_id": "90", "rating": "0.1", "user_id": "26"}, {"cosmetic_id": "63", "rating": "3.5", "user_id": "2"}, {"cosmetic_id": "77", "rating": "2.8", "user_id": "18"}, {"cosmetic_id": "48", "rating": "1.7", "user_id": "43"}]
    
    return render_template('recommand.html', userInfo=recommended_name, similarCos=similarCos, similarUser=similarUser, allRating=allRating)
                

@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/userdata')
def userdata():
    return render_template('userdata.html')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

    '''
	cos_name = 'Sidmool Cream'
	cos_skintype = 'dry'
	cos_price = 200
	cos_rating = 4.5

	entity = datastore.Entity(key=ds.key('cosmetics'))
	entity.update({
		'name': cos_name,
		'skintype': cos_skintype,
		'price': cos_price,
		'rating': cos_rating
	})

	ds.put(entity)

	query = ds.query(kind='cosmetics', order=('-name',))

	results = [
		'name: {name} price: {price} rating: {rating}'.format(**x)
		for x in query.fetch(limit=10)]

	output = 'list of cosmetics:\n{}'.format('\n'.join(results))

    return output, 200, {'Content-Type': 'text/plain; charset=utf-8'} 
    '''

    '''
    # reading csv
    cinputFile = open('newproducts.csv','r',encoding='"UTF-8"')
    cFile = csv.reader(cinputFile)
    for i,line in enumerate(cFile):
        if( i is not 0):
            ds = datastore.Client()
            entity = datastore.Entity(key=ds.key('cosmetics'))
            entity.update({
                'id' : line[0],
                'name': line[1],
                'skintype': line[3],
                'product_type' : line[2],
                'price' : line[4],
                'rating' : line[5]
            })
            ds.put(entity)
    cinputFile.close()
    rinputFile = open('newratings.csv','r',encoding='"UTF-8"')
    rFile = csv.reader(rinputFile)
    for i,line in enumerate(rFile):
        if( i is not 0):
            ds = datastore.Client()
            entity = datastore.Entity(key=ds.key('favorite'))
            entity.update({
                'user_id' : line[0],
                'cosmetic_id': line[1],
                'rating': line[2],
            })
            ds.put(entity)
    rinputFile.close()
    '''