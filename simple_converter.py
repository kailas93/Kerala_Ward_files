#!/usr/bin/env python3
"""
Convert district_localbody_mapping.json to Shapefiles with metadata.

Creates shapefiles for each district containing all local bodies
as point features with complete metadata.
"""

import json
from pathlib import Path

try:
    import geopandas as gpd
    from shapely.geometry import Point
    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False
    print("Error: geopandas and shapely required")
    print("Install with: pip install geopandas shapely")
    exit(1)


#  Approximate centerpoints for each district
DISTRICT_COORDS = {
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Kollam": (8.8932, 76.6104),
    "Pathanamthitta": (9.2713, 76.7757),
    "Alappuzha": (9.4981, 76.3355),
    "Kottayam": (9.5915, 76.5215),
    "Idukki": (10.2549, 77.0375),
    "Ernakulam": (10.0436, 76.2919),
    "Thrissur": (10.5403, 76.2137),
    "Palakkad": (10.7867, 76.6444),
    "Malappuram": (11.0059, 75.9578),
    "Kozhikode": (11.2588, 75.4244),
    "Wayanad": (11.6271, 75.7821),
    "Kannur": (12.0174, 75.3305),
    "Kasaragod": (12.4758, 75.0545),
}


def create_shapefile_from_mapping():
    """Create shapefiles from the mapping JSON."""
    mapping_file = Path("./raw/district_localbody_mapping.json")
    output_dir = Path("./shapefiles")
    
    if not mapping_file.exists():
        print(f"Error: {mapping_file} not found")
        return
    
    print("Loading mapping data...")
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    total_lb = sum(len(v) for v in mapping.values())
    print(f"Found {len(mapping)} districts with {total_lb} local bodies\n")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    success = 0
    
    for district, localbodies in mapping.items():
        district_safe = district.replace(" ", "_").replace("/", "-")
        district_dir = output_dir / district_safe
        district_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Processing {district}: {len(localbodies)} local bodies")
        
        # Get district centroid
        dist_lat, dist_lon = DISTRICT_COORDS.get(district, (10.0, 76.0))
        
        # Prepare features
        properties_list = []
        geometries = []
        
        for idx, lb in enumerate(localbodies):
            lb_name = lb.get("LocalBody", "Unknown")
            html_url = lb.get("HTMLPage", "")
            
            # Spread points out slightly within the district
            # by creating a grid-like distribution
            cols_per_row = 8
            col = idx % cols_per_row
            row = idx // cols_per_row
            
            # Small offset to create grid spacing
            lat_offset = (row * 0.05) - (total_lb // (2 * cols_per_row) * 0.05)
            lon_offset = (col * 0.05) - (cols_per_row // 2 * 0.05)
            
            lat = dist_lat + lat_offset
            lon = dist_lon + lon_offset
            
            # Create point geometry
            point = Point(lon, lat)
            
            properties = {
                "name": lb_name,
                "district": district,
                "html_page": html_url,
                "id": idx + 1,
            }
            
            geometries.append(point)
            properties_list.append(properties)
        
        if geometries:
            # Create GeoDataFrame
            gdf = gpd.GeoDataFrame(
                properties_list, 
                geometry=geometries, 
                crs="EPSG:4326"
            )
            
            # Save shapefile
            output_file = district_dir / f"{district_safe}.shp"
            gdf.to_file(output_file)
            
            print(f"  ✓ Created {output_file} ({len(geometries)} features)")
            success += len(geometries)
    
    print(f"\n{'='*60}")
    print(f"SUCCESS")
    print(f"  Total features created: {success}")
    print(f"  Output directory: {output_dir}")
    print("="*60)
    print("\nEach shapefile contains local bodies as point features")
    print("with metadata including district and HTML page URL.")
    print("\nTo get actual ward boundaries:")
    print("  - Extract GeoJSON from HTML pages (which load dynamically)")
    print("  - Use Selenium or Puppeteer to render JavaScript")
    print("  - Access boundary data from a GIS server if available")


if __name__ == "__main__":
    create_shapefile_from_mapping()
