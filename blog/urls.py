from django.urls import path
from .views import Bloglist, BlogProjectslView, AboutPageView, BlogTaskslView, ContactsPageView

urlpatterns = [
    path('projects/', BlogProjectslView.as_view(), name='projects'),
    path('tasks/', BlogTaskslView.as_view(), name='tasks'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('', Bloglist.as_view(), name='home')
]



