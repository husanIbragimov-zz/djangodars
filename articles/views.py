from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from random import randint

from django.urls import reverse

from .models import Article
from django.contrib import messages
from .forms import ArticleCreateForm
from django.db.models import Q


def _home_view(request):
    RANDOM_ID = randint(1, 3)
    article_obj = Article.objects.get(id=RANDOM_ID)
    TITLE_STRING = f'<h2>{article_obj.title} ID: {RANDOM_ID}</h2>'
    CONTENT_STRING = f'<p>{article_obj.content}</p>'

    HTML_STRING = TITLE_STRING + CONTENT_STRING

    return HttpResponse(HTML_STRING)


@login_required(login_url='/login')
def home_view(request):
    object_list = Article.objects.all()

    context = {
        'object_list': object_list
    }

    return render(request, 'articles/index.html', context)


@login_required
def my_articles_view(request):
    object_list = Article.objects.filter(author=request.user)

    context = {
        'object_list': object_list
    }
    return render(request, 'articles/index.html', context)


# @login_required(login_url='/login')
def article_detail_view(request, slug):
    obj = Article.objects.get(slug=slug)
    # year = obj.created_at.year
    # month = obj.created_at.month
    # day = obj.created_at.day
    # qs1 = Article.objects.filter(title__contains="HELLO world")
    # qs2 = Article.objects.filter(title__icontains="HELLO world")
    # qs3 = Article.objects.filter(title__exact="HELLO world")
    # qs4 = Article.objects.filter(title__iexact="HELLO world")
    # qs5 = Article.objects.filter(title__startswith="HELLO world")
    # qs6 = Article.objects.filter(title__endswith="HELLO world")
    # ids = [7,8,9]
    # qs7 = Article.objects.filter(id__in=ids)
    # print("111 ", qs7)

    context = {
        'object': obj
    }

    return render(request, 'articles/detail.html', context)


# @login_required(login_url='/login')
def search_article_view(request):
    obj = None
    if request.method == "POST":
        # lookup = Q(title__icontains=query) | Q(title__icontains=query)
        query = request.POST.get('q')
        try:
            obj = Article.objects.search(query)
            if not obj:
                messages.error(request, 'Siz qidirgan article topilmadi.!')
        except:
            redirect('articles/search')

    context = {
        'object': obj
    }
    return render(request, 'articles/search.html', context)


@login_required
def create_article_view(request, ralse=None):
    context = {

    }
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            obj = Article.objects.create(title=title, content=content)
            context['obj'] = obj
        else:
            messages.error(request, 'title yoki content yozilmagan')

        print('Title: ', title)
        print('Content: ', content)

    return render(request, 'articles/create.html', context)


@login_required(login_url='/login')
def article_create_form_view_old(request):
    form = ArticleCreateForm()
    obj = None
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            obj = Article.objects.create(title=title, content=content)
    context = {
        'form': form,
        'obj': obj
    }
    return render(request, 'articles/create.html', context)


@login_required
def article_create_form_view_old_(request):
    form = ArticleCreateForm()
    obj = None
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'form': form,
        'obj': obj
    }
    return render(request, 'articles/create.html', context)


@login_required
def article_create_form_view(request):
    form = ArticleCreateForm()
    obj = None
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            form.save_m2m()
    context = {
        'form': form,
        'obj': obj
    }
    return render(request, 'articles/create.html', context)


@login_required
def article_update_view(request, slug):
    obj = get_object_or_404(Article, slug=slug)
    form = ArticleCreateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(reverse('article_detail_view', kwargs={'slug': slug}))
    context = {
        'form': form,
        'object': obj
    }
    return render(request, 'articles/update.html', context)


@login_required
def article_delete_view(request, slug):
    obj = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('/articles')
    return render(request, 'articles/delete.html')

