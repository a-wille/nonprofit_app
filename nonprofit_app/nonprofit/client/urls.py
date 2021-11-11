from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.index),
	path('events', views.events),
	path('home', views.home),
	path('donate', views.donate),
	path('volunteer', views.volunteer),
	path('about', views.about),
	path('login', views.login),
	path('create', views.account_view),
	path('donate_unrestricted', views.donation_unrestricted),
	re_path(r'donate_restricted/.*$', views.donation_restricted),
	path('make_restricted_donation/', views.make_restricted_donation),
	path('make_unrestricted_donation/', views.make_unrestricted_donation),
	path('check_login/', views.check_login),
	path('create_account/', views.create_account),
	path('logout/', views.my_logout)
]


