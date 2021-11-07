import datetime
from nonprofit.extra.view_helper import get_mongo
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json

def sign_up(request):
    conn = get_mongo()
    doc = conn.nonprofit.events.find_one({'id':int(request.POST.get('id'))})
    if len(doc['volunteers']) >= int(doc['volunteers_needed']):
        return HttpResponse(json.dumps({'success': 'false'}))
    new_volunteers = doc['volunteers'].copy()
    new_volunteers.append(request.user.email)
    filter = {'id': int(request.POST.get('id'))}
    new_vals = { "$set": {'volunteers': new_volunteers}}
    conn.nonprofit.events.update_one(filter, new_vals)

    filter = {'id': request.user.email}
    events = conn.nonprofit.users.find_one({'id': request.user.email})['events'].copy()
    events.append(int(request.POST.get('id')))
    new_vals = {"$set": {'events': events}}
    conn.nonprofit.users.update_one(filter, new_vals)
    return HttpResponse({'success': 'true'})

def get_volunteer_events(request):
    data = []
    conn = get_mongo()
    doc = conn.nonprofit.users.find_one({'id': request.user.email})
    dt = datetime.datetime.now()
    event_list = []
    for e in doc['events']:
        event_list.append(e)
    for e in event_list:
        doc = conn.nonprofit.events.find_one({'id': e})
        date = doc['start'].strftime("%m/%d/%Y")
        start = doc['start'].strftime("%H:%M")
        end = doc['end'].strftime("%H:%M")
        m = "__________________________________\n{} {} - {}: {}\n{} \n Location: {}\n".format(date, start, end, doc['name'], doc['description'], doc['location'])
        if doc['end'] > dt:
            data.append({'data': m})
    data.insert(0, {'data': 'MY EVENTS'})
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

def get_all_events(request):
    #kinda a lie, returns all events that the user isn't actively signed up for
    data = []
    conn = get_mongo()
    dt = datetime.datetime.now()
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
            if doc['end'] > dt:
                data.append(doc)
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))