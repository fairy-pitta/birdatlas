# core/views.py

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from .models import Species, Country, ObservationSG, ObservationSGSpecies, SGBird
from .serializers import SpeciesSerializer, CountrySerializer, ObservationSGSerializer, ObservationSGSpeciesSerializer, SGBirdSerializer

# Species一覧・Species詳細
class SpeciesListView(generics.ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

class SpeciesDetailView(generics.RetrieveAPIView):
    lookup_field = 'species_code'
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

# 🆕 SpeciesCodeでObservationSGを取得する
class SpeciesObservationSGView(generics.ListAPIView):
    serializer_class = ObservationSGSerializer

    def get_queryset(self):
        species_code = self.kwargs['species_code']
        start_date = parse_date(self.request.query_params.get('start'))
        end_date = parse_date(self.request.query_params.get('end'))

        observations = ObservationSG.objects.filter(
            observed_species__species__species_code=species_code
        ).distinct()

        if start_date:
            observations = observations.filter(obs_dt__gte=start_date)
        if end_date:
            observations = observations.filter(obs_dt__lte=end_date)

        return observations

# Country一覧・CountryにいるSpecies一覧
class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountrySpeciesListView(generics.ListAPIView):
    serializer_class = SpeciesSerializer

    def get_queryset(self):
        country_code = self.kwargs['country_code']
        return Species.objects.filter(countries__code=country_code)

# ObservationSG一覧・ObservationSGにいるSpecies一覧
class ObservationSGListView(generics.ListAPIView):
    queryset = ObservationSG.objects.all()
    serializer_class = ObservationSGSerializer

class ObservationSGSpeciesListView(generics.ListAPIView):
    serializer_class = ObservationSGSpeciesSerializer

    def get_queryset(self):
        observation_id = self.kwargs['pk']
        return ObservationSGSpecies.objects.filter(observation_id=observation_id)
    


class SGBirdListView(generics.ListAPIView):
    queryset = SGBird.objects.all()
    serializer_class = SGBirdSerializer

class SGBirdDetailView(generics.RetrieveAPIView):
    queryset = SGBird.objects.all()
    serializer_class = SGBirdSerializer
    lookup_field = 'species_code'

class SGBirdDateObservationView(APIView):
    def get(self, request, *args, **kwargs):
        species_code = request.query_params.get('species')
        start_date = parse_date(request.query_params.get('date'))
        end_date = parse_date(request.query_params.get('end'))

        qs = ObservationSG.objects.all()

        if species_code:
            qs = qs.filter(observed_species__species__species_code=species_code).distinct()

        if start_date:
            qs = qs.filter(obs_dt__gte=start_date)

        if end_date:
            qs = qs.filter(obs_dt__lte=end_date)

        serializer = ObservationSGSerializer(qs, many=True)
        return Response(serializer.data)