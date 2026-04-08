# Kerala Ward Files

Prepared for: Climate Leaders Action Network (CLAN)

## File Descriptions

- **README.md** - This file with project documentation
- **scrapper.py** - Downloads fresh district-localbody mapping data from wardmap.ksmart.live
- **geojson_conv.py** - Extracts GeoJSON data from ward mapping HTML pages using Playwright
- **shape_file_conv.py** - Converts GeoJSON files to shapefiles for each district

## Data Files

- **raw/district_localbody_mapping.json** - Downloaded mapping data with district and local body information

## Output Directories

- **shapefiles/** - Contains generated shapefiles for each district (Alappuzha, Ernakulam, etc.)
  - Each district folder contains: .shp, .shx, .dbf, .prj files

