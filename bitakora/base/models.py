import time
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect
from photologue.models import Photo
from django.contrib.sites.models import Site
from bitakora.base.managers import PublishedManager
from bitakora.utils.models import get_user_model_name
from bitakora.utils.text import make_responsive
from bitakora.utils.images import get_pattern
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
from django.template.defaultfilters import removetags, striptags, truncatechars
from voting.models import Vote
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from django.contrib.sites.models import Site

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now    

user_model_name = get_user_model_name()

DEFAULT_TEMPLATE = "one-page-wonder.css"

TEMPLATE_CHOICES = (
    (DEFAULT_TEMPLATE, _("One page wonder")),
    ("minimalist-blog.css", _("Minimalist")),
)

DEFAULT_LICENSE = "cc-by-sa"

LICENSE_CHOICES = (
    (DEFAULT_LICENSE, _("CC-BY-SA")),
    ("copyright", _("Copyright")),
)

BLOG_PHOTO_SLUG=getattr(settings,'BLOG_PHOTO_DEFAULT_SLUG','no-blog-photo')

class Blog(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField(_("URL"), max_length=300, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))
    tagline = models.CharField(max_length=200, verbose_name=_('Tagline'),null=True,blank=True)
    header_image = models.ForeignKey(Photo,null=True,blank=True)
    custom_html = models.TextField(max_length=2000, verbose_name=_('Custom HTML'), null=True, blank=True)
    analytics_code = models.TextField(max_length=1000, verbose_name=_('Analytics code'), null=True, blank=True)

    template = models.CharField(_("Template"), max_length=200,
        choices=TEMPLATE_CHOICES, default=DEFAULT_TEMPLATE)

    license = models.CharField(_("License"), max_length=200,
        choices=LICENSE_CHOICES, default=DEFAULT_LICENSE)

    user = models.ForeignKey(user_model_name, verbose_name=_("Author"),
        related_name="%(class)ss")

    def get_photo(self):
        if self.header_image:
            return self.header_image
        else:
            try:
                return Photo.objects.get(slug=BLOG_PHOTO_SLUG+'-'+str(get_pattern(self.user)))
            except:
                return None

    def get_articles(self):
        from bitakora.base.models import Article
        return Article.objects.published(for_blog=self)

    def get_articles_months(self):
        from bitakora.base.models import Article, CONTENT_STATUS_PUBLISHED
        month_list = Article.objects.filter(blog=self,status=CONTENT_STATUS_PUBLISHED).dates('publish_date','month',order='DESC')
        return month_list

    def get_myposts(self):
        from bitakora.base.models import Article
        return Article.objects.filter(blog=self).order_by('-publish_date')

    def get_comments(self):
        from bitakora.base.models import Comment
        articles = self.get_articles()
        return Comment.objects.filter(parent__in=articles)

    def get_last_comments(self):
        return self.get_comments()[:5]

    def get_blog_template(self):
        return "%s/%s/%s" % ("base","css",self.template)

    def get_absolute_url(self):
        return "/%s" % (self.slug)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

