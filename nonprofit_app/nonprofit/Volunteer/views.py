import datetime

import pytz

from nonprofit.extra.view_helper import get_mongo
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json


def cancel(request):
    conn = get_mongo()
    doc = conn.nonprofit.events.find_one({'id': int(request.POST.get('id'))})
    new_volunteers = doc['volunteers'].copy()
    new_volunteers.pop(new_volunteers.index(request.user.email))
    filter = {'id': int(request.POST.get('id'))}
    new_vals = {"$set": {'volunteers': new_volunteers}}
    conn.nonprofit.events.update_one(filter, new_vals)

    filter = {'id': request.user.email}
    events = conn.nonprofit.users.find_one({'id': request.user.email})['events'].copy()
    events.pop(int(events.index(int(request.POST.get('id')))))
    new_vals = {"$set": {'events': events}}
    conn.nonprofit.users.update_one(filter, new_vals)
    return HttpResponse({'success': 'true'})


def sign_up(request):
    conn = get_mongo()
    doc = conn.nonprofit.events.find_one({'id':int(request.POST.get('id'))})
    if len(doc['volunteers']) >= int(doc['volunteers_needed']):
        return HttpResponse(json.dumps({'success': 'false'}))

    #check that dates don't overlap
    events = conn.nonprofit.users.find_one({'id': request.user.email})['events'].copy()
    for e in events:
        d = conn.nonprofit.events.find_one({'id': int(e)})
        start1 = d['start']
        end1 = d['end']
        start2 = doc['start']
        end2 = doc['end']
        if start1 <= end2 and start2 <= end1:
            return HttpResponse(json.dumps({'success': 'false'}))

    new_volunteers = doc['volunteers'].copy()
    new_volunteers.append(request.user.email)
    filter = {'id': int(request.POST.get('id'))}
    new_vals = { "$set": {'volunteers': new_volunteers}}
    conn.nonprofit.events.update_one(filter, new_vals)

    filter = {'id': request.user.email}
    events.append(int(request.POST.get('id')))
    new_vals = {"$set": {'events': events}}
    conn.nonprofit.users.update_one(filter, new_vals)
    return HttpResponse({'success': 'true'})


def get_volunteer_events(request):
    data = []
    conn = get_mongo()

    doc = conn.nonprofit.users.find_one({'id': request.user.email})
    dt = datetime.datetime.now(tz=pytz.timezone("US/Central"))
    event_list = []
    for e in doc['events']:
        event_list.append(e)
    for e in event_list:
        doc = conn.nonprofit.events.find_one({'id': e})
        doc.pop('_id')
        doc.pop('donations')
        doc['volunteers_needed'] = int(doc['volunteers_needed']) - len(doc['volunteers'])
        doc.pop('volunteers')
        doc['endnew'] = pytz.timezone("US/Central").localize(doc['end'])
        if doc['endnew'] > dt:
            data.append(doc)
    # data.insert(0, {'data': 'MY EVENTS'})
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

def get_all_events(request):
    #kinda a lie, returns all events that the user isn't actively signed up for
    data = []
    conn = get_mongo()
    dt = datetime.datetime.now(tz=pytz.timezone("US/Central"))
    docs = conn.nonprofit.events.find({})
    for doc in docs:
        already_volunteering = 0
        for v in doc['volunteers']:
            if v == request.user.email:
                already_volunteering = 1
        if not already_volunteering:
            doc.pop('_id')
            doc.pop('donations')
            doc['volunteers_needed'] = int(doc['volunteers_needed']) - len(doc['volunteers'])
            doc.pop('volunteers')
            doc['endnew'] = pytz.timezone("US/Central").localize(doc['end'])
            if doc['endnew'] > dt and doc['volunteers_needed'] != 0:
                data.append(doc)
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))