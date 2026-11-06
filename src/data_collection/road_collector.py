"""
OpenStreetMap Road Network Collector for Chennai.
Extracts road network, highway classes, and junction nodes using the Overpass API.
Study Area: Chennai Metropolitan Bounding Box (12.80 - 13.25 N, 80.00 - 80.35 E).
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests

from config.settings import RAW_ROAD_DIR, STUDY_AREA

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
USER_AGENT = "ChennaiRoadSafetyResearch/1.0 (academic research; contact: research@chennai-safety.edu)"


class OSMRoadNetworkCollector:
    """Collects highway geometries and road characteristics from OpenStreetMap."""

    def __init__(self, bbox=STUDY_AREA["bbox"], output_dir=RAW_ROAD_DIR):
        self.bbox = bbox
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {"User-Agent": USER_AGENT}

    def fetch_major_roads(self, highway_types=None):
        """
        Query Overpass API for Chennai major road network.
        highway_types default: motorway, trunk, primary, secondary, tertiary.
        """
        if highway_types is None:
            highway_types = "motorway|trunk|primary|secondary|tertiary"

        s, w, n, e = self.bbox["south"], self.bbox["west"], self.bbox["north"], self.bbox["east"]

        # Overpass QL query: extract major highways and associated nodes
        query = f"""
        [out:json][timeout:90];
        (
          way["highway"~"^({highway_types})$"]({s},{w},{n},{e});
        );
        out body;
        >;
        out skel qt;
        """

        logger.info(f"Querying Overpass API for Chennai major roads within bbox ({s}, {w}, {n}, {e})...")
        try:
            response = requests.post(OVERPASS_API_URL, data={"data": query}, headers=self.headers, timeout=120)
            response.raise_for_status()
            osm_data = response.json()
        except Exception as e:
            logger.error(f"Failed to retrieve OSM data from Overpass API: {e}")
            raise

        output_file = self.output_dir / "chennai_major_roads_osm.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(osm_data, f)

        num_elements = len(osm_data.get("elements", []))
        logger.info(f"Retrieved {num_elements} OSM elements (ways and nodes). Saved to {output_file}")
        return output_file

    def fetch_intersections_and_junctions(self):
        """Query Overpass API for motorway junctions and major intersections."""
        s, w, n, e = self.bbox["south"], self.bbox["west"], self.bbox["north"], self.bbox["east"]

        query = f"""
        [out:json][timeout:60];
        (
          node["highway"="motorway_junction"]({s},{w},{n},{e});
          node["highway"="traffic_signals"]({s},{w},{n},{e});
          node["junction"="roundabout"]({s},{w},{n},{e});
        );
        out body;
        """

        logger.info(f"Querying Overpass API for Chennai junctions and signals...")
        try:
            response = requests.post(OVERPASS_API_URL, data={"data": query}, headers=self.headers, timeout=90)
            response.raise_for_status()
            junction_data = response.json()
        except Exception as e:
            logger.error(f"Failed to retrieve junction data: {e}")
            raise

        output_file = self.output_dir / "chennai_junctions_signals_osm.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(junction_data, f)

        num_elements = len(junction_data.get("elements", []))
        logger.info(f"Retrieved {num_elements} junction/signal nodes. Saved to {output_file}")
        return output_file


if __name__ == "__main__":
    collector = OSMRoadNetworkCollector()
    collector.fetch_intersections_and_junctions()
