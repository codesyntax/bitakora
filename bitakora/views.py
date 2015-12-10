from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from bitakora.base.models import Article, Category, Blog, Comment
from voting.models import Vote
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _

SECTIONS = (
    (1, _('Top stories')),
    (2, _('Bookmarks')),
)

def index(request):
    articles = Article.objects.published()[:25]
    comments = Comment.objects.all().order_by('-publish_date')[:10]
    categories = Category.objects.all()[:8]
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def top_stories(request):
    section = SECTIONS[0]
    articles = Article.objects.top_stories()
    comments = Comment.objects.all().order_by('-publish_date')[:10]
    categories = Category.objects.all()[:8]
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def bookmarks(request):
    section = SECTIONS[1]
    articles = Article.objects.bookmarks(user=request.user)
    comments = Comment.objects.all().order_by('-publish_date')[:10]
    categories = Category.objects.all()[:8]
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def category(request,slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(categories=category)[:25]
    comments = Comment.objects.all().order_by('-publish_date')[:10]
    categories = Category.objects.all().exclude(slug=slug)[:8]
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def useroptions(request):
    url = request.GET.get('url','/')
    article_slug = request.GET.get('article','')
    blog_slug = request.GET.get('blog','')
    if article_slug and blog_slug:
        blog = Blog.objects.get(slug=blog_slug)
        if request.user == blog.user:
            article = Article.objects.get(slug=article_slug)
    return render_to_response('useroptions.html', locals(), context_instance=RequestContext(request))

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