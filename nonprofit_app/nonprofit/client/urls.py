from django.urls import path
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
	path('check_login/', views.check_login),
	path('create_account/', views.create_account),
	path('logout/', views.my_logout)
]


