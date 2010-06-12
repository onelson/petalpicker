from piston.handler import AnonymousBaseHandler, BaseHandler
from piston.utils import rc
from buttercup.specimen.models import Specimen

class SpecimenHandler(AnonymousBaseHandler):
    model = Specimen
    exclude = ('id', 'image', 'edge')
    allowed_methods = ('GET')