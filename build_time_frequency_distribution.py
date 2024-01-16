import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('changes_revision_rbe_time.csv')

# Remove outliers
outliers = [1293.55, 868.68]
df = df[~df['rbe_bb_time_minutes'].isin(outliers)]

# Plot the frequency distribution
plt.figure(figsize=(10, 6))
plt.hist(df['rbe_bb_time_minutes'], bins=20, edgecolor='black')
plt.title('Frequency Distribution of Build Times')
plt.xlabel('Build Time (minutes)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
