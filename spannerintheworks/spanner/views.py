import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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


class SpannerHome(DataMixin, ListView):
    # model = Spanner
    template_name = 'spanner/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Spanner.published.all().select_related('cat')



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

@login_required
def about(request):
    contact_list = Spanner.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'spanner/about.html',
                  {'page_obj': page_obj, 'title': 'О сайте'})



class AddPage(LoginRequiredMixin,DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'spanner/addpage.html'
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

class UpdatePage(DataMixin, UpdateView):
    model = Spanner
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'spanner/addpage.html'
    success_url = reverse_lazy('home')


def contact(request):
    return HttpResponse("Обратная связь")
def login(request):
    return HttpResponse("Авторизация")
