import geopandas as gpd
import matplotlib.pyplot as plt

# Load cadastral data (assuming the file is in Shapefile format)
cadastral_file = 'path_to_cadastral_data.shp'
gdf = gpd.read_file(cadastral_file)

# Load land-use classification data (for example, another shapefile with 'green spaces' tagged)
land_use_file = 'path_to_land_use_data.shp'
land_use_gdf = gpd.read_file(land_use_file)

# Make sure the coordinate reference system (CRS) matches between datasets
if gdf.crs != land_use_gdf.crs:
    land_use_gdf = land_use_gdf.to_crs(gdf.crs)

# Identify green space areas in land-use data
# Assuming there is a column 'land_use_type' that classifies the land type
green_spaces = land_use_gdf[land_use_gdf['land_use_type'].isin(['green_space', 'park', 'forest'])]

# Spatial join to identify which green spaces overlap with cadastral parcels
joined = gpd.sjoin(gdf, green_spaces, how='left', op='intersects')

# Calculate the area of green space within each property parcel
# Create a new column 'green_space_area' that calculates the intersection area
joined['green_space_area'] = joined.geometry.intersection(green_spaces.unary_union).area

# Calculate the total area of each cadastral parcel
joined['parcel_area'] = joined.geometry.area

# Calculate the proportion of green space for each parcel
joined['green_space_ratio'] = joined['green_space_area'] / joined['parcel_area']

# Plot the results
fig, ax = plt.subplots(figsize=(10, 10))
joined.plot(column='green_space_ratio', ax=ax, legend=True,
            legend_kwds={'label': "Proportion of Green Space within Parcels",
                         'orientation': "horizontal"})
plt.title("Proportion of Green Space in French Property Parcels")
plt.show()

# You can also export the results to a new shapefile for further analysis
joined.to_file('green_space_proportion_analysis.shp')
