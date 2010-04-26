from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.emitters import Emitter, JSONEmitter, YAMLEmitter, PickleEmitter, XMLEmitter

# overriding default content type for json emitter
#Emitter.unregister('json')
#Emitter.register('json', JSONEmitter, 'text/plain; charset=utf-8')
#Emitter.unregister('yaml')
#Emitter.register('yaml', YAMLEmitter, 'text/plain; charset=utf-8')
#Emitter.unregister('pickle')
#Emitter.register('pickle', PickleEmitter, 'text/plain; charset=utf-8')
#Emitter.unregister('xml')
#Emitter.register('xml', XMLEmitter, 'text/plain; charset=utf-8')
from .handlers import SpecimenHandler

specimen_resource = Resource(handler=SpecimenHandler)

urlpatterns = patterns('',
    url(r'^list/$', specimen_resource), 
)