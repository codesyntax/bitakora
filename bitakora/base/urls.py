from django.conf.urls import url, include
from bitakora.rss.feeds import BlogEntriesFeed
from django.views.generic.base import RedirectView
from bitakora.contact.views import BitakoraContactFormView, BlogContactDetailView
from bitakora.base import views


urlpatterns = [
    url(r'^new-blog$', views.new_blog, name='new_blog'),
    url(r'^new-blog/import$', views.import_blog, name='import_blog'),
    url(r'^schools/', include('bitakora.ikasbloga.urls')),

    url(r'^change_comment_status$', views.change_comment_status, name='change_comment_status'),
    url(r'^(?P<slug>[\-\d\w]+)$', views.blog_index, name='blog_index'),
    url(r'^(?P<slug>[\-\d\w]+)/archive$', views.blog_archive, name='blog_archive'),
    url(r'^(?P<slug>[\-\d\w]+)/my-posts$', views.my_posts, name='my_posts'),
    url(r'^(?P<slug>[\-\d\w]+)/my_comments$', views.my_comments, name='my_comments'),
    url(r'^(?P<slug>[\-\d\w]+)/export$', views.export_blog, name='export_blog'),
    url(r'^(?P<slug>[\-\d\w]+)/contact$', BitakoraContactFormView.as_view(
        template_name='contact/blog_contact_form.html'),
        name='blog_contact_form'),
    url(r'^(?P<slug>[\-\d\w]+)/contact-sent$', BlogContactDetailView.as_view(
        template_name='contact/blog_contact_form_sent.html'),
        name='blog_contact_form_sent'),

    url(r'^(?P<blogslug>[\-\d\w]+)/add-article$', views.add_article, name='add_article'),
    # url(r'^(?P<blogslug>[\-\d\w]+)/rss$', BlogEntriesFeed(), name="blog_rss"),
    url(r'^(?P<blogslug>[\-\d\w]+)/rss$', RedirectView.as_view(pattern_name='blog_rss')),
    url(r'^(?P<blogslug>[\-\d\w]+)/feed.xml$', BlogEntriesFeed(), name="blog_rss"),
    url(r'^(?P<blogslug>[\-\d\w]+)/(?P<slug>[\-\d\w]+)$', views.article, name='article'),
    url(r'^(?P<blogslug>[\-\d\w]+)/(?P<slug>[\-\d\w]+)/edit-article$', views.edit_article, name='edit_article'),
    url(r'^(?P<blogslug>[\-\d\w]+)/(?P<slug>[\-\d\w]+)/delete-article$', views.delete_article, name='delete_article'),
    url(r'^(?P<blogslug>[\-\d\w]+)/(?P<slug>[\-\d\w]+)/add-comment$', views.add_comment, name='add_comment'),
]
