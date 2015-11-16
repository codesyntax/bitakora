from django.db import models
from photologue.models import Photo
from bitakora.base.managers import PublishedManager
from bitakora.utils.models import get_user_model_name
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

user_model_name = get_user_model_name()


class Blog(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    tagline = models.CharField(max_length=200, verbose_name=_('Tagline'),null=True,blank=True)
    header_image = models.ForeignKey(Photo,null=True,blank=True)

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
    title = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField(verbose_name=_('Slug'))

    blog = models.ForeignKey(Blog)
    user = models.ForeignKey(user_model_name, verbose_name=_("Author"),
        related_name="%(class)ss")
    status = models.IntegerField(_("Status"),
        choices=CONTENT_STATUS_CHOICES, default=CONTENT_STATUS_PUBLISHED,
        help_text=_("With Draft chosen, will only be shown for admin users "
            "on the site."))
    publish_date = models.DateTimeField(_("Published from"),
        help_text=_("With Published chosen, won't be shown until this time"),
        blank=True, null=True, db_index=True)
    expiry_date = models.DateTimeField(_("Expires on"),
        help_text=_("With Published chosen, won't be shown after this time"),
        blank=True, null=True)
    categories = models.ManyToManyField(Category,
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="blogposts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    # comments = CommentsField(verbose_name=_("Comments"))
    # rating = RatingField(verbose_name=_("Rating"))
    featured_image = models.ForeignKey(Photo,verbose_name=_("Featured Image"), null=True, blank=True)
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)

    objects = PublishedManager()

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

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-publish_date",)


    # def category_list(self):
    #     from warnings import warn
    #     warn("blog_post.category_list in templates is deprecated"
    #          "use blog_post.categories.all which are prefetched")
    #     return getattr(self, "_categories", self.categories.all())

    # def keyword_list(self):
    #     from warnings import warn
    #     warn("blog_post.keyword_list in templates is deprecated"
    #          "use the keywords_for template tag, as keywords are prefetched")
    #     try:
    #         return self._keywords
    #     except AttributeError:
    #         keywords = [k.keyword for k in self.keywords.all()]
    #         setattr(self, "_keywords", keywords)
    #         return self._keywords
