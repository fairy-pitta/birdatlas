from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Species(models.Model):
    species_code = models.CharField(max_length=20, unique=True)
    com_name = models.CharField(max_length=200)
    sci_name = models.CharField(max_length=200)
    countries = models.ManyToManyField(Country, related_name="species")
    country_count = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.com_name
    

class SGObservation(models.Model):
    species_code = models.ForeignKey(on_delete=models.CASCADE, related_name='observations', to='core.species')
    com_name = models.CharField(max_length=200)
    sci_name = models.CharField(max_length=200)
    obs_dt = models.DateField()
    how_many = models.IntegerField(null=True, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    location_name = models.CharField(max_length=255, null=True, blank=True)
    location_id = models.CharField(max_length=100, null=True, blank=True)
    obs_valid = models.BooleanField(default=True)
    obs_reviewed = models.BooleanField(default=False)
    user_display_name = models.CharField(max_length=100, null=True, blank=True)
    subnational1_name = models.CharField(max_length=100, null=True, blank=True)
    subnational2_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ("obs_dt", "species_code", "lat", "lng")

    def __str__(self):
        return f"{self.com_name} on {self.obs_dt}"
    

class ObservationSG(models.Model):
    obs_dt = models.DateField()
    lat = models.FloatField()
    lng = models.FloatField()
    location_name = models.CharField(max_length=255, null=True, blank=True)
    location_id = models.CharField(max_length=100, null=True, blank=True)
    obs_valid = models.BooleanField(default=True)
    obs_reviewed = models.BooleanField(default=False)
    user_display_name = models.CharField(max_length=100, null=True, blank=True)
    subnational1_name = models.CharField(max_length=100, null=True, blank=True)
    subnational2_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ("obs_dt", "lat", "lng")

    def __str__(self):
        return f"ObservationSG {self.obs_dt} at ({self.lat}, {self.lng})"


class ObservationSGSpecies(models.Model):
    observation = models.ForeignKey(ObservationSG, on_delete=models.CASCADE, related_name="observed_species")
    species = models.ForeignKey('Species', on_delete=models.CASCADE, related_name="observation_sg_species")
    how_many = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.species.com_name} seen at {self.observation}"
    
class SGBird(models.Model):
    species_code = models.CharField(max_length=50, unique=True)
    com_name = models.CharField(max_length=200)
    sci_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.com_name} ({self.sci_name})"