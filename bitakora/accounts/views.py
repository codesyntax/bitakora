from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import HASH_SESSION_KEY
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from bitakora.base.models import Blog, External_link
from bitakora.base.forms import BlogFormNoCaptcha, WPXMLForm, External_linkForm
from bitakora.accounts.forms import ProfileForm, ProfilePhotoForm, StudentRegistrationForm, TeacherRegistrationForm
from django.contrib.auth.views import password_change, password_change_done
from bitakora.utils.images import handle_uploaded_file
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from registration.backends.default.views import RegistrationView
from bitakora.accounts.forms import RegistrationForm

def select_register(request):
    return render(request, 'registration/select_registration_form.html', locals())


def student_registration(request):
    title = _('Create a student account')
    form = StudentRegistrationForm()
    return render(request, 'registration/registration_form.html', locals())


def teacher_registration(request):
    title = _('Create a teacher account')
    form = TeacherRegistrationForm()
    return render(request, 'registration/registration_form.html', locals())


@login_required
def edit_profile(request):
    tab = 'personal'
    user = request.user
    blog = user.get_blog()
    msg = ''
    if request.method == 'POST' and 'personal' in request.POST:
        posta=request.POST.copy()
        profileform = ProfileForm(posta, instance=user)
        imageform = ProfilePhotoForm()
        if profileform.is_valid():
            profileform.save()
            msg = _('New user data saved')
            messages.add_message(request, messages.SUCCESS, msg, fail_silently=True)
    elif request.method == 'POST' and 'image' in request.POST:
        imageform = ProfilePhotoForm(request.POST, request.FILES)
        profileform = ProfileForm(instance=user)
        if imageform.is_valid():
            photo = handle_uploaded_file(request.FILES['avatarpic'], user)
            user.photo = photo
            user.save()
            msg = _('New photo saved')
            messages.add_message(request, messages.SUCCESS, msg, fail_silently=True)
    else:
        profileform = ProfileForm(instance=user)
        imageform = ProfilePhotoForm()
    return render(request, 'profile/edit_personal.html', locals())


@login_required
def edit_blog(request):
    tab = 'blog'
    user = request.user
    blog = user.get_blog()
    msg = ''
    if request.method == 'POST':
        form = BlogFormNoCaptcha(request.POST)
        wp_form = WPXMLForm()
        link_form = External_linkForm(request.POST)
        if form.is_valid():
            blog.name = form.cleaned_data.get('name')
            blog.tagline = form.cleaned_data.get('tagline')
            if request.FILES.get('header_image',''):
                blog.header_image = handle_uploaded_file(request.FILES['header_image'], user)
            blog.license = form.cleaned_data.get('license')
            blog.analytics_code = form.cleaned_data.get('analytics_code')
            blog.custom_html = form.cleaned_data.get('custom_html')
            blog.template = form.cleaned_data.get('template')
            blog.save()
            msg = _('New blog data saved')
        if link_form.is_valid():
            link = External_link()
            link.title = link_form.cleaned_data.get('title')
            link.url = link_form.cleaned_data.get('url')
            link.blog = blog
            link.save()
            form = BlogFormNoCaptcha(instance=blog)
            link_form = External_linkForm()
            msg = _('New link saved')
        if msg:
            messages.add_message(request, messages.SUCCESS, msg, fail_silently=True)
    else:
        form = BlogFormNoCaptcha(instance=blog)
        wp_form = WPXMLForm()
        link_form = External_linkForm()
    return render(request, 'profile/edit_blog.html', locals())


@login_required
def edit_pass(request):
    return password_change(request,post_change_redirect="/users/accounts/password/change/done/",extra_context={'blog': request.user.get_blog()})


@login_required
def pass_done(request):
    return password_change_done(request,extra_context={'blog': request.user.get_blog()})


class BlogRegistrationView(RegistrationView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if isinstance(context.get('form'), StudentRegistrationForm):
            context['title'] = _('Create a student account')
        elif isinstance(context.get('form'), TeacherRegistrationForm):
            context['title'] = _('Create a teacher account')
        return context

    def get_form_class(self):
        if 'code' in self.request.POST:
            return StudentRegistrationForm
        elif 'school' in self.request.POST:
            return TeacherRegistrationForm
        else:
            return RegistrationForm
        pass
