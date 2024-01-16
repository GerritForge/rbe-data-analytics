import pandas as pd
import matplotlib.pyplot as plt

# Read data from the CSV file
file_path = 'changes_revision_rbe_time.csv'
df = pd.read_csv(file_path)

# Filter out rows with missing or failed values
df = df.dropna(subset=['rbe_gcp_state', 'rbe_bb_state'])
df = df[(df['rbe_gcp_state'] == 'SUCCESSFUL') & (df['rbe_bb_state'] == 'SUCCESSFUL')]

# Calculate average build times for RBE GCP and RBE BB across change numbers
avg_gcp_times = df.groupby('change_number')['rbe_gcp_time_seconds'].mean()
avg_bb_times = df.groupby('change_number')['rbe_bb_time_seconds'].mean()

# Create a bar chart for average build times
bar_width = 0.35
index = range(1, len(avg_gcp_times) + 1)

plt.bar(index, avg_gcp_times, width=bar_width, label='RBE GCP')
plt.bar([i + bar_width for i in index], avg_bb_times, width=bar_width, label='RBE BB')

# Add labels and title
plt.xlabel('Change Number')
plt.ylabel('Average Build Time (seconds)')
plt.title('Average Build Times for RBE GCP and RBE BB Across Change Numbers')
plt.xticks([i + bar_width/2 for i in index], avg_gcp_times.index)  # Use index from avg_gcp_times as x-axis labels
plt.legend()

# Show the plot
plt.show()
