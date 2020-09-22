from django.conf.urls import url
from . import views
# "http://127.0.0.1:8000/v1/topics/modify/qqqqq/tid


urlpatterns = [
    #http://127.0.0.1/v1/topics/<author>
    url(r'^/(?P<author_id>[\w]{1,11})$',views.topics),
    url(r'^/modify/(?P<username>\w+)/(?P<tid>\d+)',views.modify)
]