from django.contrib.syndication.views import Feed
from django.urls import reverse
from bitakora.base.models import Article, Blog
from django.template.defaultfilters import striptags
from django.utils.translation import ugettext_lazy as _

class BlogEntriesFeed(Feed):

    def get_object(self, request, blogslug):
        return Blog.objects.get(slug=blogslug)

    def title(self, obj):
        return obj.name

    def link(self, obj):
        return "/%s/feed.xml" % (obj.name)

    def description(self, obj):
        return "%s %s" % (obj.name, _("articles feed"))

    def author_name(self, obj):
        return obj.user.get_fullname()

    def feed_copyright(self,obj):
        return obj.get_license_display()

    def items(self,obj):
        return Article.objects.published(for_blog=obj)[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    def item_pubdate(self, item):
        return item.publish_date

    def item_categories(self, item):
        return item.categories.all()