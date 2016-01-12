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
    categories = forms.CharField(label=_('Categories'), widget=forms.SelectMultiple(),required=False)
    related_posts = forms.CharField(label=_('Related posts'), widget=forms.SelectMultiple(),required=False)
    status = forms.ChoiceField(label=_('Status'), widget=forms.RadioSelect, choices=CONTENT_STATUS_CHOICES,initial=CONTENT_STATUS_DRAFT)
    captcha = ReCaptchaField()

    def clean_featured_image(self):
        try:
            photo = Photo.objects.get(id=self.cleaned_data['featured_image'])
            return photo
        except:
            return None

    def clean_categories(self):
        if self.cleaned_data.get('categories'):
            categories = self.cleaned_data['categories']
            cat_lst = []
            for cat in eval(categories):
                if not isdigit(cat):
                    cat_lst.append(Category(title=cat,slug=slugify(cat)))
                else:
                    cat_lst.append(int(cat))
            return cat_lst
        else:
            return []

    def clean_related_posts(self):
        if self.cleaned_data.get('related_posts'):
            posts = self.cleaned_data['related_posts']
            return map(int,eval(posts))
        else:
            return []

    def __init__(self, *args, **kwargs):
        cat = kwargs.pop('cat', None)
        rel = kwargs.pop('rel', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        if cat:
            import pdb;pdb.set_trace()
            self.fields['categories'].queryset = cat
        if rel:
            self.fields['related_posts'].queryset = rel

    class Meta:
        model = Article
        fields = ['title', 'text', 'featured_image', 'status', 'categories','related_posts','publish_date', 'allow_comments']


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


class WPXMLForm(forms.Form):
    wp_xml = forms.FileField(label=_("Wordpress file"), help_text=_("Please, select your Wordpress XML file")) 
