from django import forms
from models import BitakoraUser
import re
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

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

    username = forms.CharField(label=_("Username"))
    email = forms.EmailField(label=_("E-mail"))

    class Meta:
        model = BitakoraUser
        fields = ('username', "email")

    def clean_username(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError(_("This username contains spaces. Please, register an username without spaces."))
        return username

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if BitakoraUser.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']
