import json
import requests
import csv
from datetime import datetime
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

# Collect authors and dates for each file
def collect_author_file_touches(lsttokens, repo):
    ipage = 1
    ct = 0
    file_data = []  # Store tuples of (filename, author, date, weeks_since_start)
    
    # Define source file extensions (same as CollectFiles)
    source_extensions = ['.java', '.kt', '.gradle', '.xml', '.pro', 'c', 'c++']
    
    # Get the first commit date to calculate weeks
    first_commit_url = 'https://api.github.com/repos/' + repo + '/commits?per_page=1&page=1'
    first_commit, ct = github_auth(first_commit_url, lsttokens, ct)
    
    # We'll need to get all commits to find the earliest, so we'll track it as we go
    project_start_date = None
    
    try:
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            if len(jsonCommits) == 0:
                break
                
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                commit_date_str = shaObject['commit']['author']['date']
                commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')
                
                # Track the earliest commit date
                if project_start_date is None or commit_date < project_start_date:
                    project_start_date = commit_date
                
                # Get commit details
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                
                author = shaObject['commit']['author']['name']
                filesjson = shaDetails['files']
                
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    
                    # Only process source files
                    if any(filename.endswith(ext) for ext in source_extensions):
                        file_data.append({
                            'filename': filename,
                            'author': author,
                            'date': commit_date,
                            'date_str': commit_date_str
                        })
                        print(f"Collected: {filename} by {author} on {commit_date_str}")
            
            ipage += 1
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Calculate weeks since project start for each entry
    for entry in file_data:
        weeks_diff = (entry['date'] - project_start_date).days / 7
        entry['weeks_since_start'] = round(weeks_diff, 1)
    
    return file_data, project_start_date

# Main execution
repo = 'scottyab/rootbeer'
lstTokens = ["Secret Secret very secret"]  # Replace with your token

print("Collecting author and file touch data...")
file_touches, start_date = collect_author_file_touches(lstTokens, repo)

print(f"\nProject started on: {start_date}")
print(f"Total file touches collected: {len(file_touches)}")

# Save to CSV
file = repo.split('/')[1]
fileOutput = 'data/author_file_touches_' + file + '.csv'

with open(fileOutput, 'w', newline='', encoding='utf-8') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(['Filename', 'Author', 'Date', 'Weeks_Since_Start'])
    
    for entry in file_touches:
        writer.writerow([
            entry['filename'],
            entry['author'],
            entry['date_str'],
            entry['weeks_since_start']
        ])

print(f"\nData saved to {fileOutput}")

# Get unique authors and files
unique_authors = set(entry['author'] for entry in file_touches)
unique_files = set(entry['filename'] for entry in file_touches)

print(f"Unique source files: {len(unique_files)}")
print(f"Unique authors: {len(unique_authors)}")