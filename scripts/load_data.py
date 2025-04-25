# scripts/load_data.py

import os
import sys
import json
import django
from dotenv import load_dotenv

# プロジェクトルートを sys.path に追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django 環境設定
load_dotenv(".env.local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "birdatlas.settings")
django.setup()

from core.models import Country

def load_countries(json_path="data/country_list.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        countries = json.load(f)

    for entry in countries:
        code = entry["code"]
        name = entry["name"]
        country, created = Country.objects.get_or_create(code=code, defaults={"name": name})
        if not created:
            country.name = name
            country.save()

    print(f"✅ {len(countries)} countries loaded into the database.")

if __name__ == "__main__":
    load_countries()