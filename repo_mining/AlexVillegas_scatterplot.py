import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# ----------------------------------------
# Configuration
# ----------------------------------------
# GitHub repos:
CSV_FILE = "data/file_rootbeer.csv"
# CSV_FILE = "data/file_backpack_authors.csv"
# CSV_FILE = "data/file_k-9_authors.csv"
# CSV_FILE = "data/file_gpslogger.csv"

# ----------------------------------------
# Helper functions
# ----------------------------------------

def date_to_week(date_str):
  # convert ISO date string to sortable year-week integer
  # ex: 2023-12 -> 202312
  dt = datetime.fromisoformat(date_str.replace("Z", ""))
  year, week, _ = dt.isocalendar()
  return week

# ----------------------------------------
# Read CSV and reconstruct dictfiles
# ----------------------------------------
# (author, week) -> set of files

author_week_files = defaultdict(set)

with open(CSV_FILE, newline="", encoding="utf-8") as f:
  reader = csv.DictReader(f)
  for row in reader:
    author = row["Author"]
    filename = row["Filename"]
    week = date_to_week(row["Date"])

    author_week_files[(author, week)].add(filename)

# ----------------------------------------
# Collect unique authors
# ----------------------------------------

authors = sorted({
  author for author, _ in author_week_files.keys()
})

# ----------------------------------------
# Assign colors to authors
# ----------------------------------------

cmap = plt.get_cmap("tab10")
author_to_color = {
  author: cmap(i % 10) for i, author in enumerate(authors)
}

# ----------------------------------------
# Build scatter data
# ----------------------------------------

x_vals = [] # number of files touched
y_vals = [] # week
colors = []

for (author, week), files in author_week_files.items():
  x_vals.append(len(files))
  y_vals.append(week)
  colors.append(author_to_color[author])

# ----------------------------------------
# Plot
# ----------------------------------------

plt.figure(figsize=(12, 8))
plt.scatter(
  x_vals,
  y_vals,
  c=colors,
  alpha=0.7,
  s=20
)

plt.xlabel("Files")
plt.ylabel("Weeks")
plt.title("File Touches Over Time by Author")


# ----------------------------------------
# Legend
# ----------------------------------------

legend_handles = [
  plt.Line2D(
    [0], [0],
    marker='o',
    linestyle='',
    label=author,
    markerfacecolor=color,
    markeredgecolor='black',
    markersize=8
  )
  for author, color in author_to_color.items()
]

plt.legend(
  handles=legend_handles,
  title="Author",
  bbox_to_anchor=(1.02, 1),
  loc="upper left"
)

plt.tight_layout()
plt.show()