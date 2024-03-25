from django.views.generic import ListView, DetailView, TemplateView
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views import View

class Bloglist(ListView):
    model = Post
    template_name = 'blog/home.html'

class BlogTaskslView(TemplateView):
    model = Post
    template_name = 'blog/tasks.html'

class BlogProjectslView(TemplateView):
    model = Post
    template_name = 'blog/projects.html'

class AboutPageView(View):
    template_name = 'blog/about.html'
    data = [
        {'Имя': 'Азаров Владимир',
         'Роль': 'Информация: Оператор FPV-дронов, который способен создать невероятные и захватывающие видеоролики с воздушной перспективы.',
         'Цитата': 'Главная цитата: "Начальнику второго отделения прибыть в 314 кабинет" - это не просто фраза, это наше девиз, который символизирует нашу организованность и четкость в работе.',
         'Фото': 'blog/img/azarov.jpg'},
        {'Имя': 'Зюков Антон',
         'Роль': 'Информация: Оператор "евреев" - Его уникальная способность искусно торговать, находя лучшие предложения для нашей команды.',
         'Цитата': 'Главная цитата: "Как прогреть гоя?" - эта загадочная фраза стала нашим лозунгом, отражающим нашу способность преодолевать любые трудности.',
         'Фото': 'blog/img/zyukov.jpg'},
        {'Имя': 'Петрухин Владислав',
         'Роль': 'Информация: -',
         'Цитата': 'Главная цитата: -',
         'Фото': 'blog/img/petrukhin.jpg'}
    ]
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        page_number = request.GET.get('page')
        paginator = Paginator(self.data, self.paginate_by)

        try:
            page_data = paginator.page(page_number)
        except PageNotAnInteger:
            page_data = paginator.page(1)
        except EmptyPage:
            page_data = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'page_data': page_data})

class ContactsPageView(TemplateView):
    template_name = 'blog/contacts.html'

