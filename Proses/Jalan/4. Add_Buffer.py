# import geopandas as gpd
# from shapely.geometry import MultiPolygon

# # Load the shapefile
# shapefile_path = '..\\result\\Jalan\\jalan_desa_roi_modified.shp'
# gdf = gpd.read_file(shapefile_path)

# # Reproject to UTM zone 48S
# utm_epsg = 32748
# gdf = gdf.to_crs(epsg=utm_epsg)

# # Define the buffer distances for each classification
# buffer_distances = {
#     0: 200,
#     1: 400,
#     2: 600,
#     3: 800,
#     4: 1000
# }

# # Create an empty GeoDataFrame to store the multibuffer polygons and buffer information
# multibuffer_gdf = gpd.GeoDataFrame(columns=['level', 'geometry', 'shape', 'distance'], crs=gdf.crs)

# # Iterate over each road geometry
# for idx, row in gdf.iterrows():
#     # Create buffers for each distance
#     buffer_geoms = [row['geometry'].buffer(distance) for distance in buffer_distances.values()]
    
#     # Create polygons for each buffer and append them to the GeoDataFrame
#     for level, buffer_geom in zip(buffer_distances.keys(), buffer_geoms):
#         multibuffer_gdf = multibuffer_gdf.append({'level': level, 'geometry': buffer_geom, 'shape': 'polygon', 'distance': buffer_distances[level]}, ignore_index=True)

# # Save the new shapefile with the multibuffer polygons
# output_shapefile_path = '..\\result\\Jalan\\jalan_desa_roi_multibuffer.shp'
# multibuffer_gdf.to_file(output_shapefile_path)

# print(f"Multibuffer shapefile saved to {output_shapefile_path}")

import geopandas as gpd
from shapely.geometry import MultiPolygon

# Load the shapefile
shapefile_path = '..\\result\\Jalan\\jalan_desa_roi_modified.shp'
gdf = gpd.read_file(shapefile_path)

# Reproject to UTM zone 48S
utm_epsg = 32748
gdf = gdf.to_crs(epsg=utm_epsg)

# Define the buffer distances and corresponding scores
buffer_distances = [200, 400, 600, 800, 1000]
buffer_scores = {200: 1, 400: 1, 600: 2, 800: 2, 1000: 3}

# Create an empty GeoDataFrame to store the multibuffer polygons and buffer information
multibuffer_gdf = gpd.GeoDataFrame(columns=['level', 'geometry', 'shape', 'distance', 'Skor'], crs=gdf.crs)

# Iterate over each road geometry
for idx, row in gdf.iterrows():
    # Create buffers for each distance
    for level, distance in enumerate(buffer_distances):
        buffer_geom = row['geometry'].buffer(distance)
        skor = buffer_scores[distance]
        
        # Append polygon buffer information to the GeoDataFrame
        multibuffer_gdf = multibuffer_gdf.append({
            'level': level, 
            'geometry': buffer_geom, 
            'shape': 'polygon', 
            'distance': distance, 
            'Skor': skor
        }, ignore_index=True)

# Save the new shapefile with the multibuffer polygons
output_shapefile_path = '..\\result\\Jalan\\jalan_desa_roi_multibuffer_2.shp'
multibuffer_gdf.to_file(output_shapefile_path)

print(f"Multibuffer shapefile saved to {output_shapefile_path}")
