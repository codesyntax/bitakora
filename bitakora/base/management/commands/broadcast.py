from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from django.db.models import Q
from datetime import timedelta
from bitakora.utils.social import send_to_twitter
from bitakora.base.models import *

def broadcast(minutes):
    minutes=int(minutes)
    now = datetime.now()
    x_hours_ago = now - timedelta(minutes=minutes)
    articles = Article.objects.filter(Q(publish_date__gte=x_hours_ago) 
                                            & Q(publish_date__lte=now) & Q(status=CONTENT_STATUS_PUBLISHED) 
                                            & Q(shared=False)).order_by('-publish_date')
    
    for article in articles:
        send_to_twitter(article)
        article.shared = True
        article.save()

class Command(BaseCommand):
   help = 'Broadcast articles'

   def add_arguments(self, parser):
        parser.add_argument('minutes', type=int)

   def handle(self, *args, **options):
       minutes = options.get('minutes', 0)
       broadcast(minutes)