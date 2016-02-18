from lxml import etree
import sys
from cStringIO import StringIO
from django.template.defaultfilters import slugify
from bitakora.utils.text import clean_html, make_responsive
from bitakora.base.models import Article, Blog, Comment, Category, CONTENT_STATUS_DRAFT, COMMENT_STATUS_VISIBLEADMIN
from datetime import datetime
from os.path import basename, normpath

def import_from_wp(file_content, user, debug=False):
    tree = etree.parse(StringIO(file_content))
    root = tree.getroot()

    try:
        for blognode in root.findall('channel'):
            if Blog.objects.filter(user=user).exists():
                blog = Blog.objects.get(user=user).delete()
                
            blogdata = {
                'name': blognode.find('title').text or user.username,
                'slug': user.username,
                'tagline': blognode.find('description').text and blognode.find('description').text[:200],
                'user': user,
            }
            blog = Blog(**blogdata)
            blog.save()

            for art in blognode.findall('item'):
                article = Article()
                article.title = art.find('title').text and art.find('title').text[:200] or art.find('link').text[art.find('link').text.rfind('/')+1:200]
                article.slug = basename(normpath(art.find('link').text))
                article.text = make_responsive(clean_html(art.find('content:encoded', root.nsmap).text))
                article.publish_date = datetime.strptime(art.find('wp:post_date', root.nsmap).text, "%Y-%m-%d %H:%M:%S")
                if art.find('wp:status', root.nsmap).text != 'publish':
                    article.status = CONTENT_STATUS_DRAFT
                if art.find('wp:comment_status', root.nsmap).text != 'open':
                    article.allow_comments = False
                article.blog = blog

                if debug:
                    print article.title

                article.shared = True
                article.save()

                for cmt in art.findall('wp:comment', root.nsmap):
                    cmtdata = {
                        'nickname': cmt.find('wp:comment_author', root.nsmap).text,
                        'email':  cmt.find('wp:comment_author_email', root.nsmap).text,
                        'url': cmt.find('wp:comment_author_url', root.nsmap).text,
                        'parent': article,
                        'text': cmt.find('wp:comment_content', root.nsmap).text,
                        'status': cmt.find('wp:comment_approved', root.nsmap).text == '1' and 1 or COMMENT_STATUS_VISIBLEADMIN,
                        'publish_date': datetime.strptime(cmt.find('wp:comment_date', root.nsmap).text, "%Y-%m-%d %H:%M:%S")
                    }
                    comment = Comment(**cmtdata)
                    comment.save()

                for cat in art.findall('category'):
                    if cat.text:
                        catdata = {
                            'title': cat.text,
                            'slug': slugify(cat.text),
                        }
                        category, created = Category.objects.get_or_create(**catdata)
                        article.categories.add(category)
            return blog
    except Exception as e:
        raise Exception, "The code is buggy: %s" % e, sys.exc_info()[2]

