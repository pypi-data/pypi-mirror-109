from django.urls import path, re_path

from .views import AutoconfigView, AutodiscoverView

urlpatterns = [
    path('mail/config-v1.1.xml', AutoconfigView.as_view()),
    re_path(
        r'^[aA]utodiscover/[aA]utodiscover.xml',
        AutodiscoverView.as_view(),
    ),
]
