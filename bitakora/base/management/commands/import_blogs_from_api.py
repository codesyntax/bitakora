from django.core.management.base import BaseCommand
from django.conf import settings
from bitakora.accounts.models import BitakoraUser
from bitakora.utils.import_from_wp import import_from_wp
from django.contrib.auth.hashers import make_password
from django.template.defaultfilters import slugify
import json
import urllib2

BLOGS_JSON_URL = 'http://blogak.com/000_blogs_api'
BLOGS_PASS_JSON_URL = 'http://blogak.com/000_user_api'

def build_dict(seq, key):
    return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))

def import_blogs_from_api():
    request = urllib2.unquote(BLOGS_JSON_URL)
    pass_request = urllib2.unquote(BLOGS_PASS_JSON_URL)
    
    try:
        result = urllib2.urlopen(request, timeout=5*60).read()
        data = eval(result)

        pass_result = urllib2.urlopen(pass_request, timeout=5*60).read()
        pass_data = build_dict(eval(pass_result),key='blogs')

        for dataset in data:    
            
            userdata = {
                'username': slugify(dataset['slug']),
                'fullname': dataset['title'],
                'email': dataset['email'],
                'bio': dataset['description'],
                'password': pass_data.get(dataset['slug']) and pass_data[dataset['slug']]['password'] or dataset['slug'],
            }
            if '{SSHA}' in userdata['password']:
                userdata['password'] = userdata['password'].replace("{SSHA}","")
            	
            user, created = BitakoraUser.objects.get_or_create(**userdata)
            print user.username
            


            blog_result = urllib2.urlopen('http://blogak.com/'+dataset['slug'].replace(" ","%20")+'/downloadWordPress',timeout=5*60).read()
            import_from_wp(blog_result,user)

    except Exception as e:
        raise e

    return True

class Command(BaseCommand):
    help = "Import blog from api"

    def handle(self, *args, **options):
        import_blogs_from_api()