from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code

class Species(models.Model):
    species_code = models.CharField(max_length=20, unique=True)
    com_name = models.CharField(max_length=200)
    sci_name = models.CharField(max_length=200)
    countries = models.ManyToManyField(Country, related_name="species")

    def __str__(self):
        return self.species_code