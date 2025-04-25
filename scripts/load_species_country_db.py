# scripts/load_species_country.py

import os
import sys
import json
import django
from dotenv import load_dotenv

# Djangoプロジェクトへのパス設定
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django設定ロード
load_dotenv(".env.local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "birdatlas.settings")
django.setup()

from core.models import Species, Country

def load_species_and_link_countries(json_path="data/species_country_map.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        species_map = json.load(f)

    total_species = len(species_map)
    created_species = 0
    linked_relations = 0

    print(f"\n🚀 Starting import of {total_species} species...\n")

    for idx, (sp_code, info) in enumerate(species_map.items(), start=1):
        com_name = info.get("comName", "")
        sci_name = info.get("sciName", "")
        countries = info.get("countries", [])

        # Species を作成または取得
        species, created = Species.objects.get_or_create(
            species_code=sp_code,
            defaults={"com_name": com_name, "sci_name": sci_name}
        )

        if created:
            created_species += 1
            print(f"[{idx}/{total_species}] 🆕 Created species {sp_code} - {com_name}")
        else:
            print(f"[{idx}/{total_species}] ✅ Found species {sp_code} - {com_name}")

        # Country とリンク
        for cc in countries:
            country = Country.objects.filter(code=cc).first()
            if country and country not in species.countries.all():
                species.countries.add(country)
                linked_relations += 1
                print(f"    ↪️ Linked to country {cc}")

        # country_count を静的に更新
        new_count = species.countries.count()
        if species.country_count != new_count:
            species.country_count = new_count
            species.save(update_fields=["country_count"])
            print(f"    📊 Updated country_count: {new_count}")

    print("\n✅ Done.")
    print(f"🧬 Species created: {created_species}")
    print(f"🔗 Species-country relations created: {linked_relations}\n")

if __name__ == "__main__":
    load_species_and_link_countries()