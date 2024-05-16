

from django.contrib import admin
from django.urls import path,include
from home.views import index,list_engineers,search_engineers,list_user,edit_user,set_availability,Login_View,log_out
from .views import create_user,create_engineer,edit_engineer,log_in,delete_engineer,delete_user
from .views import engr_available_today,engr_available_today_jobtype,engr_available_weekly
from .profile import engineer_profile,add_availability,edit_availability,delete_availability

urlpatterns = [
    
    path('', index,name='dashboard'),
    # path('login/', Login_View.as_view(),name='login'),
    path('login/', log_in,name='login'),
    path('logout/', log_out,name='logout'),

    # add Edit Engineers
    path('create_engineer/', create_engineer,name='addengineer'),
    path('edit_engineer/<int:id>', edit_engineer,name='editengineer'),
    path('delete_engineer/<int:id>', delete_engineer,name='deleteengineer'),
    path('list_engineers/', list_engineers,name='listengineers'),
    path('set_availability/<int:id>', set_availability,name='setavailability'),
    path('search_engineers/', search_engineers,name='searchengineers'),

    path('engineers_today/', engr_available_today,name='engrstoday'),
    path('engineers_today_jobtype/', engr_available_today_jobtype,name='engrstodayjobtype'),
    path('engr_available_weekly/', engr_available_weekly,name='engrstodayjobtype'),

    # users
    path('list_user/', list_user,name='listusers'),
    path('edit_user/<int:id>', edit_user,name='edituser'),
    path('delete_user/<int:id>', edit_user,name='deleteuser'),
    path('create_user/', create_user, name='createuser'),

# Engineer Profile
    path('engr_profile/', engineer_profile, name='engrprofile'),
    path('add_availability/', add_availability, name='addavailability'),
    path('edit_availability/<int:id>', edit_availability, name='editavailability'),
    path('delete_availability/<int:id>', delete_availability, name='deleteavailability'),



]
