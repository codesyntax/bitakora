from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from bitakora.base.models import Article, Category, Blog, Comment, External_link
from voting.models import Vote
import json
from django.views.generic import View
from bitakora.utils.images import handle_uploaded_file
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Context
from django.views.decorators.cache import cache_page

IMAGE_SIZE = 5242880

SECTIONS = (
    (1, _('Top stories')),
    (2, _('Bookmarks')),
)


@cache_page(60*60)
def index(request):
    articles = Article.objects.published()[:25]
    comments = Comment.objects.filter(status=1).order_by('-publish_date')[:10]
    categories = [cat for article in articles for cat in article.categories.all()][:8]
    categories = list(set(categories))
    return render(request, 'index.html', locals())


@cache_page(60*60*8)
def top_stories(request):
    section = SECTIONS[0]
    articles = Article.objects.top_stories()
    last_articles = Article.objects.published()[:25]
    comments = Comment.objects.filter(status=1).order_by('-publish_date')[:10]
    if last_articles:
        categories = [cat for article in last_articles for cat in article.categories.all()][:8]
        categories = list(set(categories))
    return render(request, 'index_no_header.html', locals())


@cache_page(60*60)
def bookmarks(request):
    section = SECTIONS[1]
    articles = Article.objects.bookmarks(user=request.user)
    comments = Comment.objects.filter(status=1).order_by('-publish_date')[:10]
    if articles:
        categories = [cat for article in articles for cat in article.categories.all()][:8]
        categories = list(set(categories))
    return render(request, 'index_no_header.html', locals())


def category(request,slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(categories=category)[:25]
    comments = Comment.objects.all().order_by('-publish_date')[:10]
    last_articles = Article.objects.published()[:25]
    if articles:
        categories = [cat for article in last_articles for cat in article.categories.all()][:8]
        categories = list(set(categories))
    return render(request, 'index_no_header.html', locals())


def useroptions(request):
    url = request.GET.get('url','/')
    article_slug = request.GET.get('article','')
    blog_slug = request.GET.get('blog','')
    if article_slug and blog_slug:
        blog = Blog.objects.get(slug=blog_slug)
        if request.user == blog.user:
            article = Article.objects.get(slug=article_slug)
    return render(request, 'useroptions.html', locals())


class DataGetCategories(View):
    def get(self, request):
        data = []
        try:
            cat = Category.objects.all()
            data = sorted(cat.title.split('\n'))
        except Category.DoesNotExist:
            data = []

        return HttpResponse(
            json.dumps(data), content_type='application/json')


def get_related_posts(request):
    results = []
    if request.is_ajax():
        q = request.GET.get('term', '')
        results = [{'text': art.title, 'id': art.id} for art in Article.objects.filter(title__icontains=q)]
        data = json.dumps(results)
    else:
        data = []
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_categories(request):
    results = []
    if request.is_ajax():
        q = request.GET.get('term', '')
        results = [{'text': cat.title, 'id': cat.id} for cat in Category.objects.filter(title__istartswith=q)]
        data = json.dumps(results)
    else:
        data = []
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def remove_link(request):
    if request.is_ajax():
        link_id = int(request.GET.get('id', ''))
        blog_id = int(request.GET.get('blog_id', ''))
        try:
            c = {}
            External_link.objects.get(id=link_id).delete()
            c['blog'] = Blog.objects.get(id=blog_id)
            context = Context(c)
            template = loader.get_template('base/external_links.html')
            html = template.render(context)
        except:
            html = ""
    else:
        html = ""
    return HttpResponse(html)
