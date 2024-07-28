import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import geopandas as gpd
from rasterio.mask import mask
from shapely.geometry import box
import glob
import dask.array as da
from sklearn.linear_model import LinearRegression

# Function to load and display night light data
def load_night_light_data(file_path):
    # Open the GeoTIFF file
    with rasterio.open(file_path) as src:
        # Read the first band
        night_lights = src.read(1)
        # Mask the no-data values
        night_lights = np.ma.masked_equal(night_lights, src.nodata)
    
    return night_lights, src

# Plot night light intensity
def plot_night_light_intensity(night_lights, src, region_name='Global'):
    # Set up the plot
    plt.figure(figsize=(10, 6))
    plt.title(f"Night Light Intensity - {region_name}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    
    # Display the night light data
    show(night_lights, transform=src.transform, cmap='viridis', vmin=0, vmax=60)
    plt.colorbar(label='Light Intensity')
    plt.show()

# Calculate economic activity proxy from night lights
def calculate_economic_activity(night_lights):
    # Calculate the total light intensity
    total_intensity = np.sum(night_lights)
    
    # Calculate the average light intensity
    avg_intensity = np.mean(night_lights)
    
    return total_intensity, avg_intensity

# Load country borders (for plotting)
def load_country_borders():
    # Read the world shapefile
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    return world

# Correlate night light data with GDP
def correlate_with_gdp(night_lights, src, gdp_data, country_name):
    # Mask the night lights data to focus on a specific country
    country_geom = gdp_data.loc[gdp_data['name'] == country_name, 'geometry'].values[0]
    geo_box = [box(*country_geom.bounds)]
    out_image, out_transform = mask(src, geo_box, crop=True)

    # Flatten the arrays for correlation
    flattened_lights = out_image.flatten()
    flattened_gdp = np.full(flattened_lights.shape, gdp_data.loc[gdp_data['name'] == country_name, 'gdp_md_est'].values[0])

    # Filter out the masked areas
    mask_array = flattened_lights.mask
    filtered_lights = flattened_lights[~mask_array]
    filtered_gdp = flattened_gdp[~mask_array]

    # Calculate the correlation
    correlation = np.corrcoef(filtered_lights, filtered_gdp)[0, 1]
    
    print(f"Correlation between night light intensity and GDP for {country_name}: {correlation:.2f}")

# Perform a time series analysis
def time_series_analysis(file_pattern, region_name='Global'):
    # Find all files matching the pattern
    files = sorted(glob.glob(file_pattern))
    
    # Load each file and calculate the average light intensity over time
    time_series = []
    for file in files:
        night_lights, _ = load_night_light_data(file)
        avg_intensity = np.mean(night_lights)
        time_series.append(avg_intensity)
    
    # Plot the time series
    plt.figure(figsize=(12, 6))
    plt.plot(time_series, marker='o', linestyle='-')
    plt.title(f"Time Series of Average Night Light Intensity - {region_name}")
    plt.xlabel("Time (Months)")
    plt.ylabel("Average Light Intensity")
    plt.xticks(ticks=range(len(files)), labels=[f"Month {i+1}" for i in range(len(files))], rotation=45)
    plt.grid(True)
    plt.show()

# Analyze large data with Dask
def analyze_large_data(file_path):
    # Load the data using Dask
    with rasterio.open(file_path) as src:
        night_lights_dask = da.from_array(src.read(1), chunks=(2048, 2048))
    
    # Perform calculations
    total_intensity = night_lights_dask.sum().compute()
    avg_intensity = night_lights_dask.mean().compute()
    
    print(f"Total Light Intensity (Dask): {total_intensity}")
    print(f"Average Light Intensity (Dask): {avg_intensity}")

# Main function
def main():
    # Path to the night light data
    night_light_file = 'VIIRS_2023_global.tif'
    
    # Load the night light data
    night_lights, src = load_night_light_data(night_light_file)
    
    # Plot night light intensity
    plot_night_light_intensity(night_lights, src)
    
    # Calculate economic activity proxy
    total_intensity, avg_intensity = calculate_economic_activity(night_lights)
    print(f"Total Light Intensity: {total_intensity}")
    print(f"Average Light Intensity: {avg_intensity}")
    
    # Load country borders
    world = load_country_borders()
    
    # Plot the world with night lights overlay
    fig, ax = plt.subplots(figsize=(12, 8))
    world.boundary.plot(ax=ax, linewidth=1, edgecolor='black')
    show(night_lights, transform=src.transform, cmap='hot', ax=ax, alpha=0.5)
    plt.title('Night Lights Overlaid on Country Borders')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
    
    # Correlate night lights with GDP for a specific country (e.g., United States)
    world['gdp_md_est'] = world['gdp_md_est'].fillna(0)  # Fill missing GDP values with 0
    correlate_with_gdp(night_lights, src, world, country_name='United States')
    
    # Time series analysis using monthly data (pattern assumes filenames like VIIRS_2023_01.tif, VIIRS_2023_02.tif, ...)
    file_pattern = 'VIIRS_2023_*.tif'
    time_series_analysis(file_pattern)
    
    # Analyze large data with Dask
    analyze_large_data(night_light_file)

# Run the main function
if __name__ == '__main__':
    main()
