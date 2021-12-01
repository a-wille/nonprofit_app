from django.urls import path
from . import views

urlpatterns = [
	# path('GetEvents/', views.get_volunteer_events),
	path('GetAllEvents/', views.get_all_events),
	path('GetMyDonations/', views.get_my_donations)
	# path('EventDonation/', views.donate_to_event),
	# path('UnrestrictedDonation/', views.unrestricted_donation)
	# path('SignUp/', views.sign_up)
]