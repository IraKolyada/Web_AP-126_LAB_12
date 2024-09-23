from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Spanner, Category, TagPost

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]

data_dp = [
    {'id': 1, 'title': 'Эй, Арнольд!(Hey Arnold!)','content':
     '''<h1>Главный герой сериала — школьник Арнольд</h1>, живущий со своими дедушкой Филом и бабушкой Гертрудой в пансионе «Сансет-Армз», владельцами которого они являются. 
     Его родители Стелла и Майлз пропали, когда принимали участие в спасательной операции в далекой стране. Место действия — вымышленный город Хиллвуд.''','is_publish':True},
    {'id': 2, 'title': 'Утиные истории (DuckTales)', 'content':
        'Мультсериал 1987 года выпуска','is_publish':False},
    {'id': 3, 'title': 'Черный Плащ (Darkwing Duck)', 'content':
        'Мультсериал 1991 года выпуска','is_publish':True},
]

cats_db = [
    {'id': 1, 'name': 'Мультсериалы'},
    {'id': 2, 'name': 'Сериалы'},
    {'id': 3, 'name': 'Другое'},
]

# Create your views here.
class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
def index(request):
    posts = Spanner.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Spanner.published.all(),
        'cat_selected': 0,
    }
    return render(request, 'spanner/index.html', context = data)

def show_post(request, post_slug):
    post = get_object_or_404(Spanner, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'spanner/post.html', context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug = cat_slug)
    posts = Spanner.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'spanner/index.html', context= data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Spanner.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'spanner/index.html',context=data)

def about(reqest):
    data = {'title' : 'О нас'}
    return render(reqest,'spanner/about.html', {'title': 'О сайте','menu': menu})
def addpage(request):
    return HttpResponse("Добавление статьи")
def contact(request):
    return HttpResponse("Обратная связь")
def login(request):
    return HttpResponse("Авторизация")
