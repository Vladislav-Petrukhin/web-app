from django.urls import path
from .views import Bloglist, BlogProjectslView, AboutPageView, BlogTaskslView, ContactsPageView, ajax_register, ajax_login, logout_user, translate_text

urlpatterns = [
    path('projects/', BlogProjectslView.as_view(), name='projects'),
    path('tasks/', BlogTaskslView.as_view(), name='tasks'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('ajax/register/', ajax_register, name='ajax_register'),
    path('ajax/login/', ajax_login, name='ajax_login'),
    path('logout/', logout_user, name='logout'),
    path('translate/', translate_text, name='translate'),
    path('', Bloglist.as_view(), name='home'),
]



