#coding: utf-8

import django.forms as forms
from django.utils.translation import ugettext_lazy as _

class LawNodeForm(forms.ModelForm):
    
    def clean_parent(self):
        if 'parent' in self.cleaned_data:
            parent = self.cleaned_data['parent']
            
            if parent is not None:
                if 'node_type' in self.cleaned_data:
                    node_type = self.cleaned_data['node_type']
                else:
                    raise forms.ValidationError(_(u"Hnúturinn verður að hafa tag"))
                
                if node_type.treelevel == 1 or (parent.node_type.treelevel != (node_type.treelevel - 1)):
                    raise forms.ValidationError(_(u"%(child_node_type)s má ekki vera undir %(parent_node_type)s í lagatrénu" % 
                                                    {'child_node_type': node_type, 'parent_node_type': parent.node_type }))
                else:
                    return parent
            
                                        
