from django.db import models
from django.forms import ModelForm
from string import Template

class MissingDataError(Exception):pass
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
    
    def get_name(self):
        template = Template('$date.$subtype.$population.$plant_number.$flower.$morph')
        if(self.date
           and self.subtype
           and self.population
           and self.plant_number
           and self.flower
           and self.morph):
            name = template.substitute(
               date=self.date,
               subtype=self.subtype,
               population=self.population,
               plant_number=self.plant_number,
               flower=self.flower,
               morph=self.morph
            )
            return name.upper()
        else:
            raise MissingDataError
    
    name = property(get_name)
    date = models.DateField()
    population = models.CharField(max_length=5)
    plant_number = models.CharField(max_length=6)
    flower = models.CharField(max_length=1)
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
                                   name=self.name,
                                   filename=filename)
        return path
    
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