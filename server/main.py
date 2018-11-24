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

# related to recommandation algorithm
import csv
import pandas as pd
import numpy as np
import math
from math import sqrt
import pickle

from flask import Flask, request, redirect, url_for, render_template

from google.cloud import datastore

app = Flask(__name__)

user_id = 1
userInfo = [{"birthyear": "1995", "gender": "male", "id": "1", "name": "Leland", "pw": "9771", "skintype": "dry", "user_id": "Leland"}]

def getCosmeticsWithFav():
    ds = datastore.Client()
    query = ds.query(kind='cosmetics')
    entity = query.fetch()
    cosmetics = list(entity)    

    query = ds.query(kind='favorite')
    query.add_filter('user_id', '=', str(user_id))
    entity = query.fetch()
    userPick = []
    for i in range(len(cosmetics)):
        cosmetics[i].update({'fav_flag':'false'})
    if(entity is not None):
        userPick = list(entity)
        for i in range(len(userPick)):
            for j in range(len(cosmetics)):
                if(cosmetics[j]['id'] == userPick[i]['cosmetic_id']):
                    cosmetics[j].update({'fav_flag':'true'})
    return cosmetics                    

def getUsers():
    ds = datastore.Client()
    query = ds.query(kind='user')
    entity = query.fetch()
    return list(entity)

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/getlogin', methods=['GET', 'POST'])
def getlogin():
    if(request.json):
        data = request.json
        uid = data["data"][0]
        upw = data["data"][1]
        users = getUsers()
        for user in users:
            if(user["id"] == uid and user["pw"] ==  upw):
                global user_id
                user_id = uid
                global userInfo
                userInfo = []
                userInfo.append(user)
                return json.dumps({'status':'ok'})
    return json.dumps({'status':'fail'})

@app.route('/list') 
@app.route('/')
def getlist():
    cosmetics = getCosmeticsWithFav()
    cosList = []
    for tmp in cosmetics:
        list_item = [int(tmp["id"]), tmp["name"], float(tmp["price"]), float(tmp["rating"]), tmp["product_type"], tmp["fav_flag"]]
        cosList.append(list_item)

    for i in range(len(cosList)):
        ptype = cosList[i][4].upper()
        if(ptype == "SUNSCREEN"):
            cosList[i][4] = "sunblock"
        elif(ptype == "MOSITURIZER"):
            cosList[i][4] = "skin"
        elif(ptype == "CREAM"):
            cosList[i][4] = "lotion"

    return render_template('list.html', cosList=cosList, user_id=user_id)

'''
add: {"data":[user, cos, rating]}
remove: {"data":[user, cos, -1]}
'''
@app.route('/updatefav', methods=['GET','POST'])
def updatefav():
    print(request.json)

    if request.json:
        data = request.json
        uid = data["data"][0]
        cid = data["data"][1]
        rating = data["data"][2]
        print(uid, ",", cid, ",", rating)
#favorite table
    
    return redirect(url_for('getlist'))

# local debugging    
@app.route('/recommand')
def recommand():
    ds = datastore.Client()
    # get user data
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
    entity = query.fetch()
    allRating = list(entity)

    recommanded_name = ["a", "b", "c"]
    list_dataset = algo.define_listset(similarUser, similarCos, allRating)
    dataset = algo.define_dataset(list_dataset["uid_list"], list_dataset["cid_list"], list_dataset["rating_uid_list"], list_dataset["rating_cid_list"], list_dataset["rating_score_list"])

    while True:
        try:
            recommanded_id = algo.recommand_hybrid(user_id,10,3,dataset)
            break
        except ZeroDivisionError:
            logging.info("Oops!  That was no valid number.  Try again...")

    recommanded_name = algo.change_id_to_name(list_dataset["cname_list"], list_dataset["cid_list"], recommanded_id["Cos_id"])
    
    cosmetics = getCosmeticsWithFav()
    recommanded_cos = []
    n = len(cosmetics)
    for i in range(len(recommanded_name)):
        for j in range(n):
            if(cosmetics[j]["name"] == recommanded_name[i]):
                recommanded_cos.append(cosmetics[j])
                break

    return render_template('recommand.html', recommanded_cos=recommanded_cos, similarCos=similarCos, similarUser=similarUser, allRating=allRating)
                

