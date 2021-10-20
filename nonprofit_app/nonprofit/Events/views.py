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
	post = request.POST.dict()
	start = datetime.datetime.strptime(post['start'], "%m/%d/%Y %H:%M %p")
	end = datetime.datetime.strptime(post['end'], "%m/%d/%Y %H:%M %p")
	possible = [1, 2, 3, 4, 5, 6, 7, 8, 9, 19]
	conn = get_mongo()
	docs = conn.nonprofit.events.find({})
	for d in docs:
		if d['id'] in possible:
			possible.pop(possible.index(d['id']))

	doc = {
		'name': post['myname'],
		'description': post['description'],
		'start': start,
		'end': end,
		'id': possible[0],
		'volunteers_needed': post['num_volunteers'],
		'volunteers': [],
		'donations': [],
		'location': post['location']
	}
	conn.nonprofit.events.insert(doc)
	return HttpResponse({'success': 'true'})
	# {'success': 'true', 'X-Frame-Options': 'Fuckthis', 'status_code': 200}


def delete(request):
	return HttpResponse([])

def index(request):
	return render(request, 'index.html')
	# return HttpResponse("Hello world. You're at the client index")

