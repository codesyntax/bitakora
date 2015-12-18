from django.conf import settings
from django import forms
from photologue.models import Photo
from bitakora.base.models import *
from tinymce.widgets import TinyMCE
from captcha.fields import ReCaptchaField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

TINYMCE_DEFAULT_CONFIG = getattr(settings, 'TINYMCE_DEFAULT_CONFIG', {})

class ArticleForm(forms.ModelForm):
    featured_image = forms.FileField(label=_('Header image'),help_text=_('Valid formats: jpg, png, gif.'),required=False)
    text = forms.CharField(label=_('Text'),widget=TinyMCE(mce_attrs=TINYMCE_DEFAULT_CONFIG))
    categories = forms.ModelMultipleChoiceField(label=_('Categories'),widget=forms.SelectMultiple(attrs={'class':'chosen-category','data-placeholder':_('Choose categories')}),queryset=Category.objects.all(),required=False)
    related_posts = forms.ModelMultipleChoiceField(label=_('Related posts'),widget=forms.SelectMultiple(attrs={'class':'chosen-select','data-placeholder':_('Choose related posts')}),queryset=Article.objects.all(),required=False)
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=CONTENT_STATUS_CHOICES,initial=CONTENT_STATUS_DRAFT)
    captcha = ReCaptchaField()

    def clean_featured_image(self):
        try:
            photo = Photo.objects.get(id=self.cleaned_data['featured_image'])
            return photo
        except:
            return None

    def is_valid(self):
        valid = super(ArticleForm, self).is_valid()
        if not valid:
            cleaned_data = self.cleaned_data
            data = dict(self.data).get('categories')
            if data:
                for i,cat in enumerate(data):
                    if Category.objects.filter(slug=slugify(cat)):
                        data[i] = u"%s" % (Category.objects.get(slug=slugify(cat)).title)
                    elif not cat.isdigit():
                        cat_obj = Category(title=cat,slug=slugify(cat))
                        cat_obj.save()
                        data[i] = u"%d" % (cat_obj.id)
                
                self.cleaned_data.update({
                    'categories': list(set(data)),
                })
                if 'categories' in self.errors:
                    self.errors.pop('categories')
        valid = super(ArticleForm, self).is_valid()
        return valid



    class Meta:
        model = Article
        fields = ['title', 'text', 'featured_image', 'categories', 'related_posts', 'status', 'publish_date', 'allow_comments']


class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(label=_('Text'),widget=TinyMCE(mce_attrs=TINYMCE_DEFAULT_CONFIG))

    class Meta:
        model = Article
        fields = ['title', 'slug', 'text', 'featured_image', 'blog','categories', 'related_posts', 'allow_comments','publish_date','expiry_date','status']


class BlogForm(forms.ModelForm):
    header_image = forms.ImageField(label=_('Header image'),help_text=_('Valid formats: jpg, png, gif.'),required=False)
    template = forms.ChoiceField(widget=forms.RadioSelect, choices=TEMPLATE_CHOICES,initial=DEFAULT_TEMPLATE)
    license = forms.ChoiceField(widget=forms.RadioSelect, choices=LICENSE_CHOICES,initial=DEFAULT_LICENSE)
    captcha = ReCaptchaField()

    class Meta:
        model = Blog
        fields = ['name', 'tagline', 'header_image','template','license','analytics_code']

class BlogFormNoCaptcha(forms.ModelForm):
    header_image = forms.ImageField(label=_('Header image'),help_text=_('Valid formats: jpg, png, gif.'),required=False)
    template = forms.ChoiceField(widget=forms.RadioSelect, choices=TEMPLATE_CHOICES,initial=DEFAULT_TEMPLATE)
    license = forms.ChoiceField(widget=forms.RadioSelect, choices=LICENSE_CHOICES,initial=DEFAULT_LICENSE)
    
    class Meta:
        model = Blog
        fields = ['name', 'tagline', 'header_image','template','license','analytics_code']

    
class CommentForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.Textarea)
    captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ['text',]

    def clean_body(self):
        text = self.cleaned_data['text'].strip()
        if not text:
            raise forms.ValidationError(_('Empty comment. Please, write something!'))

class AnonimousCommentForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.Textarea)
    captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ['nickname','email','text',]

    def clean_body(self):
        text = self.cleaned_data['text'].strip()
        if not text:
            raise forms.ValidationError(_('Empty comment. Please, write something!'))
