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

def get_all_time(request):
	data = []
	conn = get_mongo()
	docs = conn.nonprofit.events.find({})
	for doc in docs:
		doc.pop('_id')
		doc['startdate'] = doc['start'].date()
		doc['start'] = doc['start'].time()
		doc['end'] = doc['end'].time()
		doc.pop('volunteers')
		doc.pop('donations')
		doc.pop('volunteers_needed')
		doc['start'] = doc['start'].strftime("%H:%M")
		d = datetime.datetime.strptime(doc['start'], "%H:%M")
		doc['start'] = d.strftime("%I:%M %p")
		doc['end'] = doc['end'].strftime("%H:%M")
		d = datetime.datetime.strptime(doc['end'], "%H:%M")
		doc['end'] = d.strftime("%I:%M %p")
		doc['myid'] = doc['id']
		# doc.pop('id')
		data.append(doc)
	return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

def uncancel_event(request):
	try:
		conn = get_mongo()
		doc = conn.nonprofit.cancelled_events.find_one({'id': int(request.POST['id'])})
		dt = datetime.datetime.now()
		if doc['start'] < dt:
			return HttpResponse("error")
		# doc.pop('_id')
		conn.nonprofit.events.insert(doc)
		conn.nonprofit.cancelled_events.remove({'id': int(request.POST['id'])})
	except Exception as e:
		return HttpResponse('error')
	return HttpResponse("Good")

def get_cancelled(request):
	data = []
	conn = get_mongo()
	docs = conn.nonprofit.cancelled_events.find({})
	for doc in docs:
		doc.pop('_id')
		doc['startdate'] = doc['start'].date()
		doc['start'] = doc['start'].time()
		doc['end'] = doc['end'].time()
		doc.pop('volunteers')
		doc.pop('donations')
		doc.pop('volunteers_needed')
		doc['start'] = doc['start'].strftime("%H:%M")
		d = datetime.datetime.strptime(doc['start'], "%H:%M")
		doc['start'] = d.strftime("%I:%M %p")
		doc['end'] = doc['end'].strftime("%H:%M")
		d = datetime.datetime.strptime(doc['end'], "%H:%M")
		doc['end'] = d.strftime("%I:%M %p")
		data.append(doc)
	return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


from datetime import timedelta

def edit(request):
	post = request.POST.dict()
	start = datetime.datetime.strptime(post['startdate']+ " " + post['start'], "%Y-%m-%d %H:%M %p")
	end = datetime.datetime.strptime(post['startdate']+ " " + post['end'], "%Y-%m-%d %H:%M %p")
	if "PM" in post['start'] and "12" not in post['start']:
		start = start + timedelta(hours=12)
	if "PM" in post['end'] and "12" not in post['end']:
		end = end + timedelta(hours=12)

	now = datetime.datetime.now()
	updated = post.copy()
	updated['start'] = start
	updated['end'] = end
	updated.pop('startdate')
	updated.pop('id')
	if end < now:
		return HttpResponse("False")
	conn = get_mongo()
	filter = {'id': int(post['id'])}
	new_vals = {'$set': updated}
	conn.nonprofit.events.update_one(filter, new_vals)
	return HttpResponse("Good")

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


def delete_event(request):
	try:
		conn = get_mongo()
		doc = conn.nonprofit.events.find_one({'id': int(request.POST['id'])})
		dt = datetime.datetime.now()
		if doc['end'] < dt:
			return HttpResponse("error")
		conn.nonprofit.cancelled_events.insert(doc)
		conn.nonprofit.events.remove({'id': int(request.POST['id'])})
	except Exception as e:
		return HttpResponse('error')
	return HttpResponse("Good")

def delete(request):
	try:
		conn = get_mongo()
		conn.nonprofit.events.remove({'id': int(request.POST['models[0][id]'])})
	except Exception as e:
		return HttpResponse({'error': e})
	return HttpResponse({'success': 'true'})

def index(request):
	return render(request, 'index.html')

