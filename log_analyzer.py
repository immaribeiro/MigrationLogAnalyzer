import re
import pandas as pd

# List to hold the extracted log data
log_data = []

# Open the log file
with open("mylogfile.log", "r") as f:
    # Read the file line by line
    for line in f:
        # Use a regular expression to search for the word 'skipping' and ids in the line
        match = re.search(r'skipping\s+(\d+)', line)
        # If the word 'skipping' is found in the line
        if match:
            # Extract the ids from the line and add them to the log data
            log_data.append([match.group(1)])

# Create a DataFrame from the extracted log data
df = pd.DataFrame(log_data, columns=["Ids"])

# Print the DataFrame
print(df)
