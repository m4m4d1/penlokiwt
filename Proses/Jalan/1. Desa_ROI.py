import geopandas as gpd

# Load the road and region shapefiles
village = gpd.read_file('..\Dataset\Pangandaran\ADMINISTRASIDESA_AR_25K.shp')
region = gpd.read_file('..\ROI\ROI_Kecil-polygon.shp')

# Ensure both shapefiles use the same coordinate reference system (CRS)
villages = village.to_crs(region.crs)

# Perform the intersection
village_in_pangandaran = gpd.overlay(villages, region, how='intersection')

# Save the resulting shapefile
village_in_pangandaran.to_file('../result/Jalan/desa_di_roi.shp')
