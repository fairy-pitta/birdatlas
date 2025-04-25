# scripts/fetch_observations_to_db.py

import os
import sys
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Django環境準備
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "birdatlas.settings")
import django
django.setup()

from core.models import ObservationSG, ObservationSGSpecies, Species
from django.db.utils import IntegrityError

# .env.local 読み込み
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env.local")
load_dotenv(dotenv_path=dotenv_path)

# -------- Configuration -------- #
API_KEY = os.getenv("EBIRD_API_KEY")
REGION = "SG"
START_DATE = datetime(2000, 1, 1)
END_DATE = datetime.now()
RATE_SLEEP = 0.5  # seconds

# -------- Main Fetch Loop -------- #
current = START_DATE
total_new = 0

print(f"🚀 Starting eBird observation sync for region: {REGION}")

while current <= END_DATE:
    dstr = current.strftime("%Y-%m-%d")
    url = (
        f"https://api.ebird.org/v2/data/obs/{REGION}/historic/"
        f"{current.year}/{current.month}/{current.day}"
    )

    try:
        r = requests.get(url, headers={"X-eBirdApiToken": API_KEY})
        r.raise_for_status()
        rows = r.json()
    except Exception as e:
        print(f"[{dstr}] 🔴 Error: {e}")
        current += timedelta(days=1)
        time.sleep(2)
        continue

    added = 0
    for obs in rows:
        sp_code = obs.get("speciesCode")
        species = Species.objects.filter(species_code=sp_code).first()
        if not species:
            print(f"❌ Species not found in DB: {sp_code}")
            continue  # 未登録speciesはスキップ

        obs_dt_raw = obs.get("obsDt")
        obs_dt = datetime.fromisoformat(obs_dt_raw).date() if obs_dt_raw else None
        lat = obs.get("lat")
        lng = obs.get("lng")

        if not (obs_dt and lat and lng):
            continue  # 必須フィールドなかったらスキップ

        try:
            # 観察イベント（ObservationSG）を作成 or 取得
            observation, created = ObservationSG.objects.get_or_create(
                obs_dt=obs_dt,
                lat=lat,
                lng=lng,
                defaults={
                    "location_name": obs.get("locationName"),
                    "location_id": obs.get("locID") or obs.get("locationID"),
                    "obs_valid": obs.get("obsValid", True),
                    "obs_reviewed": obs.get("obsReviewed", False),
                    "user_display_name": obs.get("userDisplayName"),
                    "subnational1_name": obs.get("subnational1Name"),
                    "subnational2_name": obs.get("subnational2Name"),
                }
            )

            # 種情報（ObservationSGSpecies）を追加
            ObservationSGSpecies.objects.get_or_create(
                observation=observation,
                species=species,
                defaults={
                    "how_many": obs.get("howMany"),
                }
            )

            added += 1

        except IntegrityError:
            continue  # 重複などはスキップ

    print(f"[{dstr}] API:{len(rows):>3}  saved:{added:>3}  total:{total_new + added:>6}")
    total_new += added
    current += timedelta(days=1)
    time.sleep(RATE_SLEEP)

print(f"\n✅ Complete. Total new records added: {total_new}")