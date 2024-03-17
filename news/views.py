from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .models import Category
from .filters import PostFilter
from .forms import PostForm
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache


# Категории отражаются на главной странице
class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'flatpages/news/home.html'
    context_object_name = 'category'


# Список новостей отражается на своей странице


class PostList(ListView):
    model = Post
    ordering = 'header'
    template_name = 'flatpages/news/news.html'
    context_object_name = 'news'
    paginate_by = 25

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['next_sale'] = "Все актуальные новости у нас!"
        context['filterset'] = self.filterset
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'flatpages/news/search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/news/post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class PostCreate(CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == "/article/create/":
            post.type = 'AR'
        post.save()
        return super().form_valid(form)


# Добавляем представление для изменения товара.
class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = '/post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/news/post_delete.html'
    success_url = reverse_lazy('news')


@login_required
class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)