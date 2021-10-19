import datetime
import json
from json import JSONEncoder

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient


def get_mongo(**kwargs):
	global _mongo_conn
	user='annika'
	pw='securityismypassion'
	_mongo_conn = MongoClient(connect=False, username=user, password=pw, authSource='nonprofit')
	return _mongo_conn


class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


def get_all(request):
	data = []
	conn = get_mongo()
	docs = conn.nonprofit.events.find({})
	for doc in docs:
		doc.pop('_id')
		data.append(doc)
	return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

def edit(request):
	return HttpResponse([])

def create(request):
	return HttpResponse([])

def delete(request):
	return HttpResponse([])

def index(request):
	return render(request, 'index.html')
	# return HttpResponse("Hello world. You're at the client index")

