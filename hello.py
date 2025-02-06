import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the schedule data
schedule = {
    "Sunday": [(6, 23)],
    "Monday": [(10, 11), (16, 17)],
    "Tuesday": [(9.5, 11)],
    "Wednesday": [(10, 11), (16, 17)],
    "Thursday": [(9.5, 11)],
    "Friday": [(10, 11), (16, 17)],
    "Saturday": [(6, 23)]
}

# Create a time range for 24 hours with 1-hour increments
time_slots = np.arange(6, 24, 1)

# Create a DataFrame to mark availability
availability = pd.DataFrame(0, index=time_slots, columns=schedule.keys())

# Mark the availability based on the given schedule
for day, periods in schedule.items():
    for start, end in periods:
        availability.loc[start:end, day] = 1

# Create a plot
plt.figure(figsize=(10, 8))

# Plot the availability
for day in schedule.keys():
    plt.fill_between(availability.index, availability[day], where=availability[day] == 1, step='mid', alpha=0.5, label=day)

# Formatting the plot
plt.yticks(np.arange(6, 24, 1), labels=[f"{hour}:00" for hour in np.arange(6, 24, 1)])
plt.xlabel("Day of the Week")
plt.ylabel("Time of Day")
plt.title("Availability Schedule")
plt.legend(loc="upper right")

# Save the plot to an Excel file
file_path = "/mnt/data/Availability_Schedule.xlsx"
availability.to_excel(file_path)

file_path