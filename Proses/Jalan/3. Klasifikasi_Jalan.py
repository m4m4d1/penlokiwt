import geopandas as gpd

# Load the shapefile
shapefile_path = '../result/Jalan/jalan_desa_roi.shp'
gdf = gpd.read_file(shapefile_path)

# Display the first few rows and columns of the GeoDataFrame
print("Initial GeoDataFrame:")
print(gdf.head())
print("Initial columns:", gdf.columns)

# Check if 'REMARK_1' column exists
if 'REMARK_1' in gdf.columns:
    # Add new column "LABEL_JALAN" based on conditions
    def LABEL_JALAN_value(remark):
        if remark == "Jalan Arteri":
            return "Jalan Arteri"
        elif remark == "Jalan Kolektor":
            return "Jalan Kolektor"
        else:
            return "Jalan Lainnya"

    def LABEL_KELAS_value(remark):
        if remark == "Jalan Arteri":
            return 1
        elif remark == "Jalan Kolektor":
            return 2
        else:
            return 3
        
    gdf['LABEL_JALAN'] = gdf['REMARK_1'].apply(LABEL_JALAN_value)
    gdf['LABEL_KELAS'] = gdf['REMARK_1'].apply(LABEL_KELAS_value)
    
    # Reorder columns: bring "REMARK_1" to the first position and "LABEL_JALAN" to the second
    cols = ['REMARK_1', 'LABEL_JALAN', 'LABEL_KELAS'] + [col for col in gdf.columns if col not in ['REMARK_1', 'LABEL_JALAN', 'LABEL_KELAS']]
    gdf = gdf[cols]
else:
    print("'REMARK_1' column not found in the GeoDataFrame.")
    # If the column doesn't exist, add 'LABEL_JALAN' with default value and make it the first column
    gdf['LABEL_JALAN'] = "Jalan Lainnya"
    gdf['LABEL_KELAS'] = 3
    cols = ['REMARK_1', 'LABEL_JALAN', 'LABEL_KELAS'] + [col for col in gdf.columns if col not in ['REMARK_1', 'LABEL_JALAN', 'LABEL_KELAS']]
    gdf = gdf[cols]

# Remove columns with only 0 values and columns with any NaN values
columns_to_remove = [col for col in gdf.columns if (gdf[col].nunique() == 1 and gdf[col].iloc[0] == 0) or gdf[col].isna().any()]
gdf.drop(columns=columns_to_remove, inplace=True)

# Display the modified GeoDataFrame
print("Modified GeoDataFrame:")
print(gdf.head())
print("Modified columns:", gdf.columns)

# Save the modified GeoDataFrame to a new shapefile
modified_shapefile_path = '../result/Jalan/jalan_desa_roi_modified.shp'
gdf.to_file(modified_shapefile_path)

print(f"Modified shapefile saved to {modified_shapefile_path}")
