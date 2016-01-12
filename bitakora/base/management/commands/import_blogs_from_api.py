from django.core.management.base import BaseCommand
from django.conf import settings
from bitakora.accounts.models import BitakoraUser
from bitakora.utils.import_from_wp import import_from_wp
from bitakora.utils.images import handle_url_file
from django.contrib.auth.hashers import make_password
from django.template.defaultfilters import slugify
import json
import urllib2
import cStringIO

IMG_FORMATS = ['jpg', 'png', 'gif', 'jpeg']
BLOGS_BASE = 'http://blogak.com/'
BLOGS_JSON_URL = 'http://blogak.com/000_blogs_api'
BLOGS_PASS_JSON_URL = 'http://blogak.com/000_user_api'

def build_dict(seq, key):
    return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))

def import_blogs_from_api(match_user=None, debug=False):
    request = urllib2.unquote(BLOGS_JSON_URL)
    pass_request = urllib2.unquote(BLOGS_PASS_JSON_URL)
    
    try:
        result = urllib2.urlopen(request, timeout=5*60).read()
        data = eval(result)

        pass_result = urllib2.urlopen(pass_request, timeout=5*60).read()
        pass_data = build_dict(eval(pass_result),key='blogs')

        to_continue = match_user and True or False

        for dataset in data:

            if match_user == slugify(dataset['slug']):
                to_continue = False
            elif to_continue:
                continue    

            print slugify(dataset['slug'])

            userdata = {
                'fullname': dataset['title'],
                'email': dataset['email'],
                'bio': dataset['description'],
            }

            password = pass_data.get(dataset['slug']) and pass_data[dataset['slug']]['password']) or dataset['slug']
            if '{SSHA}' in password:
                userdata['password'] = userdata['password'].replace("{SSHA}","")
            else:
                userdata['password'] = make_password(password)
            	
            user, created = BitakoraUser.objects.get_or_create(username=slugify(dataset['slug']), defaults=userdata)

            img_url = None
            for suffix in IMG_FORMATS:
                try:
                    code  = urllib2.urlopen(BLOGS_BASE+user.username+'/image.'+suffix).code
                except:
                    code = None
                if code == 200:
                    img_url = BLOGS_BASE+user.username+'/image.'+suffix

            if img_url:
                photo = handle_url_file(img_url,user)
                user.photo = photo
                user.save()


            blog_result = urllib2.urlopen(BLOGS_BASE+dataset['slug'].replace(" ","%20")+'/downloadWordPress',timeout=5*60).read()
            import_from_wp(blog_result,user, debug)

            if match_user == slugify(dataset['slug']):
                break

    except Exception as e:
        raise e

    return True

class Command(BaseCommand):
    help = "Import blog from api"

    def handle(self, *args, **options):
        import_blogs_from_api()