import datetime
import json
from json import JSONEncoder
import pytz
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
	dt = datetime.datetime.now(tz=pytz.timezone('US/Central'))
	for doc in docs:
		doc.pop('_id')
		doc.pop('volunteers')
		doc.pop('donations')
		doc.pop('volunteers_needed')
		doc.pop('description')
		doc['endnew'] = pytz.timezone("US/Central").localize(doc['end'])
		if doc['endnew'] > dt:
			data.append(doc)
	return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

def edit(request):
	return HttpResponse([])

def create(request):
	post = request.POST.dict()
	start = datetime.datetime.strptime(post['start'], "%m/%d/%Y %H:%M %p")
	end = datetime.datetime.strptime(post['end'], "%m/%d/%Y %H:%M %p")
	conn = get_mongo()
	docs = conn.nonprofit.events.find({})
	greatest_id = 0
	for d in docs:
		if d['id'] > greatest_id:
			greatest_id = int(d['id'])

	doc = {
		'name': post['myname'],
		'description': post['description'],
		'start': start,
		'end': end,
		'id': greatest_id + 1,
		'volunteers_needed': post['num_volunteers'],
		'volunteers': [],
		'donations': [],
		'location': post['location']
	}
	conn.nonprofit.events.insert(doc)
	return HttpResponse({'success': 'true'})
	# {'success': 'true', 'X-Frame-Options': 'Fuckthis', 'status_code': 200}


def delete(request):
	try:
		conn = get_mongo()
		conn.nonprofit.events.remove({'id': int(request.POST['models[0][id]'])})
	except Exception as e:
		return HttpResponse({'error': e})
	return HttpResponse({'success': 'true'})

def index(request):
	return render(request, 'index.html')
	# return HttpResponse("Hello world. You're at the client index")

