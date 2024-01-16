import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
csv_file_path = 'changes_revision_rbe_time.csv'
df = pd.read_csv(csv_file_path)

# Filter rows where both rbe_gcp_state and rbe_bb_state are successful
successful_rows = df[(df['rbe_gcp_state'] == 'SUCCESSFUL') & (df['rbe_bb_state'] == 'SUCCESSFUL')]

# Create Build Time Distribution plot
plt.figure(figsize=(10, 6))

# Plot GCP build times for successful rows
plt.scatter(successful_rows['rbe_gcp_time_minutes'], range(len(successful_rows)), label='GCP', alpha=0.7)

# Plot BB build times for successful rows
plt.scatter(successful_rows['rbe_bb_time_minutes'], range(len(successful_rows)), label='BB', alpha=0.7)

# Set labels and title
plt.xlabel('Build Time (minutes)')
plt.ylabel('Build')
plt.title('Build Time Distribution for Successful Builds')
plt.legend()
plt.grid(True)

# Set x-axis limits to zoom in on the data up to 200 minutes
plt.xlim(0, 175)

# Show the plot
plt.show()