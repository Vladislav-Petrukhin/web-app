from django.views.generic import ListView, DetailView, TemplateView
from .models import Post

class Bloglist(ListView):
    model = Post
    template_name = 'blog/home.html'

class BlogTaskslView(TemplateView):
    model = Post
    template_name = 'blog/tasks.html'

class BlogProjectslView(TemplateView):
    model = Post
    template_name = 'blog/projects.html'

class AboutPageView(TemplateView):
    template_name = 'blog/about.html'

class ContactsPageView(TemplateView):
    template_name = 'blog/contacts.html'