import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging


# Set up logging
logging.basicConfig(filename='trail_simulation.log', level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')


# Simulation parameters
days = 365  # Number of days to simulate
daily_tourists_mean = 11000  # Average tourists per day
daily_tourists_std = 200  # Standard deviation for randomness
litter_per_tourist = 0.01  # Litter produced per tourist in kg


# Generate daily tourists with randomness
np.random.seed(42)  # For reproducibility
daily_tourists = np.random.normal(daily_tourists_mean, daily_tourists_std, days)
daily_tourists = np.clip(daily_tourists, 50, None)  # Ensure minimum of 50 tourists




def run_baseline_simulation():
   """Run baseline scenario with quality protection"""
   logging.info("Starting baseline scenario simulation")


   # Baseline parameters
   clean_up_efficiency = 0.7
   clean_up_frequency = 7  # Weekly cleanups
   erosion_rate = 0.0001
   maintenance_frequency = 30  # Monthly maintenance
   maintenance_improvement = 10  # 10% quality boost
   min_quality = 1  # Minimum quality threshold (


   # Initialize arrays
   total_litter = np.zeros(days)
   trail_quality = np.zeros(days)
   trail_quality[0] = 100  # Start at 100% quality


   # Data storage
   data = {
       "Day": [], "Tourists": [], "Litter_Added": [],
       "Litter_Removed": [], "Total_Litter": [],
       "Trail_Degradation": [], "Trail_Maintenance": [],
       "Trail_Quality": []
   }


   for day in range(days):
       tourists_today = daily_tourists[day]


       # Litter calculation
       litter_added = tourists_today * litter_per_tourist
       total_litter[day] = total_litter[day - 1] + litter_added if day > 0 else litter_added


       # Cleanup
       litter_removed = 0
       if day % clean_up_frequency == 0:
           litter_removed = total_litter[day] * clean_up_efficiency
           total_litter[day] -= litter_removed
           logging.info(f"Day {day + 1}: Removed {litter_removed:.2f}kg litter")


       # Quality calculation with protection
       degradation = tourists_today * erosion_rate
       new_quality = (trail_quality[day - 1] if day > 0 else 100) - degradation
       trail_quality[day] = max(new_quality, min_quality)


       # Maintenance
       maintenance = 0
       if day % maintenance_frequency == 0:
           maintenance = maintenance_improvement
           trail_quality[day] = min(trail_quality[day] + maintenance, 100)
           logging.info(f"Day {day + 1}: Maintenance improved quality to {trail_quality[day]:.1f}%")


       # Store data
       data["Day"].append(day + 1)
       data["Tourists"].append(tourists_today)
       data["Litter_Added"].append(litter_added)
       data["Litter_Removed"].append(litter_removed)
       data["Total_Litter"].append(total_litter[day])
       data["Trail_Degradation"].append(degradation)
       data["Trail_Maintenance"].append(maintenance)
       data["Trail_Quality"].append(trail_quality[day])


   df = pd.DataFrame(data)
   df.to_csv("baseline_results.csv", index=False)
   logging.info(
       f"Baseline simulation complete. Quality range: {df['Trail_Quality'].min():.1f}% to {df['Trail_Quality'].max():.1f}%")
   return df["Total_Litter"].mean(), df["Trail_Quality"].mean(), df




def run_alternative_simulation():
   """Run alternative scenario with enhanced parameters"""
   logging.info("Starting alternative scenario simulation")


   # Enhanced parameters
   clean_up_efficiency = 0.9  # 90% efficiency
   clean_up_frequency = 3  # Every 3 days
   erosion_rate = 0.0001
   maintenance_frequency = 21  # Every 21 days
   maintenance_improvement = 15  # 15% boosts
   min_quality = 1  # Minimum quality threshold


   # Initialize arrays
   total_litter = np.zeros(days)
   trail_quality = np.zeros(days)
   trail_quality[0] = 100


   # Data storage
   data = {
       "Day": [], "Tourists": [], "Litter_Added": [],
       "Litter_Removed": [], "Total_Litter": [],
       "Trail_Degradation": [], "Trail_Maintenance": [],
       "Trail_Quality": []
   }


   for day in range(days):
       tourists_today = daily_tourists[day]


       # Litter calculation
       litter_added = tourists_today * litter_per_tourist
       total_litter[day] = total_litter[day - 1] + litter_added if day > 0 else litter_added


       # Cleanup
       litter_removed = 0
       if day % clean_up_frequency == 0:
           litter_removed = total_litter[day] * clean_up_efficiency
           total_litter[day] -= litter_removed
           logging.info(f"Day {day + 1}: Removed {litter_removed:.2f}kg litter (alternative)")


       # Quality calculation with protection
       degradation = tourists_today * erosion_rate
       new_quality = (trail_quality[day - 1] if day > 0 else 100) - degradation
       trail_quality[day] = max(new_quality, min_quality)


       # Maintenance
       maintenance = 0
       if day % maintenance_frequency == 0:
           maintenance = maintenance_improvement
           trail_quality[day] = min(trail_quality[day] + maintenance, 100)
           logging.info(f"Day {day + 1}: Maintenance improved quality to {trail_quality[day]:.1f}% (alternative)")


       # Store data
       data["Day"].append(day + 1)
       data["Tourists"].append(tourists_today)
       data["Litter_Added"].append(litter_added)
       data["Litter_Removed"].append(litter_removed)
       data["Total_Litter"].append(total_litter[day])
       data["Trail_Degradation"].append(degradation)
       data["Trail_Maintenance"].append(maintenance)
       data["Trail_Quality"].append(trail_quality[day])


   df = pd.DataFrame(data)
   df.to_csv("alternative_results.csv", index=False)
   logging.info(
       f"Alternative simulation complete. Quality range: {df['Trail_Quality'].min():.1f}% to {df['Trail_Quality'].max():.1f}%")
   return df["Total_Litter"].mean(), df["Trail_Quality"].mean(), df




# Run simulations
baseline_litter, baseline_quality, df_baseline = run_baseline_simulation()
alt_litter, alt_quality, df_alt = run_alternative_simulation()


# Create and save comparison
comparison = pd.DataFrame({
   "Scenario": ["Baseline", "Alternative"],
   "Avg_Litter_kg": [baseline_litter, alt_litter],
   "Avg_Quality_pct": [baseline_quality, alt_quality]
})
comparison.to_csv("scenario_comparison.csv", index=False)




# Generate visualizations
def create_comparison_plot():
   plt.figure(figsize=(14, 6))


   # Litter comparison
   plt.subplot(1, 2, 1)
   bars = plt.bar(comparison["Scenario"], comparison["Avg_Litter_kg"],
                  color=['#1f77b4', '#2ca02c'], alpha=0.7)
   plt.title("Average Litter Accumulation")
   plt.ylabel("Kilograms of Litter")
   plt.ylim(0, max(comparison["Avg_Litter_kg"]) * 1.2)
   for bar in bars:
       height = bar.get_height()
       plt.text(bar.get_x() + bar.get_width() / 2., height,
                f'{height:.1f} kg', ha='center', va='bottom')


   # Quality comparison
   plt.subplot(1, 2, 2)
   bars = plt.bar(comparison["Scenario"], comparison["Avg_Quality_pct"],
                  color=['#1f77b4', '#2ca02c'], alpha=0.7)
   plt.title("Average Trail Quality")
   plt.ylabel("Quality Score (%)")
   plt.ylim(0, 100)
   for bar in bars:
       height = bar.get_height()
       plt.text(bar.get_x() + bar.get_width() / 2., height,
                f'{height:.1f}%', ha='center', va='bottom')


   plt.tight_layout()
   plt.savefig("scenario_comparison.png")
   plt.show()




create_comparison_plot()


print("Simulation completed successfully. Results saved to:")
print("- baseline_results.csv")
print("- alternative_results.csv")
print("- scenario_comparison.csv")
print("- scenario_comparison.png")

