

from pymongo import MongoClient

def get_mongo(**kwargs):
	global _mongo_conn
	user='annika'
	pw='securityismypassion'
	_mongo_conn = MongoClient(connect=False, username=user, password=pw, authSource='nonprofit')
	return _mongo_conn