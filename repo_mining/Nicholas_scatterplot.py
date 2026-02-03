import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os

# 1. SETUP
repo_name = 'rootbeer' 
file_input = f'data/authorsFile_{repo_name}.csv'

if not os.path.exists(file_input):
    print(f"File {file_input} not found.")
    exit()

weeks_y = []
files_x = []
authors_c = []

file_names = []    
author_names = []  

# 2. READ DATA
with open(file_input, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

    if not data:
        print("CSV is empty.")
        exit()

    # Sort data by date if necessary to ensure 'start_date' is accurate
    all_dates = [datetime.strptime(row['Date'], "%Y-%m-%dT%H:%M:%SZ") for row in data]
    start_date = min(all_dates)

    for i, row in enumerate(data):
        # Y Axis: Weeks
        date_obj = all_dates[i]
        days_diff = (date_obj - start_date).days
        weeks_y.append(days_diff / 7) 

        # X Axis: Files
        fname = row['Filename']
        if fname not in file_names:
            file_names.append(fname)
        files_x.append(file_names.index(fname))

        # Color: Authors
        author = row['Author']
        if author not in author_names:
            author_names.append(author)
        authors_c.append(author_names.index(author))

# 3. PLOT
# Adjusting figure size to match standard proportions
plt.figure(figsize=(8, 6))

# Set 's' to a constant value (e.g., 40) for uniform dots
# Using 'Set1' or 'tab10' for more distinct, basic colors like the image
plt.scatter(files_x, weeks_y, c=authors_c, s=40, cmap='Set1', edgecolors='none')

# 4. FORMATTING (Matching the reference style)
plt.xlabel('file')
plt.ylabel('weeks')

# Match the axis padding seen in the image
plt.xlim(-1, max(files_x) + 1)
plt.ylim(-15, max(weeks_y) + 15)

# Save and Show
plt.savefig(f'data/scatterplot_{repo_name}.png')
print(f"Plot saved as scatterplot_{repo_name}.png.")
plt.show()