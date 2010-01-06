from django.http import HttpResponse
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
            pi.thumbnail((1024,1024))
            pi.save(spec.image.path)
            return redirect(spec)
    return render_to_response('new.html',{'title': 'new specimen',
                                          'form':form},RequestContext(request))
def edit(request,specimen_id):
    specimen = get_object_or_404(Specimen, pk=specimen_id)
    form = specimen.get_edit_form()
    if 'POST' == request.method:
        form = specimen.get_edit_form(request.POST)
        if form.is_valid(): form.save()
    return render_to_response('edit.html',
                              {'title': 'editing '+specimen.name,
                               'specimen':specimen,
                               'form':form},
                               RequestContext(request))

def upload(request,specimen_id):
    specimen = get_object_or_404(Specimen, pk=specimen_id)
    if specimen.image.name:
        return redirect(specimen)
    form = specimen.get_upload_form()
    return render_to_response('upload.html',
                              {'title': 'upload '+specimen.name,
                               'specimen':specimen,
                               'form':form},
                               RequestContext(request))

def pick(request):
    form = PickForm()
    image = None
    if 'POST' == request.method:
        form = PickForm(request.POST, request.FILES)
        if form.is_valid():
            vals = form.cleaned_data
            # TODO: create new model instance and populate
            dest = os.path.join(settings.MEDIA_ROOT,'files/process/tmp.jpg') # populate file dest based on slide name or model pk
            handle_uploaded_file(request.FILES['source_img'], dest)
            # resize image before finishing
    return render_to_response('pick.html',{'form':form, 'pic': image},RequestContext(request))


from django import forms

class EdgeForm(forms.Form):
    lo = forms.FloatField(initial=90.0)
    hi = forms.FloatField(initial=100.0)

class PickForm(forms.Form):
    source_img = forms.ImageField()
    name = forms.CharField(max_length=23)
    # TODO: override clean() to enforce regex validation of name
    
    
def handle_uploaded_file(f, dest):
    dest_fh = open(dest,'wb+')
    for chunk in f.chunks():
        dest_fh.write(chunk)
    dest_fh.close()