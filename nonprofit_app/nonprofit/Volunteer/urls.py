from django.urls import path
from . import views

urlpatterns = [
	path('GetEvents/', views.get_volunteer_events),
	path('GetAllEvents/', views.get_all_events),
	path('SignUp/', views.sign_up),
	path('Cancel/', views.cancel)
]