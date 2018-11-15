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

from flask import Flask, request, render_template
#from google.cloud import datastore


app = Flask(__name__)

# [START main]
@app.route('/')
def main():
    return render_template('about.html')
    '''
    ds = datastore.Client()

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