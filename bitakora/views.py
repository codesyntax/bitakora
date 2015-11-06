from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    h = {}
    return render_to_response('index.html', h, context_instance=RequestContext(request))
  
