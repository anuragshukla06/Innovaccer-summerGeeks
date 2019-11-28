from django.urls import path
from. import views
#TODO: spell Innovaccer correctly and remove this todo
urlpatterns = [
    path('', views.home, name='home'),
    path('registerHost', views.host_registration, name="host_register_url"),
    path('showMeetings', views.showMeetings, name='check_in_url'),
    path('guestRegForm/<int:meeting_pk>', views.guestRegForm, name='guestRegForm_url'),
    path('checkout', views.check_out, name='check_out_url'),
    path('manage/<email>/<int:token>', views.manage, name='manage_url'),
    path('kickoutGuest/<email>/<int:token>/<int:guest_pk>', views.kickoutGuest, name='kick_out_guest_url'),
    path('manageForm', views.manageForm, name='manage_form_url'),
]