import datetime
import json
from json import JSONEncoder

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import HttpResponse
from nonprofit.extra.view_helper import get_mongo


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
		doc.pop('volunteers')
		doc.pop('donations')
		doc.pop('volunteers_needed')
		doc.pop('description')
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

