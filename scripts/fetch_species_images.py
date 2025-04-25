# scripts/fetch_species_images.py

import os
import sys
import json
import django
import requests

# Django setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "birdatlas.settings")
django.setup()

from core.models import Species

WIKI_API = "https://en.wikipedia.org/w/api.php"
OUTPUT_JSON = "data/species_image_not_found.json"

def fetch_wikipedia_image(title):
    # Step 1: 検索してページタイトルを取得
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": title,
        "format": "json"
    }
    search_response = requests.get(WIKI_API, params=search_params)
    search_data = search_response.json()

    search_results = search_data.get("query", {}).get("search", [])
    if not search_results:
        return None

    page_title = search_results[0]["title"]

    # Step 2: ページから画像取得（リダイレクト対応）
    image_params = {
        "action": "query",
        "titles": page_title,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": 600,
        "redirects": 1
    }
    image_response = requests.get(WIKI_API, params=image_params)
    image_data = image_response.json()

    pages = image_data.get("query", {}).get("pages", {})
    for page in pages.values():
        thumbnail = page.get("thumbnail")
        if thumbnail:
            return thumbnail["source"]
    return None

def fetch_and_store_images():
    species_qs = Species.objects.filter(image_url__isnull=True)
    total = species_qs.count()
    found = 0
    not_found = []

    print(f"\n🔍 Checking {total} species for images...\n")

    for i, sp in enumerate(species_qs, start=1):
        print(f"[{i}/{total}] {sp.species_code}... ", end="")
        url = fetch_wikipedia_image(sp.sci_name) or fetch_wikipedia_image(sp.com_name)

        if url:
            sp.image_url = url
            sp.save(update_fields=["image_url"])
            print(f"✅ image found")
            found += 1
        else:
            print(f"❌ no image found")
            not_found.append({
                "species_code": sp.species_code,
                "comName": sp.com_name,
                "sciName": sp.sci_name
            })

    # JSONで保存
    if not_found:
        os.makedirs("data", exist_ok=True)
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(not_found, f, ensure_ascii=False, indent=2)
        print(f"\n📄 Missing image list saved to {OUTPUT_JSON}")

    print(f"\n✅ Done. {found}/{total} species were updated with images.\n")

if __name__ == "__main__":
    fetch_and_store_images()