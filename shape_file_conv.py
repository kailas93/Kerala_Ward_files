#!/usr/bin/env python3

import geopandas as gpd
from pathlib import Path
import pandas as pd

INPUT_DIR = Path("geojson")
OUTPUT_DIR = Path("shapefiles")


def convert_all():
    all_gdfs = []

    for district_folder in INPUT_DIR.iterdir():
        if not district_folder.is_dir():
            continue

        district = district_folder.name
        print(f"\n📂 District: {district}")

        for geojson_file in district_folder.glob("*.geojson"):
            try:
                name = geojson_file.stem  # file name without extension

                print(f"   ➜ {name}")

                gdf = gpd.read_file(geojson_file)

                # Add metadata
                gdf["district"] = district
                gdf["name"] = name

                # Ensure CRS
                if gdf.crs is None:
                    gdf.set_crs(epsg=4326, inplace=True)

                # -------------------------------
                # CREATE FOLDER PER FILE
                # -------------------------------
                out_folder = OUTPUT_DIR / district / name
                out_folder.mkdir(parents=True, exist_ok=True)

                shp_path = out_folder / f"{name}.shp"

                gdf.to_file(shp_path)

                print(f"     ✅ Saved → {shp_path}")

                all_gdfs.append(gdf)

            except Exception as e:
                print(f"     ❌ Error: {e}")

    # -------------------------------
    # OPTIONAL: MERGED FILE
    # -------------------------------
    if all_gdfs:
        print("\n🔥 Creating merged Kerala shapefile...")

        merged = gpd.GeoDataFrame(
            pd.concat(all_gdfs, ignore_index=True),
            crs="EPSG:4326"
        )

        merged.to_file(OUTPUT_DIR / "kerala_wards.shp")

        print("✅ Merged shapefile created")


if __name__ == "__main__":
    convert_all()
