# coding=utf-8
# version:3.6.4
#

from django.urls import path, re_path
from dataview import apps


urlpatterns = [
    path('pageA/', wpi.pageA),
    path('aJaxTest/', wpi.aJaxTest),
    path('pageB/', wpi.pageB),
    path('windowclose/', wpi.windowclose)
]
