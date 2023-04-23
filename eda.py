import collect_transform

# check for missing values - in a full project these should be filled based on other columns and/or the image
used_bikes = collect_transform.read_bike_data()
used_bikes = collect_transform.reduce_col_to_first_number(used_bikes, 'Frame Size')
used_bikes = collect_transform.reduce_col_to_first_number(used_bikes, 'Wheel Size')
print(used_bikes.isna().sum() / used_bikes.shape[0])

# running out of time here and I havent done anything with the image.
# I'm going to spend 20 min to see if I can do a 3D bar chart with color, brightness, and price

