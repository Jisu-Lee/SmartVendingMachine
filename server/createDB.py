
from google.appengine.ext import ndb
from google.appengine.api import users

class User(ndb.Model):
	id = ndb.FloatProperty()
	pw = ndb.StringProperty()
	name = ndb.StringProperty()
	gender = ndb.StringProperty()
	birthyear = ndb.IntegerProperty()
	skintype = ndb.StringProperty()

class Vending(ndb.Model):
	id = ndb.IntegerProperty()
	wedo = ndb.FloatProperty()
	kyungdo = ndb.FloatProperty()

class Cosmetics(ndb.Model):
	id = ndb.IntegerProperty()
	name = ndb.StringProperty()
	skintype = ndb.StringProperty()
	product_type = ndb.StringProperty()
	price = ndb.FloatProperty()
	rating = ndb.FloatProperty()

class Favorite(ndb.Model):
	user_id = ndb.StringProperty()
	cos_name = ndb.StringProperty()
	rating = ndb.FloatProperty()

class Stock(ndb.Model):
	ven_id = ndb.IntegerProperty()
	cos_name = ndb.FloatProperty()
	quantity = ndb.IntegerProperty()