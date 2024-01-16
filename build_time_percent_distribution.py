import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('changes_revision_rbe_time.csv')

# Remove outliers
outliers = [1293.55, 868.68]
df = df[~df['rbe_bb_time_minutes'].isin(outliers)]

# Filter rows where 'rbe_bb_state' is 'SUCCESSFUL'
df = df[df['rbe_bb_state'] == 'SUCCESSFUL']

# Plot the frequency distribution as percentages
plt.figure(figsize=(10, 6))
plt.hist(df['rbe_bb_time_minutes'], bins=20, edgecolor='black', density=True, alpha=0.7)
plt.title('Percentage Distribution of Successful Build Times')
plt.xlabel('Build Time (minutes)')
plt.ylabel('Percentage')
plt.grid(True)
plt.show()
