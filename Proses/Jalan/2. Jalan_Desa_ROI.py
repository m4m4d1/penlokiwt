import geopandas as gpd

# Load the road and region shapefiles
road = gpd.read_file('..\\Dataset\\Jalan\\KAB. PANGANDARAN\\JALAN_LN_25K.shp')
village = gpd.read_file('..\\result\\Jalan\\desa_di_roi.shp')

# Ensure both shapefiles use the same coordinate reference system (CRS)
roads = road.to_crs(village.crs)

# Perform the intersection
roads_in_pangandaran = gpd.overlay(roads, village, how='intersection')

# Save the resulting shapefile
roads_in_pangandaran.to_file('../result/Jalan/jalan_desa_roi.shp')
