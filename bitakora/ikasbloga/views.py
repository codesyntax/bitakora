from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bitakora.base.models import Blog
from bitakora.ikasbloga.models import School
from bitakora.ikasbloga.models import Room
from bitakora.base.models import Article
from bitakora.base.models import Comment
from bitakora.ikasbloga.forms import SchoolForm
from bitakora.ikasbloga.forms import RoomForm
from bitakora.utils.text import code_generator
from django.utils.translation import ugettext_lazy as _


def index(request):
    schools = School.objects.all()
    return render(request, 'ikasbloga/index.html', locals())


@login_required
def dashboard(request, slug):
    school = get_object_or_404(School, slug=slug)
    gelak = Room.objects.filter(school=school)
    blogs = Blog.objects.filter(room__in=gelak)
    articles = Article.objects.filter(blog__in=blogs)
    comments = Comment.objects.filter(parent__blog__in=blogs)
    return render(request, 'ikasbloga/dashboard.html', locals())


@login_required
def edit_school(request):
    tab = 'school'
    user = request.user
    school = user.school
    rooms = Room.objects.filter(school=school)
    msg = ''
    if request.method == 'POST':
        if 'school' in request.POST:
            form = SchoolForm(request.POST, instance=school)
            roomform = RoomForm()
        else:
            roomform = RoomForm(request.POST)
            form = SchoolForm(instance=school)
        if form.is_valid() and 'school' in request.POST:
            form.save()
            msg = _('New school data saved')
            messages.add_message(request, messages.SUCCESS, msg, fail_silently=True)
        elif roomform.is_valid():
            room = roomform.save(commit=False)
            room.school = school
            room.code = code_generator()
            room.save()
            msg = _('New room data saved')
            messages.add_message(request, messages.SUCCESS, msg, fail_silently=True)
            roomform = RoomForm()
    else:
        form = SchoolForm(instance=school)
        roomform = RoomForm()
    return render(request, 'profile/edit_school.html', locals())
