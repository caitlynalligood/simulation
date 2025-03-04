import numpy as np
import pandas as pd
import logging

# Set up logging
logging.basicConfig(filename='simulation.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Simulation parameters
days = 365  # Simulate for 1 year
daily_tourists_mean = 11000  # Average number of tourists per day
daily_tourists_std = 1000  # Standard deviation for randomness
litter_per_tourist = 0.2  # Average litter per tourist in kg
clean_up_frequency = 1  # Clean-up every day
clean_up_efficiency = 0.9  # 90% of litter is removed during clean-up
erosion_rate = 0.0001  # Trail erosion rate
trail_maintenance_frequency = 7  # Maintenance every 7 days
trail_maintenance_improvement = 10  # Trail quality improvement

# Validate input parameters
if daily_tourists_mean <= 0 or litter_per_tourist < 0 or clean_up_efficiency < 0 or clean_up_efficiency > 1:
    raise ValueError("Invalid input parameters.")

# Generate daily tourists
np.random.seed(42)  # For reproducibility
daily_tourists = np.random.normal(daily_tourists_mean, daily_tourists_std, days)
daily_tourists = np.clip(daily_tourists, 0, None)  # Ensure no negative tourists

# Initialize variables
total_litter = np.zeros(days)
trail_quality = np.zeros(days)
trail_quality[0] = 100  # Initial trail quality

# Data collection
data = {
    "Day": [],
    "Tourists": [],
    "Total_Litter": [],
    "Trail_Quality": []
}

# Simulate daily changes
for day in range(days):
    logging.info(f"Day {day + 1}: Simulation started.")

    # Calculate daily litter
    litter_added = daily_tourists[day] * litter_per_tourist
    total_litter[day] = total_litter[day - 1] + litter_added if day > 0 else litter_added

    # Perform clean-up
    if day % clean_up_frequency == 0:
        litter_removed = total_litter[day] * clean_up_efficiency
        total_litter[day] -= litter_removed
        logging.info(f"Day {day + 1}: Clean-up performed. Litter removed: {litter_removed:.2f} kg.")

    # Calculate trail erosion
    degradation = daily_tourists[day] * erosion_rate
    trail_quality[day] = trail_quality[day - 1] - degradation if day > 0 else 100 - degradation

    # Perform maintenance
    if day % trail_maintenance_frequency == 0:
        trail_quality[day] += trail_maintenance_improvement
        trail_quality[day] = min(trail_quality[day], 100)  # Cap at 100%
        logging.info(f"Day {day + 1}: Maintenance performed. Trail quality improved by {trail_maintenance_improvement}%.")

    logging.info(f"Day {day + 1}: Simulation ended. Total litter: {total_litter[day]:.2f} kg, Trail quality: {trail_quality[day]:.2f}%.")

    # Collect data
    data["Day"].append(day + 1)
    data["Tourists"].append(daily_tourists[day])
    data["Total_Litter"].append(total_litter[day])
    data["Trail_Quality"].append(trail_quality[day])

# Convert data to DataFrame and save
df = pd.DataFrame(data)
df.to_csv("simulation_data.csv", index=False)
logging.info("Simulation data saved to simulation_data.csv.")

print("Simulation completed. Data saved to simulation_data.csv.")