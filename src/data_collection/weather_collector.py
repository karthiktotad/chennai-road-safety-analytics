"""
NASA POWER Weather Data Collector for Chennai.
Downloads daily atmospheric and meteorological indicators from the NASA POWER API.
Endpoint: https://power.larc.nasa.gov/api/temporal/daily/point
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests
import pandas as pd

from config.settings import RAW_WEATHER_DIR, STUDY_AREA

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

NASA_POWER_BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Core meteorological parameters
# PRECTOTCORR: Precipitation Corrected (mm/day)
# T2M: Temperature at 2m (C)
# T2M_MAX: Maximum Temperature at 2m (C)
# T2M_MIN: Minimum Temperature at 2m (C)
# RH2M: Relative Humidity at 2m (%)
# WS10M: Wind Speed at 10m (m/s)
# PS: Surface Pressure (kPa)
DEFAULT_PARAMETERS = ["PRECTOTCORR", "T2M", "T2M_MAX", "T2M_MIN", "RH2M", "WS10M", "PS"]


class NASAWeatherCollector:
    """Collector for NASA POWER meteorological daily data."""

    def __init__(self, lat=STUDY_AREA["center_lat"], lon=STUDY_AREA["center_lon"], output_dir=RAW_WEATHER_DIR):
        self.lat = lat
        self.lon = lon
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_daily_weather(self, start_date="20180101", end_date="20241231", parameters=None):
        """
        Query NASA POWER API for daily point observations.
        Dates formatted as YYYYMMDD.
        """
        if parameters is None:
            parameters = DEFAULT_PARAMETERS

        params_str = ",".join(parameters)
        payload = {
            "parameters": params_str,
            "community": "RE",
            "longitude": self.lon,
            "latitude": self.lat,
            "start": start_date,
            "end": end_date,
            "format": "JSON"
        }

        logger.info(f"Querying NASA POWER API for Chennai ({self.lat}, {self.lon}) from {start_date} to {end_date}...")
        try:
            response = requests.get(NASA_POWER_BASE_URL, params=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.error(f"Failed to retrieve data from NASA POWER API: {e}")
            raise

        # Save raw JSON response
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_json_file = self.output_dir / f"chennai_weather_nasa_power_{start_date}_{end_date}_{timestamp_str}.json"
        with open(raw_json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved raw JSON payload to {raw_json_file}")

        # Parse parameter series into a tabular CSV
        properties = data.get("properties", {})
        param_dict = properties.get("parameter", {})

        records = {}
        for param, date_vals in param_dict.items():
            for date_key, val in date_vals.items():
                if date_key not in records:
                    records[date_key] = {"date": date_key}
                records[date_key][param] = val

        df = pd.DataFrame(list(records.values()))
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
            df = df.sort_values("date").reset_index(drop=True)
            # NASA POWER uses -999 for missing values
            df = df.replace(-999.0, pd.NA)

            csv_file = self.output_dir / f"chennai_weather_nasa_power_daily_{start_date}_{end_date}.csv"
            df.to_csv(csv_file, index=False)
            logger.info(f"Successfully processed and saved {len(df)} daily weather records to {csv_file}")
            return csv_file, raw_json_file

        return None, raw_json_file


if __name__ == "__main__":
    collector = NASAWeatherCollector()
    collector.fetch_daily_weather(start_date="20180101", end_date="20231231")

