from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewsForm
from .models import News, Category
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, ContactForm
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Successfully registered!')
            return redirect('home'
                            '')
        else:
            messages.error(request, 'Error registration')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('home')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                'alisherrakhimov1997@gmail.com',
                ['rakhimovalisher@mail.ru'],
                fail_silently=False
            )
            if mail:
                messages.success(request, 'Successfully sent!')
                return redirect('contact')
            else:
                messages.error(request, 'Error on sent')
        else:
            messages.error(request, 'Not valid data')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', {'form': form})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    extra_context = {'title': 'Glavnaya'}

    mixin_prop = 'Hello world'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Main page')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    allow_empty = False  # 404 if not found or empty

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context


class ViewNews(MyMixin, DetailView):
    model = News
    # pk_url_kwarg = 'news_id'
    template_name = 'news/view_news.html'

    context_object_name = 'item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = reverse_lazy('home')
    # raise_exception = True
    # success_url = reverse_lazy('home')

# def index(request):
#     # news = News.objects.order_by('-created_at')
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'News list'
#     }
#     return render(request=request, template_name='news/index.html', context=context)


# def get_category(request, category_id):
#     # category = Category.objects.get(pk=category_id)
#     category = get_object_or_404(Category, pk=category_id)
#     news = News.objects.filter(category_id=category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request=request, template_name='news/category.html', context=context)


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news_item = News.objects.create(**form.cleaned_data)
#             news_item = form.save()
#             return redirect(news_item)
#     else:
#         form = NewsForm()
#
#     return render(request, 'news/add_news.html', {'form': form})