@app.route('/favorite')
def favorite():
    cosmetics = getCosmeticsWithFav()
    fav_list = []
    for i in range(len(cosmetics)):
        if(cosmetics[i]['fav_flag'] == 'true'):
            fav_list.append(cosmetics[i])
            if(len(fav_list) > 10):
                break
    for i in range(len(fav_list)):
        fav_list[i]["rating"] = float(fav_list[i]["rating"])
    fav_list = sorted(fav_list, key=lambda k: k['rating'], reverse=True)
    return render_template('favorite.html', fav_list=fav_list)


@app.route('/map')
def map():
    cosmetics = getCosmeticsWithFav()
    ds = datastore.Client()
    query = ds.query(kind='vending')
    entity = query.fetch()
    locationsDic = list(entity)

    query = ds.query(kind='stock')
    entity = query.fetch()
    stocks = list(entity)
    # stock(cos_id, ven_id, rating)
    data = []
    for i in range(len(locationsDic)):
        data.append([])
        data[i].append(int(locationsDic[i]["id"]))
        for j in range(len(stocks)):
            if(data[i][0] == int(stocks[j]["ven_id"])):
                tmp = []
                for item in cosmetics:    # for name, age in dictionary.iteritems():  (for Python 2.x)
                    if item["id"] == stocks[j]["cos_id"]:
                        tmp.append(item["name"])
                tmp.append(stocks[j]["rating"])
                data[i].append(tmp)
    locations = []
    for tmp in locationsDic:
        list_item = [int(tmp["id"]), tmp["name"], tmp["wedo"], tmp["kyungdo"], tmp["address"]]
        locations.append(list_item)

    return render_template('map.html', data=data, locations=locations)

@app.route('/userdata')
def userdata():
    return render_template('userdata.html', user=userInfo)

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
@app.route('/data')
def data():
    # reading ve csv
    sinputFile = open('newstock.csv','r',encoding='"UTF-8"')
    sFile = csv.reader(sinputFile)
    for i,line in enumerate(sFile):
        if( i is not 0):
            ds = datastore.Client()
            entity = datastore.Entity(key=ds.key('stock'))
            entity.update({
                'cos_id' : line[1],
                'ven_id': line[0],
                'rating': line[2]
            })
            ds.put(entity)
    sinputFile.close()
    return "done"
    # reading cosmetic csv
    
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
    # reading rating csv
    rinputFile = open('newratings.csv','r',encoding='"UTF-8"')
    rFile = csv.reader(rinputFile)
    for i,line in enumerate(rFile):
        if( i is not 0):
            ds = datastore.Client()
            entity = datastore.Entity(key=ds.key('favorite'))
            entity.update({
                'user_id' : line[0],
                'cosmetic_id': line[1],
                'rating': line[2]
            })
            ds.put(entity)
    rinputFile.close()
    # reading ve csv
    sinputFile = open('newstock.csv','r',encoding='"UTF-8"')
    sFile = csv.reader(sinputFile)
    for i,line in enumerate(sFile):
        if( i is not 0):
            ds = datastore.Client()
            entity = datastore.Entity(key=ds.key('stock'))
            entity.update({
                'cos_id' : line[1],
                'ven_id': line[0],
                'rating': line[2]
            })
            ds.put(entity)
    sinputFile.close()
    
    # reading vending csv
    vinputFile = open('newvendings.csv','r',encoding='"UTF-8"')
    vFile = csv.reader(vinputFile)
    for i,line in enumerate(vFile):
        if( i is not 0):
            ds = datastore.Client()
            entity = datastore.Entity(key=ds.key('vending'))
            entity.update({
                'id' : line[0],
                'kyungdo': line[1],
                'wedo': line[2],
                'name': line[3],
                'address': line[4]
            })
            ds.put(entity)
    vinputFile.close()
    return "done"
    '''
