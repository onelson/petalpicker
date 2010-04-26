from django.conf.urls.defaults import *
from django.views.generic import list_detail
from .models import Specimen

specimen_info = {
    "queryset" : Specimen.objects.all(),
}

urlpatterns = patterns('django.views.generic',
   url(r'list/$', list_detail.object_list, specimen_info, name='specimen_list'),
)

urlpatterns += patterns('buttercup.specimen.views',
    (r'new/$', 'new'),
    url(r'edit/(?P<specimen_id>\d+)/$', 'edit', name='edit_specimen'),
    url(r'edit/(?P<specimen_id>\d+)/upload/$', 'edit', name='upload_specimen'),
    url(r'edit/(?P<specimen_id>\d+)/do_canny/$', 'do_canny', name='do_canny'),
    url(r'edit/(?P<specimen_id>\d+)/calc_bbox/$', 'calc_bbox', name='calc_bbox'),
    url(r'edit/(?P<specimen_id>\d+)/store_scale/$', 'store_scale', name='store_scale'),
)

urlpatterns += patterns('django.views.generic.simple',
    ('$', 'redirect_to', {'url': '/specimen/list/'}),
)