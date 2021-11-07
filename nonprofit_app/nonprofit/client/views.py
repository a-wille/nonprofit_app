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

def donation_view(request):
	return render(request, 'unrestricted_donation.html')

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
