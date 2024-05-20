from django.urls import path
from .views import *

app_name = "incidentModule"

urlpatterns = [
    path('incidents/', ListCreateIncident.as_view(), name='incident-list-create'),
    path('incidents/<str:id>/', IncidentRetrieveUpdateDestroyAPIView.as_view(), name='incident-detail'),
    path("search-by-Id/",SerachIncident.as_view(),name = "search by id")
]
