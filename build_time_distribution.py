import pandas as pd
import matplotlib.pyplot as plt

# Read data from the CSV file
file_path = 'changes_revision_rbe_time.csv'
df = pd.read_csv(file_path)

# Filter out rows with missing or failed values
df = df.dropna(subset=['rbe_gcp_state', 'rbe_bb_state'])
df = df[(df['rbe_gcp_state'] == 'SUCCESSFUL') & (df['rbe_bb_state'] == 'SUCCESSFUL')]

# Extract build times for both RBE GCP and RBE BB
rbe_gcp_times = df['rbe_gcp_time_seconds'].tolist()
rbe_bb_times = df['rbe_bb_time_seconds'].tolist()

# Create a histogram for RBE GCP build times
plt.hist(rbe_gcp_times, bins=20, alpha=0.5, label='RBE GCP')

# Create a histogram for RBE BB build times
plt.hist(rbe_bb_times, bins=20, alpha=0.5, label='RBE BB')

# Add labels and title
plt.xlabel('Build Time (seconds)')
plt.ylabel('Frequency')
plt.title('Build Time Distribution for RBE GCP and RBE BB')
plt.legend()

# Show the plot
plt.show()
