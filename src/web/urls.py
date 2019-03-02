from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.web_index, name='index'),
    url(r'^main$', views.web_upload_file, name='upload'),
    url(r'^download$', views.download_file, name='download'),
    url(r'^status$', views.web_status, name='status'),
    url(r'^about$', views.web_about, name='about'),
    url(r'^gold$', views.download_gold, name='gold'),
    url(r'^p$', views.web_processing, name='p'),
    url(r'^download_txt$', views.download_txt, name='download_txt'),
    url(r'^download_xml$', views.download_xml, name='download_xml'),
    url(r'^download_processed$', views.download_processed, name='download_processed'),
    url(r'^tag$', views.web_tag, name='tag')
]
