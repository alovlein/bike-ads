import collect_transform
import image_analysis
from PIL import Image

# check for missing values - in a full project these should be filled based on other columns and/or the image
used_bikes = collect_transform.read_bike_data()
used_bikes = collect_transform.reduce_col_to_first_number(used_bikes, 'Frame Size')
used_bikes = collect_transform.reduce_col_to_first_number(used_bikes, 'Wheel Size')
# print(used_bikes.isna().sum() / used_bikes.shape[0])

# running out of time here and I havent done anything with the image.
# I'm going to spend 20 min to see if I can do a 3D bar chart with color, brightness, and price

im = Image.open('bike-ad-data/images/12.jpg')
reducer = image_analysis.Reducer(im)
colors = reducer.identify_dominant_colors(6)
brightness = reducer.identify_brightness()
print(colors)
print(brightness)

# we would just iterate over the files in /bike-ad-data/images with pathlib.

