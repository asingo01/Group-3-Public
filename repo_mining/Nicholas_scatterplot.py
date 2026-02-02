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
sizes_s = []       # New list for Touch Count

file_names = []    
author_names = []  

# 2. READ DATA
with open(file_input, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

    if not data:
        print("CSV is empty.")
        exit()

    all_dates = [datetime.strptime(row['Date'], "%Y-%m-%dT%H:%M:%SZ") for row in data]
    start_date = min(all_dates)

    for i, row in enumerate(data):
        # --- Y Axis: Weeks ---
        date_obj = all_dates[i]
        days_diff = (date_obj - start_date).days
        weeks_y.append(days_diff / 7) 

        # --- X Axis: Files ---
        fname = row['Filename']
        if fname not in file_names:
            file_names.append(fname)
        files_x.append(file_names.index(fname))

        # --- Color: Authors ---
        author = row['Author']
        if author not in author_names:
            author_names.append(author)
        authors_c.append(author_names.index(author))

        # --- Size: Touch Count ---
        # We multiply by a factor (e.g., 20) to make the differences visible
        touch_count = float(row.get('Touch Count', 1))
        sizes_s.append(touch_count * 20) 

# 3. PLOT
plt.figure(figsize=(12, 8))

# Pass sizes_s to the 's' parameter
scatter = plt.scatter(files_x, weeks_y, c=authors_c, s=sizes_s, cmap='tab20', alpha=0.6, edgecolors='w')

# 4. FORMATTING
plt.title(f'Evolution of {repo_name}: Files vs Time (Size = Touch Count)')
plt.xlabel('File Index')
plt.ylabel('Weeks Since Start')

# Legends
# Author Legend
handles, _ = scatter.legend_elements(prop="colors")
auth_legend = plt.legend(handles, author_names, title="Authors", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.gca().add_artist(auth_legend)

# Optional: Size Legend (to show what Touch Count looks like)
kw = dict(prop="sizes", num=4, color='gray', alpha=0.6, func=lambda s: s/20)
size_legend = plt.legend(*scatter.legend_elements(**kw), title="Touch Count", bbox_to_anchor=(1.05, 0.4), loc='upper left')

plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()

plt.savefig(f'data/scatterplot_{repo_name}.png')
print(f"Plot saved with Touch Count scaling.")
plt.show()