from django.urls import path,include
from blood_donation_app import views
from .views import *

urlpatterns=[
    path("",views.index,name="index"),
    path("add_donor/",views.add_donor,name="add_donor"),
    path('add_bloodbank/', views.add_bloodbank, name='add_bloodbank'),
    path('donorlist/',views.donorlist,name="donorlist"),
    path('admin_login_view/',views.admin_login,name="admin_login"),
    path('delete_donor/<str:donor_email>/',views.delete_donor,name="delete_donor"),
    path('edit_donor/<str:donor_email>/', views.edit_donor, name="edit_donor"),
    path('donation_records/',views.donation_record,name="donation_record"),
    path('bloodbanklist/',views.bloodbanklist,name="bloodbanklist"),
    path('admin_login/',views.admin_login_view,name="admin_login_view"),
    path('register/',RegisterUser.as_view()),
    path('orm/', my_view, name='my_view'),
    path('statistics/',views.display_blood_donation_statistics,name="display_blood_donation_statistics"),
]   