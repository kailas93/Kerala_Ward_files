# Kerala Ward Files

## File Descriptions

- **README.md** - This file with project documentation
- **main.py** - Downloads fresh district-localbody mapping data from wardmap.ksmart.live
- **simple_converter.py** - Converts mapping JSON to point-based shapefiles for each district
- **visualize_shapefiles.ipynb** - Jupyter notebook for interactive shapefile visualization

## Data Files

- **raw/district_localbody_mapping.json** - Downloaded mapping data with district and local body information

## Output Directories

- **shapefiles/** - Contains generated shapefiles for each district (Alappuzha, Ernakulam, etc.)
  - Each district folder contains: .shp, .shx, .dbf, .prj files

