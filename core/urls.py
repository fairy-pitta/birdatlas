# core/urls.py

from django.urls import path
from .views import (
    SpeciesListView, SpeciesDetailView, SpeciesObservationSGView,
    CountryListView, CountrySpeciesListView,
    ObservationSGListView, ObservationSGSpeciesListView,
    SGBirdListView, SGBirdDetailView,
    SGBirdDateObservationView
)

urlpatterns = [
    path('species/', SpeciesListView.as_view(), name='species-list'),
    path('species/<str:species_code>/', SpeciesDetailView.as_view(), name='species-detail'),
    path('species/<str:species_code>/observationsg/', SpeciesObservationSGView.as_view(), name='species-observationsg'),

    path('countries/', CountryListView.as_view(), name='country-list'),
    path('countries/<str:country_code>/species/', CountrySpeciesListView.as_view(), name='country-species-list'),

    path('observationsg/', ObservationSGListView.as_view(), name='observationsg-list'),
    path('observationsg/<int:pk>/species/', ObservationSGSpeciesListView.as_view(), name='observationsg-species-list'),
    path('sgbirds/', SGBirdListView.as_view(), name='sgbird-list'),
    path('sgbirds/<str:species_code>/', SGBirdDetailView.as_view(), name='sgbird-detail'),
    path('sgbirdsdate', SGBirdDateObservationView.as_view(), name='sgbirdsdate'),
]