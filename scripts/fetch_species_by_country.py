# scripts/fetch_species_country_map.py

import os
import sys
import json
import time
import requests
from dotenv import load_dotenv

# Djangoに接続する準備（今後のために）
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(".env.local")

# APIキーと定数
API_KEY = os.getenv("EBIRD_API_KEY")
HEADERS = {"X-eBirdApiToken": API_KEY}
BASE_URL = "https://api.ebird.org/v2/product/spplist/"  # 国ごとの鳥種リスト取得
TAXO_URL = "https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json"  # 鳥種名リスト

INPUT_COUNTRIES = "data/country_list.json"
OUTPUT_JSON = "data/species_country_map.json"
RATE_SLEEP = 1.2  # レート制限対策

def get_taxonomy():
    """鳥の英名・学名を取得"""
    print("📦 Downloading taxonomy...")
    r = requests.get(TAXO_URL, headers=HEADERS)
    r.raise_for_status()
    taxo = r.json()
    return {item["speciesCode"]: {"comName": item["comName"], "sciName": item["sciName"]} for item in taxo}

def fetch_species_per_country():
    with open(INPUT_COUNTRIES, "r", encoding="utf-8") as f:
        countries = json.load(f)

    taxonomy = get_taxonomy()
    species_map = {}

    for idx, country in enumerate(countries):
        code = country["code"]
        print(f"[{idx+1}/{len(countries)}] Fetching species for {code}...")
        try:
            url = BASE_URL + code
            r = requests.get(url, headers=HEADERS)
            r.raise_for_status()
            species_list = r.json()

            for sp_code in species_list:
                if sp_code not in species_map:
                    species_map[sp_code] = {
                        "comName": taxonomy.get(sp_code, {}).get("comName", ""),
                        "sciName": taxonomy.get(sp_code, {}).get("sciName", ""),
                        "countries": []
                    }
                species_map[sp_code]["countries"].append(code)

        except Exception as e:
            print(f"❌ Error for {code}: {e}")

        time.sleep(RATE_SLEEP)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(species_map, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    if not API_KEY:
        print("❌ EBIRD_API_KEY not found in .env.local")
    else:
        fetch_species_per_country()