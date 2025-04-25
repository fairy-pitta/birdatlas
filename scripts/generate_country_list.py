# scripts/generate_country_list.py

import json
import pycountry

def generate_country_list():
    countries = [
        {"code": country.alpha_2, "name": country.name}
        for country in pycountry.countries
    ]

    with open("data/country_list.json", "w", encoding="utf-8") as f:
        json.dump(countries, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(countries)} countries saved to country_list.json")

if __name__ == "__main__":
    generate_country_list()