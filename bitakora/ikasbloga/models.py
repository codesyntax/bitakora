from django.db import models
from django.utils.translation import ugettext_lazy as _


class School(models.Model):
    name = models.CharField(_("School name"), max_length=200)
    desc = models.TextField(_("Description"),blank=True, null=True)
    slug = models.SlugField(_("URL"), max_length=200, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))

    def get_rooms(self):
        return self.room_set.all()


    def get_blogs(self):
        blogs=[]
        for room in self.get_rooms():
            for blog in room.get_blogs():
                blogs.append(blog)
        return blogs


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")


class Level(models.Model):
    name = models.CharField(_("Level name"), max_length=200)
    slug = models.SlugField(_("URL"), max_length=200, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")


class Room(models.Model):
    name = models.CharField(_("Room name"), max_length=200)
    slug = models.SlugField(_("URL"), max_length=200, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))

    code = models.CharField(_("Code"), max_length=4)
    year = models.IntegerField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def get_blogs(self):
        return self.blog_set.all()

    def __str__(self):
        return "%s%s (%s)" % (self.level, self.name, self.school)

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
