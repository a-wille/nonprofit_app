from django.urls import path, re_path
from . import views

urlpatterns = [
	path('ViewAll/', views.get_all),
	path('Edit/', views.edit),
	path('Create/', views.create),
	path('Delete/', views.delete),
	path('', views.index),
]
