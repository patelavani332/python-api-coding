#!/usr/bin/env python
# coding: utf-8

# # VacationPy
# ---
# 
# ## Starter Code to Import Libraries and Load the Weather and Coordinates Data

# In[14]:


# Dependencies and Setup
import hvplot.pandas
import pandas as pd
import requests
import json

# Import API key
from api_keys import geoapify_key


# In[15]:


# Load the CSV file created in Part 1 into a Pandas DataFrame
city_data_df = pd.read_csv("output_data/cities.csv")

# Display sample data
city_data_df.head()


# ---
# 
# ### Step 1: Create a map that displays a point for every city in the `city_data_df` DataFrame. The size of the point should be the humidity in each city.

# In[16]:


get_ipython().run_cell_magic('capture', '--no-display', '\n# Configure the map plot\nmap_data = city_data_df.hvplot.points("Lng", "Lat", geo = True, size = "Humidity", scale = 1, color = "City", alpha = 0.5, tiles = "OSM", frame_width = 700, frame_height = 500)\n\n# Display the map\nmap_data\n')


# ### Step 2: Narrow down the `city_data_df` DataFrame to find your ideal weather condition

# In[17]:


# Narrow down cities that fit criteria and drop any results with null values
narrow_city_df = city_data_df[(city_data_df["Max Temp"] > 21) & (city_data_df["Max Temp"] < 27) & (city_data_df["Wind Speed"] < 4.5) & (city_data_df["Cloudiness"] == 0)]
# Drop any rows with null values
narrow_city_df = narrow_city_df.dropna()

# Display sample data
narrow_city_df


# ### Step 3: Create a new DataFrame called `hotel_df`.

# In[18]:


# Use the Pandas copy function to create DataFrame called hotel_df to store the city, country, coordinates, and humidity

hotel_df = narrow_city_df[["City", "Country", "Lat", "Lng", "Humidity"]].copy()
# Add an empty column, "Hotel Name," to the DataFrame so you can store the hotel found using the Geoapify API
hotel_df["Hotel Name"] = ""

# Display sample data
hotel_df


# ### Step 4: For each city, use the Geoapify API to find the first hotel located within 10,000 metres of your coordinates.

# In[37]:


# Print a message to follow up the hotel search
print("Starting hotel search")

# Iterate through the hotel_df DataFrame
for index, row in hotel_df.iterrows():
    
    # get latitude, longitude from the DataFrame
    latitude = row["Lat"]
    longitude = row["Lng"]
    categories=  "accommodation.hotel"
    radius = 10000
     # Add filter and bias parameters with the current city's latitude and longitude to the params dictionary
    filters = f"circle:{longitude},{latitude},{radius}"
    bias = f"proximity:{longitude},{latitude}"
    limit = 20
    params = {
        "categories":categories,
        "limit":limit,
        "filter":filters,
        "bias":bias,
        "apiKey":geoapify_key    
    }
     # Set base URL
    base_url = "https://api.geoapify.com/v2/places"
    # Make and API request using the params dictionaty
    response = requests.get(base_url, params=params)
#    print(response.url)
    # Convert the API response to JSON format
    name_address = response.json()

    # Print the json (pretty printed)
    #    print(json.dumps(places_data, indent=4, sort_keys=True))
     # Grab the first hotel from the results and store the name in the hotel_df DataFrame
    try:
        hotel_df.loc[index, "Hotel Name"] = name_address["features"][0]["properties"]["name"]
    except (KeyError, IndexError):
        # If no hotel is found, set the hotel name as "No hotel found".
        hotel_df.loc[index, "Hotel Name"] = "No hotel found"
        
    # Log the search results
    print(f"{hotel_df.loc[index, 'City']} - nearest hotel: {hotel_df.loc[index, 'Hotel Name']}")

# Display sample data
hotel_df


# ### Step 5: Add the hotel name and the country as additional information in the hover message for each city in the map.

# In[38]:


get_ipython().run_cell_magic('capture', '--no-display', '\n# Configure the map plot\nmap_data = hotel_df.hvplot.points("Lng", "Lat", geo = True, size = "Humidity", scale = 1, color = "City", alpha = 0.5, tiles = "OSM", frame_width = 700, frame_height = 500, hover_cols = ["Hotel Name", "Country"])\n\n\n# Display the map\nmap_data\n')


# In[ ]:




