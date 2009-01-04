 #coding: utf-8
from django.contrib import admin

from laws.models import Laws, NodeType, LawNode
from laws.forms import LawNodeForm
    
for model in [Laws, NodeType]:
    admin.site.register(model) 
    
class LawNodeAdmin(admin.ModelAdmin):
    form = LawNodeForm
    exclude = ['content_html']
    
admin.site.register(LawNode, LawNodeAdmin)