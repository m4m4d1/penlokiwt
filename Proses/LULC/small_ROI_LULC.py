import ee
import geemap
import geopandas as gpd

# Authenticate and initialize the Earth Engine library.
ee.Authenticate()
ee.Initialize(project='ee-mimaduddinar')

# Load the shapefile
shp_file = '..\..\Dataset\ROI_Kecil\ROI_Kecil.shp'
gdf = gpd.read_file(shp_file)

# Convert GeoDataFrame to GeoJSON format
geojson = gdf.__geo_interface__

# Use the first geometry as the region of interest
first_geometry = geojson['features'][0]['geometry']
roi = ee.Geometry.Polygon(first_geometry['coordinates'])

# Define the cloud and shadow mask function using the "pixel_qa" band.
def maskL8sr(image):
    # Get the pixel QA band.
    qa = image.select('pixel_qa')
    # Create a mask for cloud shadow and clouds.
    cloudShadowBitMask = 1 << 3
    cloudsBitMask = 1 << 5
    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(
        qa.bitwiseAnd(cloudsBitMask).eq(0))
    # Apply mask, divide by 10000, select bands, and copy properties.
    return image.updateMask(mask).divide(10000).select(["B[0-9]*"]).copyProperties(image, ["system:time_start"])

vis_params = {
    'min': 0,
    'max': 0.4,
    'bands': ['B6', 'B5', 'B4']  # For false color composite
}

# Load the Landsat 8 image collection for the year 2021 and the specified region.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
    .filterDate('2021-01-01', '2021-12-31') \
    .filterBounds(roi)

# Apply the cloud and shadow mask function and calculate the median.
cloud_free_median = collection.map(maskL8sr).median().clip(roi)

# Print image information.
info = cloud_free_median.getInfo()
print(info)

# Visualize the result using geemap.
Map = geemap.Map(center=[-7.6, 108.7], zoom=11)  # Adjusted center and zoom for the smaller ROI.

# Add the image to the map.
Map.addLayer(cloud_free_median, vis_params, "Landsat 8")


ESA = ee.Image('ESA/WorldCover/v100/2020').clip(roi)
Map.addLayer(ESA, {}, 'ESA')

classValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
remapValues = ee.List.sequence(0, 10)
label = 'lc'
lc = ESA.remap(classValues, remapValues).rename(label).toByte()

sample = cloud_free_median.addBands(lc).stratifiedSample(
    **{
        'numPoints': 100,
        'classBand': label,
        'region': roi,
        'scale': 10,
        'geometries': True
    })


sample = sample.randomColumn()
trainingSample = sample.filter('random <= 0.8')
validationSample = sample.filter('random > 0.8')

trainedClassifier = ee.Classifier.smileRandomForest(numberOfTrees=10).train(
    **{
        'features': trainingSample,
        'classProperty': label,
        'inputProperties': cloud_free_median.bandNames()
    })

ESAWorldCover_classified = cloud_free_median.classify(trainedClassifier)


trainAccuracy = trainedClassifier.confusionMatrix()
trainAccuracy.accuracy()

ESAWorldCover_classified = collection.map(lambda img: img.classify(trainedClassifier))

classVis = {
  'min': 0,
  'max': 10,
  'palette': ['006400' ,'ffbb22', 'ffff4c', 'f096ff', 'fa0000', 'b4b4b4',
            'f0f0f0', '0064c8', '0096a0', '00cf75', 'fae6a0']
}

#Map.addLayer(lc, classVis, 'lc');
Map.addLayer(ESAWorldCover_classified, classVis, 'Classified')
# Convert training sample and validation sample to feature collections
training_fc = trainingSample.map(lambda feature: ee.Feature(feature))
validation_fc = validationSample.map(lambda feature: ee.Feature(feature))

# Define visualization parameters for the samples
sample_vis_params = {
    'color': 'FF0000'  # Red color for training sample
}

# Add training sample and validation sample layers to the map
Map.addLayer(training_fc, sample_vis_params, 'Training Sample')
Map.addLayer(validation_fc, {}, 'Validation Sample')


# Save the map as an HTML file.
Map.to_html("../../result/LULC/smallROI.html")
print('Map saved to smallROI.html')
