import string
import random
import re
import bleach

REMOVE_TAGS = ["font", "span", "style"]
REMOVE_ATTRIBUTES = ["dir", "style", "class"]

# EMBED_TYPES = ["iframe","embed","video","object"]
# EMBED_RESPONSIVE = '<div class="embed-responsive embed-responsive-16by9">'


def clean_html(text):
    outstr = bleach.clean(text, tags=REMOVE_TAGS)
    for attr in REMOVE_ATTRIBUTES:
        for rm in re.findall(' '+attr+'=".*?"', outstr):
            outstr = outstr.replace(rm, '')
    return outstr


def make_responsive(text):
    for rpl in re.findall('<img ', text):
        text = text.replace(rpl, '<img class="img-responsive" ')
    # for emb_type in EMBED_TYPES:
    #    text = text.replace('<'+emb_type, EMBED_RESPONSIVE+'<'+emb_type).replace('</'+emb_type+'>','</'+emb_type+'></div>')
    return text

def code_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))