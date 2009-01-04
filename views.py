#coding: utf-8

from django.views.generic.list_detail import object_detail
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext


from laws.models import Laws
from student.models import Schoolyear

def show_laws(request, schoolyear_starts, schoolyear_ends):
    context = {}
    schoolyear = get_object_or_404(Schoolyear, starts__year = schoolyear_starts, ends__year = schoolyear_ends)
    context['schoolyear'] = schoolyear
    context['laws'] = get_object_or_404(Laws, schoolyear = schoolyear)
    return render_to_response('laws/laws_base.html', context , context_instance = RequestContext(request))