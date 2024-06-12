import geopandas as gpd

# Load the shapefile
shapefile_path = 'result\Jalan\jalan_desa_roi.shp'
gdf = gpd.read_file(shapefile_path)

# Display the first few rows of the GeoDataFrame
print(gdf.head())
print(gdf.columns)


# If you want to see all the unique values in a specific column (e.g., 'road_type')
if 'road_type' in gdf.columns:
    print(gdf['road_type'].unique())
