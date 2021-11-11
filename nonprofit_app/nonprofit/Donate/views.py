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


def get_all_events(request):
	data = []
	conn = get_mongo()
	docs = conn.nonprofit.events.find({})
	dt = datetime.datetime.now()
	for doc in docs:
		doc.pop('_id')
		doc.pop('volunteers')
		doc.pop('donations')
		doc.pop('volunteers_needed')
		doc.pop('description')
		if doc['end'] > dt:
			data.append(doc)
	return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))
