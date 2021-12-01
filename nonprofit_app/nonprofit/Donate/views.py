import datetime
import json
import pytz
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


def get_all_events(request):
	data = []
	conn = get_mongo()
	docs = conn.nonprofit.events.find({})
	dt = datetime.datetime.now(tz=pytz.timezone("US/Central"))
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


def get_my_donations(request):
	conn = get_mongo()
	data = []
	docs = conn.nonprofit.donations.find({'user': request.user.email})
	for doc in docs:
		if doc['event_id'] != -1:
			e = conn.nonprofit.events.find_one({'id': int(doc['event_id'])})
			doc['event_id'] = e['name']
		else:
			doc['event_id'] = "N/A"
		doc.pop('_id')
		doc.pop('user')
		doc.pop('donation_id')
		doc['dark'] =pytz.timezone("UTC").localize(doc['date']).astimezone(pytz.timezone("US/Central")).strftime("%d/%m/%y")
		doc['darktime'] = pytz.timezone("UTC").localize(doc['date']).astimezone(pytz.timezone("US/Central")).strftime("%H:%M")
		doc.pop('date')
		data.append(doc)
	return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))