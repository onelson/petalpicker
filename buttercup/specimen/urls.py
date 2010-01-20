from django.conf.urls.defaults import *

urlpatterns = patterns('buttercup.specimen.views',
    (r'list/$', 'list'),
    (r'new/$', 'new'),
    url(r'edit/(?P<specimen_id>\d+)/$', 'edit', name='edit_specimen'),
    url(r'edit/(?P<specimen_id>\d+)/upload/$', 'edit', name='upload_specimen'),
    url(r'edit/(?P<specimen_id>\d+)/do_canny/$', 'do_canny', name='do_canny'),
    url(r'edit/(?P<specimen_id>\d+)/calc_bbox/$', 'calc_bbox', name='calc_bbox'),
    (r'$', 'list'),
)
