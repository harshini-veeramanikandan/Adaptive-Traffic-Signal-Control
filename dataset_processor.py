import pandas as pd

def load_dataset(path="traffic_dataset.csv"):

    data = pd.read_csv(path)

    # total vehicles
    data["TotalVehicles"] = (
        data["CarCount"]
        + data["BikeCount"]
        + data["BusCount"]
        + data["TruckCount"]
    )

    return data


def detect_rush_hours(data):

    # average traffic per hour
    hourly = data.groupby("Time")["TotalVehicles"].mean()

    threshold = hourly.mean()

    rush_hours = hourly[hourly > threshold]

    print("\nDetected Rush Hours:")
    print(rush_hours)

    return rush_hours