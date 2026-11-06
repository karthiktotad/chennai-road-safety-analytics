"""
Spatial Preprocessing & Infrastructure Cleaner.
Parses vector geometries, OpenStreetMap infrastructure nodes,
traffic police jurisdictions (KML), and spatial junctions for Chennai.
"""

import json
import re
import logging
from pathlib import Path
import pandas as pd
import numpy as np

from config.settings import (
    RAW_ROAD_DIR, RAW_SUPPLEMENTARY_DIR, PROCESSED_DATA_DIR, STUDY_AREA
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def clean_osm_junctions() -> pd.DataFrame:
    """
    Parses and cleans OpenStreetMap junction, signal, and roundabout nodes for Chennai.
    Extracts precise latitude and longitude, node IDs, and junction types.
    """
    input_path = RAW_ROAD_DIR / "chennai_junctions_signals_osm.json"
    logger.info(f"Loading OSM junctions and signals from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    elements = data.get("elements", [])
    records = []
    for el in elements:
        tags = el.get("tags", {})
        highway_tag = tags.get("highway", "unknown")
        junction_tag = tags.get("junction", "none")

        # Determine refined infrastructure node classification
        if highway_tag == "traffic_signals":
            node_type = "Traffic Signals"
        elif highway_tag == "motorway_junction" or junction_tag == "roundabout":
            node_type = "Motorway Junction / Roundabout"
        else:
            node_type = "Intersection Node"

        records.append({
            "osm_node_id": el.get("id"),
            "latitude": el.get("lat"),
            "longitude": el.get("lon"),
            "node_type": node_type,
            "highway_tag": highway_tag,
            "junction_tag": junction_tag,
            "has_traffic_signal": 1 if highway_tag == "traffic_signals" else 0
        })

    df = pd.DataFrame(records)
    # Spatial filter: verify coordinates lie within the Chennai metropolitan bounding box
    bbox = STUDY_AREA["bbox"]
    df = df[
        (df["latitude"] >= bbox["south"]) & (df["latitude"] <= bbox["north"]) &
        (df["longitude"] >= bbox["west"]) & (df["longitude"] <= bbox["east"])
    ].reset_index(drop=True)

    output_path = PROCESSED_DATA_DIR / "chennai_osm_junctions_preprocessed.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned OSM junctions ({len(df)} nodes) to {output_path}")
    return df


def clean_osm_major_roads() -> pd.DataFrame:
    """
    Parses and summarizes OpenStreetMap major road ways (motorway, trunk, primary) in Chennai.
    Extracts highway classification, road name, lanes, and approximate midpoint coordinates.
    """
    input_path = RAW_ROAD_DIR / "chennai_major_roads_osm.json"
    logger.info(f"Loading OSM major roads from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    elements = data.get("elements", [])
    records = []
    for el in elements:
        tags = el.get("tags", {})
        geom = el.get("geometry", [])

        # Compute centroid / midpoint from line coordinates if available
        if geom:
            lats = [pt["lat"] for pt in geom]
            lons = [pt["lon"] for pt in geom]
            mid_lat = np.mean(lats)
            mid_lon = np.mean(lons)
            num_pts = len(geom)
        else:
            mid_lat, mid_lon, num_pts = None, None, 0

        # Standardize lane count
        lanes_val = tags.get("lanes")
        try:
            lanes_num = int(lanes_val) if lanes_val else 2
        except ValueError:
            lanes_num = 2

        # Standardize maxspeed
        maxspeed_val = tags.get("maxspeed")
        try:
            speed_num = int(re.sub(r"[^\d]", "", str(maxspeed_val))) if maxspeed_val else None
        except ValueError:
            speed_num = None

        records.append({
            "osm_way_id": el.get("id"),
            "road_name": tags.get("name", "Unnamed Major Road"),
            "highway_class": tags.get("highway", "primary"),
            "lanes": lanes_num,
            "oneway": 1 if tags.get("oneway") == "yes" else 0,
            "maxspeed_kmh": speed_num,
            "surface": tags.get("surface", "paved"),
            "mid_latitude": mid_lat,
            "mid_longitude": mid_lon,
            "geometry_node_count": num_pts
        })

    df = pd.DataFrame(records).dropna(subset=["mid_latitude", "mid_longitude"])
    # Spatial filter for Chennai bounds
    bbox = STUDY_AREA["bbox"]
    df = df[
        (df["mid_latitude"] >= bbox["south"]) & (df["mid_latitude"] <= bbox["north"]) &
        (df["mid_longitude"] >= bbox["west"]) & (df["mid_longitude"] <= bbox["east"])
    ].reset_index(drop=True)

    output_path = PROCESSED_DATA_DIR / "chennai_osm_roads_preprocessed.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned OSM major roads ({len(df)} segments) to {output_path}")
    return df


def parse_traffic_police_jurisdictions() -> pd.DataFrame:
    """
    Parses Chennai Traffic Police Jurisdictions KML file.
    Extracts police station name, station code, taluk, TIW, and polygon centroid coordinates.
    """
    input_path = RAW_SUPPLEMENTARY_DIR / "chennai_traffic_police_jurisdictions.kml"
    logger.info(f"Parsing Traffic Police jurisdictions KML from {input_path}...")

    with open(input_path, "r", encoding="utf-8") as f:
        kml_content = f.read()

    # Parse Placemarks using regex for robustness
    placemark_blocks = re.findall(r"<Placemark.*?>(.*?)</Placemark>", kml_content, re.DOTALL)
    records = []

    for block in placemark_blocks:
        def extract_simple(name):
            m = re.search(rf'<SimpleData name="{name}">(.*?)</SimpleData>', block)
            return m.group(1).strip() if m else None

        station_name = extract_simple("police_station")
        station_code = extract_simple("police_station_code")
        taluk_name = extract_simple("taluk_name")
        tiw_name = extract_simple("tiw")

        # Extract polygon coordinates
        coord_match = re.search(r"<coordinates>(.*?)</coordinates>", block, re.DOTALL)
        if coord_match:
            coord_str = coord_match.group(1).strip()
            pairs = coord_str.split()
            lons, lats = [], []
            for p in pairs:
                parts = p.split(",")
                if len(parts) >= 2:
                    try:
                        lons.append(float(parts[0]))
                        lats.append(float(parts[1]))
                    except ValueError:
                        continue

            if lats and lons:
                centroid_lat = np.mean(lats)
                centroid_lon = np.mean(lons)
            else:
                centroid_lat, centroid_lon = None, None
        else:
            centroid_lat, centroid_lon = None, None

        if station_name:
            records.append({
                "police_station": station_name,
                "station_code": station_code,
                "taluk": taluk_name,
                "tiw": tiw_name,
                "centroid_latitude": centroid_lat,
                "centroid_longitude": centroid_lon
            })

    df = pd.DataFrame(records).dropna(subset=["centroid_latitude", "centroid_longitude"]).reset_index(drop=True)
    output_path = PROCESSED_DATA_DIR / "chennai_traffic_police_jurisdictions_preprocessed.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved parsed traffic police jurisdictions ({len(df)} zones) to {output_path}")
    return df


