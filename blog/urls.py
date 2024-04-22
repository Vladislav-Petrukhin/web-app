from django.urls import path
from .views import Bloglist, BlogProjectslView, AboutPageView, BlogTaskslView, ContactsPageView, register, login_user, logout_user, neural_networks, fetch_predictions

urlpatterns = [
    path('projects/', BlogProjectslView.as_view(), name='projects'),
    path('tasks/', BlogTaskslView.as_view(), name='tasks'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('neural_networks/', neural_networks, name='neural_networks'),
    path('fetch_predictions/', fetch_predictions, name='fetch_predictions'),
    path('', Bloglist.as_view(), name='home'),
]



