from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from bitakora.base.models import Article, Blog, Category, Comment, CONTENT_STATUS_PUBLISHED
from bitakora.base.forms import ArticleForm, BlogForm, CommentForm, AnonimousCommentForm, WPXMLForm
from bitakora.utils.images import handle_uploaded_file
from bitakora.utils.slug import time_slug_string
from bitakora.utils.import_from_wp import import_from_wp
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context
from django.utils.translation import activate


def blog_index(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    articles = blog.get_articles()[:10]
    categories = [cat for art in articles for cat in art.categories.all()][:8]
    categories = list(set(categories))
    return render_to_response('base/blog_index.html', locals(), context_instance=RequestContext(request))


def article(request, blogslug, slug):
    article = get_object_or_404(Article, blog__slug=blogslug, slug=slug)
    if (article.status != CONTENT_STATUS_PUBLISHED or article.publish_date > datetime.now()) and article.blog.user != request.user:
        raise Http404
    elif article.status != CONTENT_STATUS_PUBLISHED:
        draft_status = True
    elif article.publish_date > datetime.now():
        future_date = True
    blog = article.blog
    if request.user.is_authenticated():
        form = CommentForm()
    else:
        form = AnonimousCommentForm()
    return render_to_response('base/article.html', locals(), context_instance=RequestContext(request))


def blog_archive(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    articles = blog.get_articles()
    categories = [cat for art in articles for cat in art.categories.all()][:8]
    categories = list(set(categories))
    return render_to_response('base/blog_archive.html', locals(), context_instance=RequestContext(request))


def my_posts(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render_to_response('base/dashboard.html', locals(), context_instance=RequestContext(request))


def my_comments(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render_to_response('base/dashboard_comments.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/users/login')
def add_article(request, blogslug):
    blog = get_object_or_404(Blog, slug=blogslug, user=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if request.FILES.get('featured_image', ''):
            format = request.FILES.get('featured_image', '').name.split('.')[-1]
            if format.lower().strip() not in (u'jpg', u'png', u'gif'):
                form.add_error('featured_image', _('Invalid image format. Please, change the format!'))
        if form.is_valid():
            article = form.save(commit=False)
            if not Article.objects.filter(slug=slugify(article.title)).exists():
                article.slug = slugify(article.title)
            else:
                article.slug = slugify(article.title) + "-" + time_slug_string()
            if request.FILES.get('featured_image', ''):
                article.featured_image = handle_uploaded_file(request.FILES['featured_image'], request.user)
            article.author = request.user
            article.blog = blog
            article.save()
            form.save_m2m()
            if form.cleaned_data['send_notification']:
                send_mail(_('New article to publish'), _('%s wants to publish this article: http://%s%s') % (article.blog.user.get_fullname(), Site.objects.get_current().domain, article.get_absolute_url()), settings.DEFAULT_FROM_EMAIL, [settings.BITAKORA_SEND_MAIL], fail_silently=False)
            return HttpResponseRedirect(reverse('article', kwargs={'blogslug': blogslug, 'slug': article.slug}))
    else:
        form = ArticleForm()
    return render_to_response('base/add_article.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/users/login')
def edit_article(request, blogslug, slug):
    article = get_object_or_404(Article, blog__slug=blogslug, slug=slug, blog__user=request.user)
    blog = article.blog
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if request.FILES.get('featured_image', ''):
            format = request.FILES.get('featured_image', '').name.split('.')[-1]
            if format.lower().strip() not in (u'jpg', u'png', u'gif'):
                form.add_error('featured_image', _('Invalid image format. Please, change the format!'))
        if form.is_valid():
            article = form.save(commit=False)
            if request.FILES and request.FILES.get('featured_image', ''):
                article.featured_image = handle_uploaded_file(request.FILES['featured_image'], request.user)
            article.save()
            form.save_m2m()
            if form.cleaned_data['send_notification']:
                send_mail(_('New article to publish'), _('%s wants to publish this article: http://%s%s') % (article.blog.user.get_fullname(), Site.objects.get_current().domain, article.get_absolute_url()), settings.DEFAULT_FROM_EMAIL, [settings.BITAKORA_SEND_MAIL], fail_silently=False)
            return HttpResponseRedirect(reverse('article', kwargs={'blogslug': blogslug, 'slug': article.slug}))
        else:
            form.fields['categories'].widget.choices = [(c.id, c.title) for c in Category.objects.filter(id__in=form.cleaned_data['categories'])]
            form.fields['related_posts'].widget.choices = [(r.id, r.title) for r in Article.objects.filter(id__in=form.cleaned_data['related_posts'])]
    else:
        form = ArticleForm(cat=article.categories.all(), rel=article.related_posts.all(), instance=article)
    return render_to_response('base/edit_article.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/users/login')
def delete_article(request, blogslug, slug):
    article = get_object_or_404(Article, blog__slug=blogslug, slug=slug, blog__user=request.user)
    blog = article.blog
    article.delete()
    return HttpResponseRedirect(reverse('blog_index', kwargs={'slug': blog.slug}))


@login_required(login_url='/users/login')
def new_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        wp_form = WPXMLForm()
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(request.user.username)
            if request.FILES.get('header_image', ''):
                blog.header_image = handle_uploaded_file(request.FILES['header_image'], request.user)
            blog.user = request.user
            blog.save()
            return HttpResponseRedirect(reverse('blog_index', kwargs={'slug': blog.slug}))
    else:
        form = BlogForm()
        wp_form = WPXMLForm()
    return render_to_response('base/new_blog.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/users/login')
def import_blog(request):
    form = BlogForm()
    if request.method == 'POST':
        wp_form = WPXMLForm(request.POST, request.FILES)
        if wp_form.is_valid() and request.FILES:
            try:
                blog = import_from_wp(request.FILES['wp_xml'].read(), request.user)
                return HttpResponseRedirect(reverse('blog_index', kwargs={'slug': blog.slug}))
            except:
                msg = _('Importation error. Please, check the XML file and try again.')
                messages.add_message(request, messages.SUCCESS, msg, fail_silently=True)
    else:
        wp_form = WPXMLForm()
    return render_to_response('base/new_blog.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/users/login')
def export_blog(request, slug):
    try:
        blog = Blog.objects.get(user=request.user)
        context = Context({"blog": blog})
        activate("en")
        template = get_template("wp_export_template.xml")
        response = HttpResponse(content_type='application/xhtml+xml')
        response['Content-Disposition'] = 'attachment; filename=wp_export_%s.xml' % (blog.name)
        response.write(template.render(context))
        return response
    except:
        return HttpResponse('ERROR')


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

        if form.is_valid:
            return HttpResponseRedirect(reverse('article', kwargs={'blogslug': blogslug, 'slug': article.slug}))
    else:
        if user.is_authenticated():
            form = CommentForm()
        else:
            form = AnonimousCommentForm()
    return render_to_response('base/add_article.html', locals(), context_instance=RequestContext(request))


def change_comment_status(request):
    comment_id = request.GET.get("comment_id", "")
    status = request.GET.get("status", 1)
    nexturl = request.GET.get("next", "")
    if comment_id:
        cmt = Comment.objects.get(id=comment_id)
        if request.user == cmt.parent.blog.user:
            if not int(status) == 3:
                cmt.status = int(status)
                cmt.save()
            else:
                cmt.delete()
        return HttpResponseRedirect(reverse('article', kwargs={'blogslug': cmt.parent.blog.slug, 'slug': cmt.parent.slug}))
    if nexturl:
        return HttpResponseRedirect(nexturl)
