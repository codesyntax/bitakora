from django.conf import settings
import ast
from django import forms
from photologue.models import Photo
from bitakora.base.models import *
from tinymce.widgets import TinyMCE
from captcha.fields import ReCaptchaField
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify

TINYMCE_DEFAULT_CONFIG = getattr(settings, 'TINYMCE_DEFAULT_CONFIG', {})
GOOGLE_URL_HTML = _("More information about  <a href='https://www.google.com/intl/es/analytics/features/index.html'>Google Analytics</a>.")

class ArticleForm(forms.ModelForm):
    featured_image = forms.FileField(label=_('Featured image'),help_text=_('Valid formats: jpg, png, gif.'),required=False)
    text = forms.CharField(label=_('Text'),widget=TinyMCE(mce_attrs=TINYMCE_DEFAULT_CONFIG))
    categories = forms.CharField(label=_('Categories'),widget=forms.SelectMultiple(), required=False)
    related_posts = forms.CharField(label=_('Related posts'), widget=forms.SelectMultiple(),required=False)
    status = forms.ChoiceField(label=_('Status'), widget=forms.RadioSelect, choices=CONTENT_STATUS_CHOICES,initial=CONTENT_STATUS_PUBLISHED)
    send_notification = forms.BooleanField(label=_('Send notification'), initial=False, required=False)

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
            for cat in ast.literal_eval(categories):
                if not cat.isdigit():
                    cat_name = slugify(cat)
                    cat_qty = Category.objects.filter(slug__icontains=cat_name).count()
                    if cat_qty:
                        cat_name += '-%s' % (str(cat_qty+1))
                    cat_ob = Category(title=cat,slug=cat_name)
                    cat_ob.save()
                    cat_lst.append(cat_ob.id)
                else:
                    cat_lst.append(int(cat))
            return cat_lst
        else:
            return []

    def clean_related_posts(self):
        if self.cleaned_data.get('related_posts'):
            posts = self.cleaned_data['related_posts']
            return map(int,ast.literal_eval(posts))
        else:
            return []

    def __init__(self, *args, **kwargs):
        cat = kwargs.pop('cat', None)
        rel = kwargs.pop('rel', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        if cat:
            self.fields['categories'].widget.choices = [(c.id,c.title) for c in cat]
        if rel:
            self.fields['related_posts'].widget.choices = [(r.id,r.title) for r in rel]

    class Meta:
        model = Article
        fields = ['title', 'text', 'featured_image', 'status', 'categories','related_posts','publish_date', 'allow_comments']


class ArticleAdminForm(forms.ModelForm):
    #text = forms.CharField(label=_('Text'),widget=TinyMCE(mce_attrs=TINYMCE_DEFAULT_CONFIG))

    class Meta:
        model = Article
        fields = "__all__"


class BlogForm(forms.ModelForm):
    header_image = forms.ImageField(label=_('Header image'),help_text=_('Valid formats: jpg, png, gif.'),required=False)
    template = forms.ChoiceField(label=_('Template'), widget=forms.RadioSelect, choices=TEMPLATE_CHOICES,initial=DEFAULT_TEMPLATE)
    license = forms.ChoiceField(label=_('License'), widget=forms.RadioSelect, choices=LICENSE_CHOICES,initial=DEFAULT_LICENSE)
    custom_html = forms.CharField(label=_("Custom HTML"), help_text=_('Sidebar extra HTML information'))
    analytics_code = forms.CharField(label=_('Analytics code'), widget=forms.Textarea, help_text=GOOGLE_URL_HTML,required=False)
    captcha = ReCaptchaField()

    class Meta:
        model = Blog
        fields = ['name', 'tagline', 'header_image','template','license','custom_html','analytics_code']

class BlogFormNoCaptcha(forms.ModelForm):
    header_image = forms.ImageField(label=_('Header image'),help_text=_('Valid formats: jpg, png, gif.'),required=False)
    template = forms.ChoiceField(label=_('Template'), widget=forms.RadioSelect, choices=TEMPLATE_CHOICES,initial=DEFAULT_TEMPLATE)
    license = forms.ChoiceField(label=_('License'), widget=forms.RadioSelect, choices=LICENSE_CHOICES,initial=DEFAULT_LICENSE)
    custom_html = forms.CharField(label=_("Custom HTML"), help_text=_('Sidebar extra HTML information'))
    analytics_code = forms.CharField(label=_('Analytics code'), widget=forms.Textarea, help_text=GOOGLE_URL_HTML,required=False)
    
    class Meta:
        model = Blog
        fields = ['name', 'tagline', 'header_image','template','license','custom_html','analytics_code']

    
class CommentForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.Textarea)

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
