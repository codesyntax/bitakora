from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from bitakora.utils.images import get_pattern
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from photologue.models import Photo
from django.utils.translation import ugettext as _
from bitakora.ikasbloga.models import School
from django.db.models.signals import post_save
from django.dispatch import receiver

PROFILE_PHOTO_DEFAULT=getattr(settings,'PROFILE_PHOTO_DEFAULT','')
BLOG_PHOTO_SLUG=getattr(settings,'BLOG_PHOTO_DEFAULT_SLUG','no-blog-photo')

USERTYPE_CHOICES = (
    (1, _("Normal")),
    (2, _("Student")),
    (3, _("Teacher")),
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, code=None, school=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class BitakoraUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='E-maila',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name="Izena", max_length=200, blank=True, null=True)
    last_name = models.CharField(verbose_name="Abizenak", max_length=200, blank=True, null=True)
    bio = models.TextField(verbose_name="Biografia/Deskribapena", null=True, blank=True)
    photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.CharField(_('Phone Number'), max_length=25, blank=True, null=True,)

    twitter_id = models.CharField(max_length=100, blank=True,null=True)
    facebook_id = models.CharField(max_length=100, blank=True,null=True)
    openid_id = models.CharField(max_length=100, blank=True,null=True)
    googleplus_id = models.CharField(max_length=100, blank=True,null=True)

    usertype = models.PositiveSmallIntegerField(choices=USERTYPE_CHOICES , default=0)
    added_source = models.PositiveSmallIntegerField(default = 0)

    last_updated = models.DateTimeField(auto_now_add=True,editable=False)
    date_joined = models.DateTimeField(auto_now_add=True,editable=False,null=True,blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    code = models.CharField(max_length=100, blank=True,null=True)
    school = models.ForeignKey(School, null=True, blank=True, on_delete=models.SET_NULL)

    added = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('BitakoraUser')
        verbose_name_plural = _('BitakoraUsers')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        elif self.first_name:
            return self.first_name
        else:
            return self.email

    def get_photo(self):
        if self.photo:
            return self.photo
        else:
            try:
                return Photo.objects.get(slug=PROFILE_PHOTO_DEFAULT)
            except Exception:
                return None

    def get_blog(self):
        from bitakora.base.models import Blog
        blogs = Blog.objects.filter(user=self)
        try:
            return blogs[0]
        except Exception:
            return None

    def get_profile(self):
        return self

    def get_absolute_url(self):
        return "/%s" % (self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_blog_photo(self):
        try:
            return Photo.objects.get(slug=BLOG_PHOTO_SLUG+'-'+str(get_pattern(self)))
        except Exception:
            return None


@receiver(post_save, sender=BitakoraUser, dispatch_uid="update_user_type_count")
def update_user_type(sender, instance, created, **kwargs):
    if created:
        if instance.school:
            instance.usertype = 3
        elif instance.code:
            instance.usertype = 2
        else:
            instance.usertype = 1
        instance.save()
