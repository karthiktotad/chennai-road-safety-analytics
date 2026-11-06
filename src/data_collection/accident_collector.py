"""
Chennai Road Accident Data Collector.
Downloads official road crash datasets from OpenCity CKAN repository:
1. Chennai Road Crashes from 1998 to 2025 (CSV & PDF)
2. Tamil Nadu Road Crashes from 1993 to 2025 (CSV & PDF)
3. Tamil Nadu District-wise Road Accidents 2021-2023 (CSV)
4. Chennai Traffic Police Jurisdictions (KML)
5. Chennai Police Jurisdictions (KML)
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests

from config.settings import RAW_ACCIDENTS_DIR, RAW_SUPPLEMENTARY_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Official OpenCity Resource URLs identified from metadata
TARGET_RESOURCES = [
    {
        "category": "accidents",
        "dataset_name": "Chennai Road Crashes Data (1998-2025)",
        "filename": "chennai_road_crashes_1998_2025.csv",
        "url": "https://data.opencity.in/dataset/2c742a2c-c559-4d9c-9987-8566aadb933c/resource/29162b87-f1a7-4011-b309-b14d904f9a7d/download/chennai-road-crashes-1998-2025.csv",
        "format": "CSV"
    },
    {
        "category": "accidents",
        "dataset_name": "Chennai Road Crashes Official Report (1998-2025)",
        "filename": "chennai_road_crashes_1998_2025_report.pdf",
        "url": "https://data.opencity.in/dataset/2c742a2c-c559-4d9c-9987-8566aadb933c/resource/b75d40f4-7f98-4183-bff2-1feeb7749afa/download/pdfpage_en_10beobtm_2026_01_23.pdf",
        "format": "PDF"
    },
    {
        "category": "accidents",
        "dataset_name": "Tamil Nadu Road Crashes Data (1993-2025)",
        "filename": "tamil_nadu_road_crashes_1993_2025.csv",
        "url": "https://data.opencity.in/dataset/2c742a2c-c559-4d9c-9987-8566aadb933c/resource/c1fe08c4-9871-4c0b-b79b-c446f24f2c03/download/tn-road-crashes-1993-2025.csv",
        "format": "CSV"
    },
    {
        "category": "accidents",
        "dataset_name": "Tamil Nadu District-wise Road Accidents (2021-2023)",
        "filename": "tamil_nadu_district_accidents_2021_2023.csv",
        "url": "https://data.opencity.in/dataset/2fc34e49-936f-4255-a4c3-1ef92f25adf3/resource/764579ad-22e0-4f27-a694-34d0d2f843ea/download/d23e7ba9-6a60-41db-b37b-62413cc72365.csv",
        "format": "CSV"
    },
    {
        "category": "supplementary",
        "dataset_name": "Chennai Traffic Police Jurisdictions Map",
        "filename": "chennai_traffic_police_jurisdictions.kml",
        "url": "https://data.opencity.in/dataset/fbc38d27-c621-42ba-ae0e-b9fa9463f394/resource/14c3bedd-bb59-49ed-ab80-c5fb93fafcd6/download/chennai_traffic_police_jurisdictions.kml",
        "format": "KML"
    },
    {
        "category": "supplementary",
        "dataset_name": "Chennai Police Jurisdictions Map",
        "filename": "chennai_police_jurisdictions.kml",
        "url": "https://data.opencity.in/dataset/fbc38d27-c621-42ba-ae0e-b9fa9463f394/resource/6a7ce9d3-0930-4647-a0ae-99ad00b5db0e/download/chennai_police_jurisdictions.kml",
        "format": "KML"
    },
    {
        "category": "supplementary",
        "dataset_name": "Chennai Bridges Infrastructure",
        "filename": "chennai_bridges.csv",
        "url": "https://data.opencity.in/dataset/4d1fc3d1-79cc-4c04-8c40-2f5e35bead60/resource/22d57250-0dd7-477c-86e5-db55844a0128/download/be75cffc-da41-4efb-b89e-6b48499ef0c5.csv",
        "format": "CSV"
    }
]


class AccidentDataCollector:
    """Retrieves and catalogs verified Chennai crash datasets."""

    def __init__(self, raw_accidents_dir=RAW_ACCIDENTS_DIR, raw_supp_dir=RAW_SUPPLEMENTARY_DIR):
        self.accidents_dir = Path(raw_accidents_dir)
        self.supp_dir = Path(raw_supp_dir)
        self.accidents_dir.mkdir(parents=True, exist_ok=True)
        self.supp_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.accidents_dir / "collection_metadata.json"

    def download_file(self, url, dest_path, dataset_name):
        """Downloads a single file with streaming and error handling."""
        headers = {"User-Agent": "Mozilla/5.0 (Academic Research; Chennai Road Safety)"}
        logger.info(f"Downloading [{dataset_name}] from {url}...")
        try:
            with requests.get(url, headers=headers, stream=True, timeout=90) as r:
                r.raise_for_status()
                with open(dest_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        if chunk:
                            f.write(chunk)
            size_kb = dest_path.stat().st_size / 1024
            logger.info(f"Downloaded {dest_path.name} ({size_kb:.2f} KB)")
            return True
        except Exception as e:
            logger.error(f"Failed to download {dataset_name}: {e}")
            return False

    def download_all(self):
        """Downloads all targeted datasets and logs metadata."""
        records = []
        for item in TARGET_RESOURCES:
            target_dir = self.accidents_dir if item["category"] == "accidents" else self.supp_dir
            dest_file = target_dir / item["filename"]

            # Avoid re-downloading if already present and non-empty
            if dest_file.exists() and dest_file.stat().st_size > 0:
                logger.info(f"File {dest_file.name} already exists ({dest_file.stat().st_size / 1024:.2f} KB). Skipping.")
                success = True
            else:
                success = self.download_file(item["url"], dest_file, item["dataset_name"])

            if success:
                records.append({
                    "dataset_name": item["dataset_name"],
                    "filename": item["filename"],
                    "category": item["category"],
                    "format": item["format"],
                    "url": item["url"],
                    "file_path": str(dest_file),
                    "file_size_bytes": dest_file.stat().st_size,
                    "download_timestamp": datetime.now().isoformat()
                })

        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump({
                "collection_timestamp": datetime.now().isoformat(),
                "total_files": len(records),
                "items": records
            }, f, indent=2)

        logger.info(f"All downloads finished. {len(records)} files verified in raw registry.")
        return records


if __name__ == "__main__":
    collector = AccidentDataCollector()
    collector.download_all()
