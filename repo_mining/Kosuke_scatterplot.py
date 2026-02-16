import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Read the data from CSV
repo = 'rootbeer'  # Change if analyzing a different repo
csv_file = f'data/author_file_touches_{repo}.csv'


filenames = []
authors = []
weeks = []

print(f"Reading data from {csv_file}...")


with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        filenames.append(row['Filename'])
        authors.append(row['Author'])
        weeks.append(float(row['Weeks_Since_Start']))

# Get unique authors and assign colors
unique_authors = sorted(list(set(authors)))
colors_list = plt.cm.tab20(np.linspace(0, 1, len(unique_authors)))

# Create a color map for each author
author_color_map = {author: colors_list[i] for i, author in enumerate(unique_authors)}

# Map each data point to its author's color
point_colors = [author_color_map[author] for author in authors]

# Get unique files for x-axis
unique_files = sorted(list(set(filenames)))
file_to_x = {file: i for i, file in enumerate(unique_files)}

# Map filenames to x-coordinates
x_coords = [file_to_x[filename] for filename in filenames]

# Create the scatter plot
plt.figure(figsize=(14, 8))
plt.scatter(x_coords, weeks, c=point_colors, alpha=0.6, s=50)

# Set up the plot
plt.xlabel('File', fontsize=12)
plt.ylabel('Weeks', fontsize=12)
plt.title(f'Developer Activity Over Time - Rootbeer Repository', fontsize=14, fontweight='bold')

# X-axis: show only EVEN file indices
max_file_index = len(unique_files) - 1
even_indices = [i for i in range(0, len(unique_files)) if i % 2 == 0]
plt.xticks(even_indices, even_indices, fontsize=10)

# Set x-axis limits to show all data
plt.xlim(-1, max_file_index + 1)

# Create legend for authors (only show top 10-15 if too many)
if len(unique_authors) <= 15:
    legend_authors = unique_authors
else:
    # Count touches per author
    author_counts = {}
    for author in authors:
        author_counts[author] = author_counts.get(author, 0) + 1
    
    # Get top 15 most active authors
    top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:15]
    legend_authors = [author for author, _ in top_authors]

legend_patches = [mpatches.Patch(color=author_color_map[author], label=author) 
                  for author in legend_authors]

plt.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5), 
           fontsize=9, title='Authors')

plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the plot
output_file = f'data/scatterplot_{repo}.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nScatter plot saved to {output_file}")

# Also create a file mapping showing which file number corresponds to which filename
mapping_file = f'data/file_mapping_{repo}.txt'
with open(mapping_file, 'w', encoding='utf-8') as f:
    f.write("File Index to Filename Mapping:\n")
    f.write("="*60 + "\n")
    for i, filename in enumerate(unique_files):
        f.write(f"{i}: {filename}\n")

print(f"File mapping saved to {mapping_file}")

# Show the plot
plt.show()

print(f"\nSummary:")
print(f"Total data points: {len(weeks)}")
print(f"Unique files: {len(unique_files)}")
print(f"Unique authors: {len(unique_authors)}")
print(f"Time span: {min(weeks):.1f} to {max(weeks):.1f} weeks")