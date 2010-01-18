from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.files import File
from django.conf import settings
import os
from PIL import Image
from uuid import uuid4

from .models import Specimen
def list(request):
    specs = Specimen.objects.all()
    return render_to_response('list.html',{'title': 'specimen list',
                                           'specimens': specs},RequestContext(request))
def new(request):
    form = Specimen.get_new_form()
    if 'POST' == request.method:
        form = Specimen.get_new_form(request.POST, request.FILES)
        if form.is_valid():
            vals = form.cleaned_data
            im = vals.pop('image')
            spec = Specimen.objects.create(**vals)
            spec.image.save('original.jpg', im, save=True)
            pi = Image.open(spec.image.path)
            pi.thumbnail((760,508))
            pi.save(spec.image.path)
            return redirect(spec)
    return render_to_response('new.html',{'title': 'new specimen',
                                          'form':form},RequestContext(request))
def edit(request,specimen_id):
    specimen = get_object_or_404(Specimen, pk=specimen_id)
    form = specimen.get_edit_form()
    edge_form = EdgeForm()
    if 'POST' == request.method:
        form = specimen.get_edit_form(request.POST)
        if form.is_valid(): form.save()
    return render_to_response('edit.html',
                              {'title': 'editing '+specimen.name,
                               'specimen':specimen,
                               'form':form,
                               'edge_form':edge_form},
                               RequestContext(request))

def do_canny(request, specimen_id):
    specimen = get_object_or_404(Specimen, pk=specimen_id)
    if 'POST' == request.method:
        form = EdgeForm(request.POST)
        if form.is_valid(): 
            vals = form.cleaned_data
            from . import process
            infile = specimen.image.path
            outfile = os.path.join(os.path.join(os.getenv('TMP'),str(uuid4())+'.jpg'))
            process.DoCanny(infile,outfile,vals['hi'],vals['lo'])
            tmpfile = File(open(outfile,'rb'))
            try:
                specimen.edge.path
                specimen.edge.delete(save=True)
            except ValueError:
                # if accessing edge.path raises ValueError, there is no file to delete
                pass
            specimen.edge.save('edge.jpg',tmpfile,save=True)
            tmpfile.close()
            os.remove(outfile)
    return redirect(specimen)

from django import forms
class EdgeForm(forms.Form):
    lo = forms.FloatField(initial=250.0)
    hi = forms.FloatField(initial=750.0)