from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse
from contact_form.views import ContactFormView
from bitakora.base.models import Blog
from django.views.generic.edit import FormView
from contact_form.forms import ContactForm
from django.views.generic.detail import DetailView


class BitakoraContactFormView(ContactFormView):
    template_name = 'contact/blog_contact_form.html'

    def get_context_data(self, **kwargs):
        context = super(BitakoraContactFormView, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, slug=self.kwargs.get('slug'))
        articles = context['blog'].get_articles()[:10]
        context['categories'] = [cat for art in articles for cat in art.categories.all()][:8]
        return context

    def get_form_kwargs(self):
        kwargs = super(BitakoraContactFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        # We may also have been given a recipient list when
        # instantiated.
        if self.kwargs.get('slug') is not None:
            blog = get_object_or_404(Blog, slug=self.kwargs.get('slug'))
            kwargs.update({'recipient_list': [blog.user.email]})
        else:
            raise Http404
        return kwargs

    def get_success_url(self):
        return reverse('blog_contact_form_sent', kwargs={'slug': self.kwargs.get('slug')})


class BlogContactDetailView(DetailView):

    model = Blog

    def get_context_data(self, **kwargs):
        context = super(BlogContactDetailView, self).get_context_data(**kwargs)
        articles = context['blog'].get_articles()[:10]
        context['categories'] = [cat for art in articles for cat in art.categories.all()][:8]
        return context