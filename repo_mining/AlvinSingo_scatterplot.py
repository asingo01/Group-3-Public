import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = "data/file_rootbeer_touches_by_author.csv"  # change if repo changes
OUT_PNG = "data/file_rootbeer_scatterplot.png"

def parse_date(d):
    # GitHub date looks like: 2020-01-01T12:34:56Z
    # Convert to datetime
    return datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ")

# Load touches
touches = []  # (filename, author, date_dt)
with open(DATA_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        filename = row["Filename"]
        author = row["Author"]
        date_str = row["Date"]
        if date_str.strip() == "":
            continue
        touches.append((filename, author, parse_date(date_str)))

if len(touches) == 0:
    print("No touches found. Did you run Alvin_authorsFileTouches.py first?")
    exit(0)

# Find earliest date to compute week index
min_date = min(t[2] for t in touches)

def week_index(dt):
    days = (dt - min_date).days
    return days // 7

# Map files to y-values
files = sorted(list(set(t[0] for t in touches)))
file_to_y = {files[i]: i for i in range(len(files))}

# Map authors to colors
authors = sorted(list(set(t[1] for t in touches)))
cmap = plt.get_cmap("tab20")
author_to_color = {authors[i]: cmap(i % 20) for i in range(len(authors))}

# Build scatter points
xs = []
ys = []
cs = []
for (filename, author, dt) in touches:
    xs.append(file_to_y[filename])
    ys.append(week_index(dt))
    cs.append(author_to_color[author])

plt.figure(figsize=(14, max(6, len(files) * 0.18)))
plt.scatter(xs, ys, c=cs, s=18, alpha=0.8)

plt.xlabel("Files")
plt.ylabel("Weeks")
plt.title("File touches over time (colored by author)")

plt.grid(True, linestyle="--", alpha=0.4)

# Legend
handles = []
labels = []
for a in authors:
    handles.append(plt.Line2D([0], [0], marker='o', linestyle='', color=author_to_color[a]))
    labels.append(a)

plt.legend(handles, labels, title="Author", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
plt.tight_layout()

plt.savefig(OUT_PNG, dpi=200)
print("Saved plot:", OUT_PNG)
plt.show()