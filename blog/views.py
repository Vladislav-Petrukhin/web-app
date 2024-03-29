from django.views.generic import ListView, TemplateView
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from googletrans import Translator, constants
import json

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

@csrf_exempt
def ajax_register(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirmPassword')

    if password == confirm_password:
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'failed', 'error': 'Пароли не совпадают'})


@csrf_exempt
def ajax_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'failed', 'error': 'Неверный логин или пароль'})

def logout_user(request):
    logout(request)

    return redirect('home')

@csrf_exempt
@require_POST
def translate_text(request):
    data = json.loads(request.body)
    text = data.get('text', "")
    dest_lang = data.get('target', 'ru')

    translator = Translator()

    try:
        translation = translator.translate(text, dest=dest_lang)
        return JsonResponse({'translation': translation.text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




