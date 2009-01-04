#coding: utf-8

from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

register = template.Library()

PERMALINK_TEXT = _(u"Fastur hlekkur á þessa klausu í lögunum")

def get_law_tree(rootnodes):
    """
    Usage:  {% get_law_tree rootnodes %}
    Before: rootnodes is a queryset of LawNode objects
    After:  A complete law tree has been rendered
    """
    rendered_trees = []
    for node in rootnodes:
        rendered_trees.append(render_tree(node))
    
    return mark_safe(render_to_string('snippets/law_tree.html', { 'trees': rendered_trees }))
        
    
    
def render_tree(rootnode):
    """
    Usage:  rendered_tree = render_tree(rootnode)
    After:  rendered_tree is a html rendering of rootnode and all of it's children
    """
    if not rootnode.has_children():
        return render_to_string('snippets/law_subtree.html', { 'node': rootnode ,'permalink_text': PERMALINK_TEXT })
    else:
        subtrees = []
        for childnode in rootnode.children.all():
            subtrees.append(render_tree(childnode))
        return render_to_string('snippets/law_subtree.html', { 'node': rootnode, 'subtrees': subtrees, 'permalink_text': PERMALINK_TEXT})

register.simple_tag(get_law_tree) 

 
