# scripts/update_country_count.py

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "birdatlas.settings")
django.setup()

from core.models import Species

def update_country_counts():
    total = 0
    for sp in Species.objects.all():
        count = sp.countries.count()
        sp.country_count = count
        sp.save(update_fields=["country_count"])
        total += 1
        print(f"✅ {sp.species_code}: {count} countries")

    print(f"\n🎯 Updated {total} species with country counts.")

if __name__ == "__main__":
    update_country_counts()