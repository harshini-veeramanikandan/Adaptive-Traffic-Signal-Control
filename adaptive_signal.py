import os
import sys
import traci

# ------------------------------
# CONNECT SUMO TO PYTHON
# ------------------------------

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# ------------------------------
# START SUMO SIMULATION
# ------------------------------

sumo_cmd = ["sumo-gui", "-c", "simu.sumocfg"]
traci.start(sumo_cmd)

# ------------------------------
# GET TRAFFIC LIGHT ID
# ------------------------------

tls_id = traci.trafficlight.getIDList()[0]

print("Traffic Light ID:", tls_id)

# ------------------------------
# MAIN CONTROL LOOP
# ------------------------------

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    current_time = traci.simulation.getTime()

    # Every 10 seconds check density
    if current_time % 10 == 0:

        lanes = traci.trafficlight.getControlledLanes(tls_id)

        lane_vehicle_count = {}

        # Count vehicles on each lane
        for lane in lanes:
            count = traci.lane.getLastStepVehicleNumber(lane)
            lane_vehicle_count[lane] = count

        # Find lane with highest density
        max_lane = max(lane_vehicle_count, key=lane_vehicle_count.get)

        print("Time:", current_time)
        print("Vehicle count:", lane_vehicle_count)
        print("Giving GREEN to:", max_lane)
        print("--------------------------------")

        # Create signal state
        # G for max lane, r for others
        state = ""

        for lane in lanes:
            if lane == max_lane:
                state += "G"
            else:
                state += "r"

        traci.trafficlight.setRedYellowGreenState(tls_id, state)

# ------------------------------
# CLOSE SIMULATION
# ------------------------------

traci.close()