#!/usr/bin/env python3
"""
Download Kerala ward delimitation mapping data from wardmap.ksmart.live

This script downloads the district_localbody_mapping.json which contains
all 14 districts and 1,034 local bodies in Kerala with their corresponding
HTML page URLs on the ward mapping platform.

Usage:
    python3 main.py

Output:
    - raw/district_localbody_mapping.json (0.15 MB)

Next Steps:
    After downloading the mapping data, use:
    - simple_converter.py : Convert mapping to point-based shapefiles
    - ward_map_scrapper.py : Extract GeoJSON from HTML pages
"""

import json
from pathlib import Path

import requests

BASE_URL = "https://wardmap.ksmart.live"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}


def download_mapping_json():
    """
    Download the district_localbody_mapping.json from wardmap.ksmart.live
    
    Returns:
        dict: Parsed JSON data or None if download fails
    """
    url = f"{BASE_URL}/files/district_localbody_mapping.json"
    
    try:
        print(f"Downloading mapping data from {url}...")
        r = requests.get(url, headers=HEADERS, timeout=60)
        r.raise_for_status()
        
        data = r.json()
        print(f"✓ Successfully downloaded mapping data")
        print(f"  Districts: {len(data)}")
        total_lbs = sum(len(v) for v in data.values())
        print(f"  Local Bodies: {total_lbs}")
        
        return data
    except Exception as e:
        print(f"✗ Failed to download mapping data: {e}")
        return None


def save_mapping_json(data, output_path):
    """
    Save mapping data to JSON file
    
    Args:
        data (dict): Mapping data to save
        output_path (Path): Where to save the file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        file_size = output_path.stat().st_size / (1024 * 1024)  # MB
        print(f"✓ Saved mapping data to {output_path}")
        print(f"  File size: {file_size:.2f} MB")
        return True
    except Exception as e:
        print(f"✗ Failed to save mapping data: {e}")
        return False


def main():
    """
    Main function: Download and save the district_localbody_mapping.json
    """
    print("="*60)
    print("Kerala Ward Data Mapper - Data Download Script")
    print("="*60)
    print()
    
    # Download mapping data
    mapping_data = download_mapping_json()
    if not mapping_data:
        print("\nAborted: Could not download mapping data")
        return False
    
    # Save to file
    output_dir = Path('./raw')
    output_path = output_dir / 'district_localbody_mapping.json'
    
    if not save_mapping_json(mapping_data, output_path):
        print("\nAborted: Could not save mapping data")
        return False
    
    print()
    print("="*60)
    print("✓ SUCCESS")
    print("="*60)
    print()
    print("Next Steps:")
    print()
    print("1. Convert to Shapefiles (Point-based):")
    print("   python3 simple_converter.py")
    print()
    print("2. Extract Ward Boundaries (Advanced):")
    print("   python3 ward_map_scrapper.py")
    print()
    print("3. Discover API Endpoints:")
    print("   python3 discover_api.py")
    print()
    print(f"Mapping data saved: {output_path}")
    print()
    
    return True


if __name__ == "__main__":
    main()