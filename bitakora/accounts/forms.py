from django import forms
from .models import BitakoraUser
import re
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from bitakora.ikasbloga.models import School


class ProfileForm(forms.ModelForm):

    class Meta:
        model = BitakoraUser
        fields = ['first_name', 'last_name']


class ProfilePhotoForm(forms.Form):
    photo = forms.ImageField(label="Zure argazkia", help_text='Igo mesedez zure argazkia. Onartutako formatuak: jpg, png, gif.')

    def clean_argazkia(self):
        photo = self.cleaned_data['photo']
        name = photo.name
        try:
            name.encode('ascii')
        except Exception:
            raise forms.ValidationError(_('The name of the picture (%s) has an unsupported character. Please rename it before uploading.') % name)

        format = name.split('.')[-1]
        if format.lower().strip()==u'bmp':
            raise forms.ValidationError(_("The picture is not in one of our supported formats. We don't support BMP files. Please change it"))


class PasswordReset(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput(),max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput(),max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput(),max_length=100)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordReset, self).__init__(*args, **kwargs)

    def clean_oldpassword(self):
        if self.clean_data.get('oldpassword') and not self.user.check_password(self.clean_data['oldpassword']):
            raise ValidationError(_('Please type your current password.'))
        return self.clean_data['oldpassword']

    def clean_password2(self):
        if self.clean_data.get('password1') and self.clean_data.get('password2') and self.clean_data['password1'] != self.clean_data['password2']:
            raise ValidationError(_('The new passwords are not the same'))
        return self.clean_data['password2']


class RegistrationForm(UserCreationForm):
    required_css_class = 'required'

    email = forms.EmailField(label=_("E-mail"))
    code = forms.CharField(label=_("Code"), required=False)
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=False)

    class Meta:
        model = BitakoraUser
        fields = ("email", )

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if BitakoraUser.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if self.cleaned_data.get("code", None):
            user.code = self.cleaned_data["code"]
        if self.cleaned_data.get("school", None):
            user.school = self.cleaned_data["school"]
        if commit:
            user.save()
        return user


class StudentRegistrationForm(RegistrationForm):
    code = forms.CharField(label=_("Code"), required=True)

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('school')

    class Meta:
        model = BitakoraUser
        fields = ("email", )


class TeacherRegistrationForm(RegistrationForm):
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super(TeacherRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('code')

    class Meta:
        model = BitakoraUser
        fields = ("email", )