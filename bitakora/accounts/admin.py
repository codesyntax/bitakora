from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm,UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext as _
from models import BitakoraUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = BitakoraUser
        fields = ('username','password')

class MyUserCreationForm(ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = BitakoraUser
        fields = ('username','password1','password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class BitakoraUserAdmin(admin.ModelAdmin):
    def admin_thumbnail(self,obj):
        if obj.photo:
            return obj.photo.admin_thumbnail()
        return ''
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True


    def get_email(self, obj):
        """ """
        return obj.email

    def fullname(self, obj):
        """ """
        return obj.get_fullname()

    form = MyUserChangeForm
    add_form = MyUserCreationForm

    list_display = ('fullname', 'username','get_email', 'date_joined','is_active', 'is_staff','admin_thumbnail')
    list_display_links = ('fullname','username')
    ordering = ('-date_joined',)
    search_fields = ['email','username',]
    raw_id_fields = ('photo',)


    fieldsets = (
        (None, {'fields': ('username', 'password')}),

        (_('Personal data'),
        {'fields':('fullname', 'email', 'phone', 'photo')},),
        (_('Biography'),
        {'fields': ('bio',)}),
        (_('Social networks'), {
            'fields': ('twitter_id', 'facebook_id', 'openid_id', 'googleplus_id')
        }),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions','last_login'),
                            'classes': ['collapse',],}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(BitakoraUserAdmin, self).get_form(request, obj, **defaults)

admin.site.register(BitakoraUser, BitakoraUserAdmin)