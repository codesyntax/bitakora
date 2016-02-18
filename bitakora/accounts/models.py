from cssocialuser.models import CSAbstractSocialUser
from django.contrib.auth.models import UserManager
from bitakora.utils.images import get_pattern
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from photologue.models import Photo
from django.utils.translation import ugettext as _

PROFILE_PHOTO_DEFAULT=getattr(settings,'PROFILE_PHOTO_DEFAULT','')
BLOG_PHOTO_SLUG=getattr(settings,'BLOG_PHOTO_DEFAULT_SLUG','no-blog-photo')

class BitakoraUser(CSAbstractSocialUser):
    last_updated = models.DateTimeField(auto_now_add=True,editable=False)
    date_joined = models.DateTimeField(auto_now_add=True,editable=False,null=True,blank=True)

    class Meta:
        verbose_name = _('BitakoraUser')
        verbose_name_plural = _('BitakoraUsers')

    objects = UserManager()

    def get_photo(self):
        if self.photo:
            return self.photo
        else:
            try:
                return Photo.objects.get(slug=PROFILE_PHOTO_DEFAULT)
            except:
                return None

    def get_blog(self):
        from bitakora.base.models import Blog
        blogs = Blog.objects.filter(user=self)
        try:
            return blogs[0]
        except:
            return None

    def get_fullname(self):
        try:
            return self.get_full_name().strip() or self.username
        except:
            return self.username

    def get_profile(self):
        return self


    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_blog_photo(self):
        try:
            return Photo.objects.get(slug=BLOG_PHOTO_SLUG+'-'+str(get_pattern(self)))
        except:
            return None