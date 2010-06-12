from django.db import models
from django.forms import ModelForm
from django.db.models.signals import pre_save
from django.core.files import File
from django.conf import settings
from string import Template

import os, subprocess, tempfile
from uuid import uuid4

class MissingDataError(Exception):pass

def sh_escape(s):
   return "'" + s.replace("'", "'\\''") + "'"
def specimen_image_dst(instance, filename):
    return instance.get_image_dir(filename)

class Specimen(models.Model):
    
    SUBTYPE_CHOICES = (
        ('c', 'caroliniana'),
        ('h', 'hybrid'),
        ('v', 'viridis')
    )
    
    MORPH_CHOICES = (
        ('d', 'deformo'),
        ('h', 'homo'),
        ('l', 'long'),
        ('s', 'short')        
    )
    
    name = models.CharField(max_length=255, editable=False, unique=True) 
    date = models.DateField()
    population = models.CharField(max_length=5)
    plant_number = models.CharField(max_length=6)
    flower = models.CharField(max_length=1, blank=True)
    subtype = models.CharField(max_length=1, choices=SUBTYPE_CHOICES)
    morph = models.CharField(max_length=1, choices=MORPH_CHOICES)
    notes = models.TextField(blank=True)
    # Images
    image = models.FileField(upload_to=specimen_image_dst, null=True)
    edge = models.FileField(upload_to=specimen_image_dst, blank=True, editable=False)
    scale = models.FloatField(blank=True, null=True, editable=False)
    # Geometry data
    flower_area = models.FloatField(null=True, editable=False)
    flower_perimeter = models.FloatField(null=True, editable=False)
    circle_radius = models.FloatField(null=True, editable=False)
    circle_perimeter = models.FloatField(null=True, editable=False)
    circle_area = models.FloatField(null=True, editable=False)
    
    def get_radius(self):
        r = self.circle_radius
        if self.scale:
           r = r * self.scale
        return r
    
    @staticmethod
    def get_new_form(*args, **kwargs):
        return NewSpecimenForm(*args, **kwargs)
    def get_edit_form(self, *args, **kwargs):
        return EditSpecimenForm(instance=self, *args, **kwargs)
    @models.permalink
    def get_absolute_url(self):
        return ('edit_specimen',(),{'specimen_id': self.pk})
    def get_image_dir(self, filename=''):
        template = Template('files/slides/$date/$population/$name/$name.$filename')
        path = template.substitute(date=self.date,
                                   population=self.population,
                                   name=get_name(self),
                                   filename=filename)
        return path
    def generate_edgemap(self, lo=90.0, hi=700.0, ap=3, save=False):
        hi = str(hi)
        lo = str(lo)
        ap = str(ap)
        infile = self.image.path
        outfile = os.path.join(os.path.join(tempfile.gettempdir(),str(uuid4())+'.jpg'))
        cmd = ' '.join(['python2.6',os.path.join(settings.PROJECT_ROOT, 'specimen','process.py'),sh_escape(infile), sh_escape(outfile), lo, hi, ap])
        subprocess.check_call(cmd, shell=True)
        tmpfile = File(open(outfile,'rb'))
        try:
            self.edge.path
            self.edge.delete(save=save)
        except ValueError:
            # if accessing edge.path raises ValueError, there is no file to delete
            pass
        self.edge.save('edge.jpg',tmpfile,save=save)
        tmpfile.close()
        os.remove(outfile)

def get_name(instance):
    template = Template('$date.$subtype.$population.$plant_number$flower.$morph')
    if(instance.date
       and instance.subtype
       and instance.population
       and instance.plant_number
       and instance.morph):
        name = template.substitute(
           date=instance.date,
           subtype=instance.subtype,
           population=instance.population,
           plant_number=instance.plant_number,
           flower=instance.flower,
           morph=instance.morph
        )
        return name.replace(' ','').upper()
    else:
        raise MissingDataError

def generate_name(sender, instance, **kwargs):
    if not instance.pk:
        instance.name = get_name(instance)
def sanatize_specimen(sender, instance, **kwargs):
    if not instance.pk:
        instance.population = ''.join(instance.population.split())

pre_save.connect(sanatize_specimen, sender=Specimen)    
pre_save.connect(generate_name, sender=Specimen)

class NewSpecimenForm(ModelForm):
    class Meta:
        model = Specimen
        fields = (
          'date',
          'population',
          'plant_number',
          'flower',
          'subtype',
          'morph',
          'image',
        )
        
class EditSpecimenForm(ModelForm):
    class Meta:
        model = Specimen
        exclude = (
          'date',
          'population',
          'plant_number',
          'flower',
          'subtype',
          'morph',
          'image',
        )