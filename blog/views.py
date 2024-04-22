from django.views.generic import ListView, TemplateView
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
import json
import pymysql.cursors
from blog.neural_networks.neural_functions import train_and_predict


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


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password1')
        password2 = data.get('password2')

        if not (username and email and password and password == password2):
            return JsonResponse(
                {'status': 'error', 'message': 'Необходимо заполнить все поля и убедиться, что пароли совпадают.'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Пользователь с таким именем уже существует.'})
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Регистрация прошла успешно!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'}, status=400)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Вы успешно вошли в систему.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Неверное имя пользователя или пароль.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'}, status=400)


@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Вы успешно вышли из системы.'})


def neural_networks(request):
    if request.method == 'POST':
        mae, mse, rmse = train_and_predict()

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='admin',
                                     database='hh',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO model_metrics (mae, mse, rmse) VALUES (%s, %s, %s)"
                cursor.execute(sql, (mae, mse, rmse))
            connection.commit()

        return JsonResponse({
            'trained': "Модель успешно обучена! Метрика сохранена в БД."
        })
    else:
        return render(request, 'blog/neural_networks.html')

@csrf_exempt
def fetch_predictions(request):
    if request.method == 'POST':
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='admin',
                                     database='hh',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT mae, mse, rmse FROM model_metrics ORDER BY id DESC LIMIT 1"
                cursor.execute(sql)
                result = cursor.fetchone()

            if result:
                return JsonResponse({
                    'mse': result['mse'],
                    'mae': result['mae'],
                    'rmse': result['rmse']
                })
            else:
                return JsonResponse({'error': 'Нет таких данных ;('}, status=404)

        finally:
            connection.close()
    else:
        return JsonResponse({'error': 'Что-то пошло не так :('}, status=400)

