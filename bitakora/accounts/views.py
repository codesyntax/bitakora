from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import HASH_SESSION_KEY
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from bitakora.base.models import Blog
from bitakora.base.forms import BlogFormNoCaptcha
from cssocialuser.forms import ProfileForm, ProfilePhotoForm
from cssocialuser.views import password_change
from bitakora.utils.images import handle_uploaded_file
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

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
    return render_to_response('profile/edit_personal.html', locals(), context_instance=RequestContext(request))

@login_required
def edit_blog(request):
    tab = 'blog'
    user = request.user
    blog = user.get_blog()
    msg = ''
    if request.method == 'POST':
        form = BlogFormNoCaptcha(request.POST)
        if form.is_valid():
            blog.name = form.cleaned_data.get('name')
            blog.tagline = form.cleaned_data.get('tagline')
            if request.FILES.get('header_image',''):
                blog.header_image = handle_uploaded_file(request.FILES['header_image'], user)
            blog.license = form.cleaned_data.get('license')
            blog.analytics_code = form.cleaned_data.get('analytics_code')
            blog.template = form.cleaned_data.get('template')
            blog.save()
            msg = _('New blog data saved')
            messages.add_message(request, messages.SUCCESS, msg, fail_silently=True)
    else:
        form = BlogFormNoCaptcha(instance=blog)
    return render_to_response('profile/edit_blog.html', locals(), context_instance=RequestContext(request))


@login_required
def edit_pass(request):
    return password_change(request,extra_context={'blog': request.user.get_blog()})