class Category(models.Model):
    title = models.CharField(_("Title"), max_length=500)
    slug = models.SlugField(_("URL"), max_length=2000, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("title",)

    # @models.permalink
    # def get_absolute_url(self):
    #     return ("blog_post_list_category", (), {"category": self.slug})


CONTENT_STATUS_DRAFT = 1
CONTENT_STATUS_PUBLISHED = 2
CONTENT_STATUS_CHOICES = (
    (CONTENT_STATUS_DRAFT, _("Draft")),
    (CONTENT_STATUS_PUBLISHED, _("Published")),
)

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(_("URL"), max_length=2000, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))

    text = models.TextField(verbose_name=_('Text'))

    blog = models.ForeignKey(Blog)
    
    status = models.IntegerField(_("Status"),
        choices=CONTENT_STATUS_CHOICES, default=CONTENT_STATUS_PUBLISHED,
        help_text=_("With Draft chosen, will only be shown for admin users "
            "on the site."))
    publish_date = models.DateTimeField(_("Published from"),
        help_text=_("With Published chosen, won't be shown until this time"),
        blank=True, null=True, db_index=True, default=now)
    expiry_date = models.DateTimeField(_("Expires on"),
        help_text=_("With Published chosen, won't be shown after this time"),
        blank=True, null=True)
    categories = models.ManyToManyField(Category,
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="blogposts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    
    featured_image = models.ForeignKey(Photo,verbose_name=_("Featured Image"), null=True, blank=True)
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)

    shared = models.BooleanField(default=False)

    objects = PublishedManager()

    def get_summary(self):
        return truncatechars(striptags(self.text), 600)

    def get_comments(self):
        return self.comments.all().order_by("publish_date")

    def get_visible_comments(self):
        return self.comments.filter(status=COMMENT_STATUS_VISIBLE).order_by("publish_date")

    def get_comments_count(self):
        return self.get_visible_comments().count()

    def is_editable(self, request):
        """
        Restrict in-line editing to the objects's owner and superusers.
        """
        return request.user.is_superuser or request.user.id == self.user_id

    def _get_next_or_previous_by_publish_date(self, is_next, **kwargs):
        """
        Retrieves next or previous object by publish date. We implement
        our own version instead of Django's so we can hook into the
        published manager and concrete subclasses.
        """
        arg = "publish_date__gt" if is_next else "publish_date__lt"
        order = "publish_date" if is_next else "-publish_date"
        lookup = {arg: self.publish_date}
        try:
            queryset = Article.objects.published
        except AttributeError:
            queryset = Article.objects.all
        try:
            return queryset(**kwargs).filter(**lookup).order_by(order)[0]
        except IndexError:
            pass


    def get_next_by_publish_date(self, **kwargs):
        """
        Retrieves next object by publish date.
        """
        return self._get_next_or_previous_by_publish_date(True, **kwargs)

    def get_previous_by_publish_date(self, **kwargs):
        """
        Retrieves previous object by publish date.
        """
        return self._get_next_or_previous_by_publish_date(False, **kwargs)

    def getTweetText(self):
        current_site = Site.objects.get_current()
        if self.blog.user.twitter_id:
            return "[%s] %s %s%s @%s" % (truncatechars(self.blog.name,20), truncatechars(self.title,40), current_site, self.get_absolute_url(), self.blog.user.twitter_id)
        return "[%s] %s %s%s" % (truncatechars(self.blog.name,20), truncatechars(self.title,40), current_site, self.get_absolute_url())

    def get_absolute_url(self):
        return reverse('article',kwargs={'blogslug': self.blog.slug, 'slug': self.slug})

    def save(self, *args, **kwargs):
        self.text = make_responsive(self.text)
        super(Article, self).save(*args, **kwargs)

    def get_rating(self):
        ctype = ContentType.objects.get_for_model(self)
        votes = Vote.objects.filter(object_id=self.id, content_type=ctype).count()
        comments = self.get_comments_count()
        return votes + comments

    def get_reverse_rating(self):
        return self.get_rating() * -1

    def get_timestamp(self):
        dtt = self.publish_date.timetuple()
        return time.mktime(dtt)

    def get_reverse_timestamp(self):
        return self.get_timestamp() * -1

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-publish_date",)

COMMENT_STATUS_VISIBLE = 1
COMMENT_STATUS_VISIBLEADMIN = 2
COMMENT_STATUS_NOTVISIBLE = 3
COMMENT_STATUS_CHOICES = (
    (COMMENT_STATUS_VISIBLE, _("Visible")),
    (COMMENT_STATUS_VISIBLEADMIN, _("Visible only for the admin")),
    (COMMENT_STATUS_NOTVISIBLE, _("Not visible")),
)

class Comment(models.Model):
    user = models.ForeignKey(user_model_name, verbose_name=_("Author"),
        related_name="%(class)ss",null=True,blank=True)

    nickname = models.CharField(verbose_name=_('Nick name'),max_length=200,null=True,blank=True)
    email = models.EmailField(verbose_name=_('Email'),null=True,blank=True)
    url = models.CharField(verbose_name=_('Url'),max_length=300,null=True,blank=True)

    parent = models.ForeignKey(Article, null = True, blank=True, related_name='comments')
    text = models.TextField(verbose_name=_('Text'), null=True,blank = True)

    ip_address  = models.GenericIPAddressField(verbose_name=_('IP address'), blank=True, null=True)
    status = models.IntegerField(_("Status"),
        choices=COMMENT_STATUS_CHOICES, default=COMMENT_STATUS_VISIBLE)
    publish_date = models.DateTimeField(_("Publish date"),
        blank=True, null=True, db_index=True)


    def get_absolute_url(self):
        return reverse('article',kwargs={'blogslug': self.parent.blog.slug, 'slug': self.parent.slug})

    def __unicode__(self):
        return u"%s" % self.user

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ("-publish_date",)


def send_comment_email(sender,instance,**kwargs):
    if kwargs['created'] and instance.email != instance.parent.blog.user.email:
        context_dict = {}
        if instance.user:
            context_dict['from_user'] = instance.user.get_fullname()
            context_dict['url'] = "http://%s%s" % (Site.objects.get_current().domain,instance.user.get_absolute_url())
        else:
            context_dict['from_user'] = instance.nickname
            context_dict['url'] = instance.url
        context_dict['from_email'] = instance.email
        context_dict['to_email'] = instance.parent.blog.user.email
        context_dict['comment_url'] = "http://%s%s" % (Site.objects.get_current().domain,instance.get_absolute_url())
        context_dict['comment_body'] = instance.text

        template = get_template("comment_email_template.txt")
        context = Context(context_dict)
        message  = template.render(context)

        send_mail("[%s] - %s" % (_("Bitakora"), _("New comment")), message, settings.DEFAULT_FROM_EMAIL, [context_dict['to_email']])

post_save.connect(send_comment_email, sender=Comment)