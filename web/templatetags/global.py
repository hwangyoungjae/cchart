# -*- encoding:utf8 -*-
from django.template import Library, Context, Node
from django.template.loader import get_template
from web.models import *
from cchart import settings
import os

register = Library()

@register.tag(name='BASEURL')
def do_BASEURL(parser, token):
    tokens = token.split_contents()
    return BASEURL(tokens)
class BASEURL(Node):
    def __init__(self, *args):
        self.args = args
    def render(self, context):
        return getattr(settings, 'BASEURL', 'False')

@register.tag(name='URL')
def do_URL(parser, token):
    tokens = token.split_contents()
    nodelist = parser.parse(('ENDURL',))
    parser.delete_first_token()
    return URL(tokens, nodelist)
class URL(Node):
    def __init__(self, *args):
        self.tokens = args[0]
        self.nodelist = args[1]
    def render(self, context):
        node = self.nodelist.render(context)
        return os.path.join(getattr(settings, 'BASEURL', 'False'),node.strip().lstrip('/'))