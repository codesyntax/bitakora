from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from bitakora.base.models import Article, Blog
from bitakora.base.forms import ArticleForm, BlogForm, CommentForm, AnonimousCommentForm
from bitakora.utils.images import handle_uploaded_file
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

def blog_index(request,slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render_to_response('base/blog_index.html', locals(), context_instance=RequestContext(request))

def article(request,blogslug,slug):
    article = get_object_or_404(Article, blog__slug=blogslug,slug=slug)
    blog = article.blog
    if request.user.is_authenticated():
        form = CommentForm()
    else:
        form = AnonimousCommentForm()
    return render_to_response('base/article.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/users/login')
def add_article(request,blogslug):
    blog = get_object_or_404(Blog, slug=blogslug, user=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if request.FILES.get('featured_image',''):
            format = request.FILES.get('featured_image','').name.split('.')[-1]
            if format.lower().strip() not in (u'jpg',u'png',u'gif'):
                form.add_error('featured_image',_('Invalid image format. Please, change the format!'))
        if form.is_valid():
            article = form.save(commit=False)
            article.slug = slugify(article.title)
            if request.FILES.get('featured_image',''):
                article.featured_image = handle_uploaded_file(request.FILES['featured_image'], request.user)
            article.author = request.user
            article.blog = blog
            article.publish_date = datetime.now()
            article.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('article', kwargs={'blogslug': blogslug,'slug': article.slug}))
    else:
        form = ArticleForm()
    return render_to_response('base/add_article.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/users/login')
def edit_article(request,blogslug,slug):
    article = get_object_or_404(Article, blog__slug=blogslug,slug=slug,blog__user=request.user)
    blog = article.blog
    if request.method == 'POST':
        form = ArticleForm(request.POST,instance=article)
        if request.FILES.get('featured_image',''):
            format = request.FILES.get('featured_image','').name.split('.')[-1]
            if format.lower().strip() not in (u'jpg',u'png',u'gif'):
                form.add_error('featured_image',_('Invalid image format. Please, change the format!'))
        if form.is_valid():
            article = form.save(commit=False)
            if request.FILES and request.FILES.get('featured_image',''):
                article.featured_image = handle_uploaded_file(request.FILES['featured_image'], request.user)
            article.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('article', kwargs={'blogslug': blogslug,'slug': article.slug}))
    else:
        form = ArticleForm(instance=article)
    return render_to_response('base/edit_article.html', locals(), context_instance=RequestContext(request))

def new_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(blog.name)
            if request.FILES.get('header_image',''):
                blog.header_image = handle_uploaded_file(request.FILES['header_image'], request.user)
            blog.user = request.user
            blog.save()
            return HttpResponseRedirect(reverse('blog_index', kwargs={'slug': blog.slug}))
    else:
        form = BlogForm()
    return render_to_response('base/new_blog.html', locals(), context_instance=RequestContext(request))


def add_comment(request, blogslug, slug):
    user = request.user
    article = get_object_or_404(Article, blog__slug=blogslug, slug=slug)
    if request.method == 'POST':
        if user.is_authenticated():
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.parent = article
                comment.publish_date = datetime.now()
                comment.save()
        else:
            form = AnonimousCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.parent = article
                comment.ip_address = request.META.get("REMOTE_ADDR", None)
                comment.publish_date = datetime.now()
                comment.save()
    else:
        if user.is_authenticated():
            form = CommentForm()
        else:
            form = AnonimousCommentForm()
    return HttpResponseRedirect(reverse('article', kwargs={'blogslug': blogslug,'slug': article.slug}))