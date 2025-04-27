# core/serializers.py

from rest_framework import serializers
from .models import Species, Country, ObservationSG, ObservationSGSpecies, SGBird

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "code", "name"]

class SpeciesSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = Species
        fields = ["id", "species_code", "com_name", "sci_name", "image_url", "countries", "country_count"]

class ObservationSGSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationSG
        fields = [
            "id", "obs_dt", "lat", "lng", "location_name", "location_id",
            "obs_valid", "obs_reviewed", "user_display_name", "subnational1_name", "subnational2_name"
        ]

class ObservationSGSpeciesSerializer(serializers.ModelSerializer):
    species = SpeciesSerializer(read_only=True)

    class Meta:
        model = ObservationSGSpecies
        fields = ["id", "species", "how_many"]


class SGBirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SGBird
        fields = ['id', 'species_code', 'com_name', 'sci_name']