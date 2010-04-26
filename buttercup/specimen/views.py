from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.files import File
from django.conf import settings
import os, tempfile
try:
    from PIL import Image, ImageOps
except ImportError:
    import Image, ImageOps
from uuid import uuid4
from django.utils import simplejson as json

from .models import Specimen
def specimen_list(request):
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
            pi.thumbnail((780,521))
            pi.save(spec.image.path)
            return redirect(spec)
    return render_to_response('new.html',{'title': 'new specimen',
                                          'form':form},RequestContext(request))
def edit(request,specimen_id):
    specimen = get_object_or_404(Specimen, pk=specimen_id)
    try:
        specimen.edge.path
    except ValueError:
        # if edge doesn't exist, we need to generate an initial one
        specimen.generate_edgemap(save=True)
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
            specimen.generate_edgemap(lo=vals['lo'], hi=vals['hi'], save=True)
    if request.is_ajax():
        return HttpResponse()        
    return redirect(specimen)

def calc_bbox(request, specimen_id):
    if not request.is_ajax() or not 'POST' == request.method: return HttpResponseServerError()
    
    x = int(request.POST['x'])
    x2 = int(request.POST['x2'])
    y = int(request.POST['y'])
    y2 = int(request.POST['y2'])
    w = int(request.POST['w'])
    h = int(request.POST['h'])
    
    specimen = get_object_or_404(Specimen, pk=specimen_id)
    crop = ImageOps.grayscale(Image.open(specimen.edge.path).crop((x,y,x2,y2)))
    
    (width,height) = crop.size
    im = crop.load()
    
    pix = []
    for i in range(0,width):
        for j in range(0,height):
            if 0 < im[i,j]: pix.append((i,j))
    unzipped = zip(*pix)
    x = list(unzipped[0])
    y = list(unzipped[1])
    x.sort()
    y.sort()
    bbox = {'x': x[0],
            'y': y[0],
            'x2': x[-1],
            'y2': y[-1],
            'w': x[-1]-x[0],
            'h': y[-1]-y[0]}
    bbox['max'] = max(bbox['w'],bbox['h'])
    bbox['radius'] = bbox['max']/2
    if specimen.scale: 
        bbox['scale'] = specimen.scale
        bbox['scaled_radius'] = bbox['scale']*bbox['radius']
    specimen.circle_radius = bbox['radius']
    specimen.save()
    return HttpResponse(json.dumps(bbox), content_type='text/javascript')

def store_scale(request, specimen_id):
    if not request.is_ajax() or not 'POST' == request.method: 
        return HttpResponseServerError()
    scale = float(request.POST['scale'])
    specimen = get_object_or_404(Specimen, pk=specimen_id)
    specimen.scale = scale
    specimen.save()
    return HttpResponse()
    
from django import forms
class EdgeForm(forms.Form):
    lo = forms.FloatField(initial=90.0)
    hi = forms.FloatField(initial=700.0)
