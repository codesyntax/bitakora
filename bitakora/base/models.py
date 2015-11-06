from django.db import models
from django.utils.translation import ugettext_lazy as _

class Blog(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

 class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField(verbose_name=_('Slug'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class Community(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Community')
        verbose_name_plural = _('Communities')
