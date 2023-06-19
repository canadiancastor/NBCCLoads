import json

with open('SkyCiv.json', 'r') as f:
  data = json.load(f)

#Locality, province (2 char), Country (Canada)
site = data[1]["arguments"]["site_data"]["project_address"]

#Degrees of slope
slope = data[1]["arguments"]["building_data"]["building_dimensions"]["roof_angle"]

#Slip = "unobstructed-slippery", No-slip = "other-cases"
slippery = data[1]["arguments"]["building_data"]["snow_parameters"]["sloped_roof_surface_condition"]

print(site, slope, slippery)

data[1]["arguments"]["site_data"]["project_address"] = "Sherbrooke, Qc, Canada"
data[1]["arguments"]["building_data"]["building_dimensions"]["roof_angle"] = 18.43
data[1]["arguments"]["building_data"]["snow_parameters"]["sloped_roof_surface_condition"] = "unobstructed-slippery"

json_object = json.dumps(data)
# Writing to sample.json
with open("SkyCiv_out.json", "w") as outfile:
    outfile.write(json_object)