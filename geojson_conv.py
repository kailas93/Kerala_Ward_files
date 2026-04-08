#!/usr/bin/env python3

import json
from pathlib import Path
from playwright.sync_api import sync_playwright

INPUT_JSON = "district_localbody_mapping.json"
OUTPUT_DIR = "geojson"


def save_geojson(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)


def run():
    with open(INPUT_JSON) as f:
        mapping = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        total = 0
        success = 0

        def handle_response(response):
            nonlocal success

            try:
                url = response.url

                # 🔥 FILTER: capture geojson-like responses
                if any(x in url.lower() for x in ["geojson", "ward", "boundary"]):
                    content_type = response.headers.get("content-type", "")

                    if "application/json" in content_type:
                        data = response.json()

                        # basic validation
                        if "features" in data or "geometry" in data:
                            file_path = Path(current_output_path)
                            save_geojson(data, file_path)

                            print(f"✅ Saved: {file_path}")
                            success += 1

            except Exception:
                pass

        page.on("response", handle_response)

        for district, bodies in mapping.items():
            for body in bodies:
                total += 1

                name = body["LocalBody"]
                url = body["HTMLPage"]

                safe_name = name.replace(" ", "_").replace("/", "_")
                global current_output_path
                current_output_path = f"{OUTPUT_DIR}/{district}/{safe_name}.geojson"

                print(f"[{total}] Opening: {district} - {name}")

                try:
                    page.goto(url, timeout=60000)
                    page.wait_for_timeout(5000)  # allow JS to load
                except Exception as e:
                    print(f"❌ Failed: {e}")
                    continue

        browser.close()

        print("\n=====================")
        print(f"Total: {total}")
        print(f"Extracted: {success}")
        print("=====================")


if __name__ == "__main__":
    run()
