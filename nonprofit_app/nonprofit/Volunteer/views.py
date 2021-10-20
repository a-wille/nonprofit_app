from nonprofit.extra.view_helper import get_mongo
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json

def get_volunteer_events(request):
    data = []
    conn = get_mongo()
    docs = conn.nonprofit.volunteer.find({})
    for doc in docs:
        doc['time_range'] = ""
        data.append(doc)

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

def get_all_events(request):
    data = []
    conn = get_mongo()
    docs = conn.nonprofit.events.find({})
    for doc in docs:
        doc.pop('_id')
        doc.pop('donations')
        doc.pop('volunteers')
        data.append(doc)
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))