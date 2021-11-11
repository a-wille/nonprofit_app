import datetime

from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, logout
from nonprofit.client.models import User
from django.contrib.auth import login as login_django
from nonprofit.extra.view_helper import get_mongo
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect


def index(request):
	return render(request, 'index.html')

def events(request):
	return render(request, 'events.html')

def donate(request):
	return render(request, 'donate.html')

def volunteer(request):
	return render(request, 'volunteer.html')

def about(request):
	return render(request, 'about.html')

def login(request):
	return render(request, 'login.html')

def home(request):
	return render(request, 'home.html')

def account_view(request):
	return render(request, 'account_creation.html')

def donation_unrestricted(request):
	return render(request, 'unrestricted_donation.html')


def remove_substring_from_string(s, substr):
	i = 0
	while i < len(s) - len(substr) + 1:
		if s[i:i + len(substr)] == substr:
			break
		i += 1
	else:
		return s
	return s[:i] + s[i + len(substr):]

def donation_restricted(request):
	event_id = int(remove_substring_from_string(request.path, '/client/donate_restricted/'))
	return render(request, 'restricted_donation.html', context={'event_id': event_id})


def make_restricted_donation(request):
	conn = get_mongo()
	greatest_id = 0
	all = conn.nonprofit.donations.find({})
	for a in all:
		if a['donation_id'] > greatest_id:
			greatest_id = a['donation_id']
	post = request.POST.dict()
	doc = {'donation_id': greatest_id +1, 'date': datetime.datetime.now(), 'user': request.user.email, 'amount': post['currency'], 'type': 'restricted', 'event_id': post['id']}
	conn.nonprofit.donations.insert(doc)
	return HttpResponse({'success': 'true'})

def make_unrestricted_donation(request):
	conn = get_mongo()
	greatest_id = 0
	all = conn.nonprofit.donations.find({})
	for a in all:
		if a['donation_id'] > greatest_id:
			greatest_id = a['donation_id']
	post = request.POST.dict()
	doc = {'donation_id': greatest_id +1, 'date': datetime.datetime.now(), 'user': request.user.email, 'amount': post['currency'], 'type': 'unrestricted', 'event_id': -1}
	conn.nonprofit.donations.insert(doc)
	return HttpResponse({'success': 'true'})

def create_account(request):
	user = User.objects.create(username=request.POST.get('user'),
							   email=request.POST.get('email'),
							   password=request.POST.get('pass'),
							   )
	conn = get_mongo()
	doc = {'user': user.username, 'id': user.email, 'events': [], 'donations': [], 'volunteer': request.POST.get('volunteer'), 'donor': request.POST.get('donor')}
	conn.nonprofit.users.insert(doc)
	if request.POST.get('donor') == 'true':
		donor_group = Group.objects.get(name='donor')
		donor_group.user_set.add(user)

	if request.POST.get('volunteer') == 'true':
		v_group = Group.objects.get(name='volunteer')
		v_group.user_set.add(user)

	user.is_active = True
	user.set_password(user.password)
	user.save()
	user = authenticate(username=request.POST.get('user'), password=request.POST.get('pass'))

	if user:
		login_django(request, user)
		return HttpResponse({'success': True})


def check_login(request):
	username = request.POST.get('user')
	password = request.POST.get('pass')
	user = authenticate(username=username, password=password)

	if user:
		login_django(request, user)
		return HttpResponse({'success': True})
	return HttpResponse({'success': False})

def my_logout(request):
	logout(request)
	return HttpResponse({'success': True})
