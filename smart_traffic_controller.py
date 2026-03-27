import os
import sys
import traci
import pandas as pd

# -----------------------------
# CHECK SUMO
# -----------------------------
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# -----------------------------
# START SUMO
# -----------------------------
sumo_cmd = ["sumo-gui", "-c", "simu.sumocfg"]
traci.start(sumo_cmd)

tls_id = traci.trafficlight.getIDList()[0]

# -----------------------------
# LANES
# -----------------------------
incoming_lanes = [
    "E0_0","E0_1",
    "-E3_0","-E3_1",
    "-E2_0","-E2_1",
    "-E4_0","-E4_1"
]

# -----------------------------
# DATA STORAGE
# -----------------------------
traffic_data = []

green_duration = 20
last_switch = 0

# -----------------------------
# SIMULATION LOOP
# -----------------------------
while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    time = traci.simulation.getTime()

    lane_counts = {}

    for lane in incoming_lanes:
        lane_counts[lane] = traci.lane.getLastStepVehicleNumber(lane)

    road_counts = {
        "WEST": lane_counts["E0_0"] + lane_counts["E0_1"],
        "EAST": lane_counts["-E3_0"] + lane_counts["-E3_1"],
        "NORTH": lane_counts["-E2_0"] + lane_counts["-E2_1"],
        "SOUTH": lane_counts["-E4_0"] + lane_counts["-E4_1"]
    }

    EW = road_counts["WEST"] + road_counts["EAST"]
    NS = road_counts["NORTH"] + road_counts["SOUTH"]

    # -----------------------------
    # SAVE DATA EVERY 5 SECONDS
    # -----------------------------
    if time % 5 == 0:

        traffic_data.append({
            "time": time,
            "west": road_counts["WEST"],
            "east": road_counts["EAST"],
            "north": road_counts["NORTH"],
            "south": road_counts["SOUTH"],
            "EW_density": EW,
            "NS_density": NS
        })

    # -----------------------------
    # SIGNAL CONTROL
    # -----------------------------
    if time - last_switch > green_duration:

        if EW > NS:
            traci.trafficlight.setPhase(tls_id,0)
        else:
            traci.trafficlight.setPhase(tls_id,2)

        last_switch = time


# -----------------------------
# SAVE CSV
# -----------------------------
df = pd.DataFrame(traffic_data)

df.to_csv("traffic_data_with_time.csv", index=False)

print("Dataset saved as traffic_data_with_time.csv")

traci.close()