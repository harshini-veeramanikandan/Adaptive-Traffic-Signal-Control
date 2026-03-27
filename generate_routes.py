import pandas as pd

data = pd.read_csv("traffic_dataset.csv")

data["TotalVehicles"] = (
    data["CarCount"]
    + data["BikeCount"]
    + data["BusCount"]
    + data["TruckCount"]
)

traffic = data.groupby("Time")["TotalVehicles"].mean()

f = open("generated_routes.rou.xml","w")

f.write("<routes>\n")

for i,(time,value) in enumerate(traffic.items()):

    vehicles = int(value * 10)

    begin = i * 300
    end = (i+1) * 300

    f.write(
        f'<flow id="flow{i}" begin="{begin}" end="{end}" '
        f'vehsPerHour="{vehicles}" from="E0" to="E3"/>\n'
    )

f.write("</routes>")
f.close()

print("Routes generated successfully")