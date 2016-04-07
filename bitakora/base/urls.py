from django.conf.urls import patterns, url, include
from bitakora.rss.feeds import BlogEntriesFeed
from django.views.generic.base import RedirectView

urlpatterns = patterns('bitakora.base.views',
    url(r'^new-blog$', 'new_blog', name='new_blog'),
    url(r'^new-blog/import$', 'import_blog', name='import_blog'),
    url(r'^change_comment_status$','change_comment_status', name='change_comment_status'),
    url(r'^(?P<slug>[\-\d\w]+)$', 'blog_index', name='blog_index'),
    url(r'^(?P<slug>[\-\d\w]+)/archive$','blog_archive', name='blog_archive'),
    url(r'^(?P<slug>[\-\d\w]+)/my-posts$', 'my_posts', name='my_posts'),
    url(r'^(?P<slug>[\-\d\w]+)/my_comments$', 'my_comments', name='my_comments'),
    url(r'^(?P<blogslug>[\-\d\w]+)/add-article$','add_article', name='add_article'),
    #url(r'^(?P<blogslug>[\-\d\w]+)/rss$', BlogEntriesFeed(), name="blog_rss"),
    url(r'^(?P<blogslug>[\-\d\w]+)/rss$', RedirectView.as_view(pattern_name='blog_rss')),
    url(r'^(?P<blogslug>[\-\d\w]+)/feed.xml$', BlogEntriesFeed(), name="blog_rss"),
    url(r'^(?P<blogslug>[\-\d\w]+)/(?P<slug>[\-\d\w]+)$','article', name='article'),
    url(r'^(?P<blogslug>[\-\d\w]+)/(?P<slug>[\-\d\w]+)/edit-article$','edit_article', name='edit_article'),
    url(r'^(?P<blogslug>[\-\d\w]+)/(?P<slug>[\-\d\w]+)/delete-article$','delete_article', name='delete_article'),
    url(r'^(?P<blogslug>[\-\d\w]+)/(?P<slug>[\-\d\w]+)/add-comment$','add_comment', name='add_comment'),
)
