import uuid

from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Spanner, Category, TagPost, UploadFiles
from .utils import DataMixin


# Create your views here.
class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
# def index(request):
#     posts = Spanner.published.all()
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': Spanner.published.all(),
#         'cat_selected': 0,
#     }
#     return render(request, 'spanner/index.html', context = data)

class SpannerHome(DataMixin, ListView):
    # model = Spanner
    template_name = 'spanner/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     #'posts': Spanner.published.all().select_related('cat'),
    #     'cat_selected': 0,
    # }
    def get_queryset(self):
        return Spanner.published.all().select_related('cat')

    # def get_context_data(self, *, object_list=None **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Spanner.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context

# def show_post(request, post_slug):
#     post = get_object_or_404(Spanner, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#
#     return render(request, 'spanner/post.html', context=data)


class ShowPost(DataMixin, DetailView):
    model = Spanner
    template_name = 'spanner/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=context['post'])
    def get_object(self, queryset=None):
        return get_object_or_404(Spanner.published, slug=self.kwargs[self.slug_url_kwarg])


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug = cat_slug)
#     posts = Spanner.published.filter(cat_id=category.pk)
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'spanner/index.html', context= data)

class SpannerCategory(DataMixin, ListView):
    template_name = 'spanner/index.html'
    context_object_name = 'posts'
    allow_empty = False
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return  self.get_mixin_context(context, title='Категория - ' + cat.name,
                                       cat_selected=cat.id,)
    def get_queryset(self):
        return Spanner.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Spanner.Status.PUBLISHED)
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#     return render(request, 'spanner/index.html',context=data)

class TagPostList(DataMixin, ListView):
    template_name = 'spanner/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Spanner.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

# def handle_uploaded_file(f):
#     name = f.name
#     ext = ''
#     if '.' in name:
#         ext = name[name.rindex('.'):]
#         name = name[:name.rindex('.')]
#
#     suffix = str(uuid.uuid4())
#     with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
def about(request):
    contact_list = Spanner.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'spanner/about.html',
                  {'page_obj': page_obj, 'title': 'О сайте'})

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#
#     data = {'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#     }
#     return render(request, 'spanner/addpage.html', data)

# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#
#         data = {'menu': menu,
#                 'title': 'Добавление статьи',
#                 'form': form
#                 }
#         return render(request, 'spanner/addpage.html', data)
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         data = {'menu': menu,
#                 'title': 'Добавление статьи',
#                 'form': form
#                 }
#         return render(request, 'spanner/addpage.html', data)

class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'spanner/addpage.html'
    title_page = 'Добавление страны'

class UpdatePage(DataMixin, UpdateView):
    model = Spanner
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'spanner/addpage.html'
    success_url = reverse_lazy('home')


def contact(request):
    return HttpResponse("Обратная связь")
def login(request):
    return HttpResponse("Авторизация")