def clean_police_stations_registry() -> pd.DataFrame:
    """
    Cleans administrative inventory of Chennai police stations.
    Separates Traffic, Law & Order, and Crime stations by Zone and Division.
    """
    input_path = RAW_SUPPLEMENTARY_DIR / "chennai_police_stations.csv"
    logger.info(f"Loading police station inventory from {input_path}...")
    df = pd.read_csv(input_path)
    df.columns = [c.replace("\ufeff", "").strip() for c in df.columns]

    rename_map = {
        "Sl No.": "sl_no",
        "Zone": "zone",
        "Sub division": "sub_division",
        "Code": "station_code",
        "Type": "station_type",
        "Station Name": "station_name",
        "Contact No.": "contact_no"
    }
    df = df.rename(columns=rename_map)

    # Clean text columns
    for col in ["zone", "sub_division", "station_code", "station_type", "station_name"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Identify Traffic-specific police stations
    df["is_traffic_station"] = df["station_type"].str.lower().str.contains("traffic").astype(int)

    output_path = PROCESSED_DATA_DIR / "chennai_police_stations_preprocessed.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned police stations ({len(df)} stations) to {output_path}")
    return df


def run_all_spatial_preprocessing():
    logger.info("Starting spatial infrastructure preprocessing...")
    junc_df = clean_osm_junctions()
    roads_df = clean_osm_major_roads()
    tp_df = parse_traffic_police_jurisdictions()
    ps_df = clean_police_stations_registry()
    logger.info("Spatial preprocessing completed successfully.")
    return junc_df, roads_df, tp_df, ps_df


if __name__ == "__main__":
    run_all_spatial_preprocessing()

