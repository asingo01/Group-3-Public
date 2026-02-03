import json
import requests
import csv
import os
from datetime import datetime

if not os.path.exists("data"):
    os.makedirs("data")

# -----------------------------
# Define what "source files" are
# -----------------------------
# Reasoning: code files only, so ownership/touch patterns reflect code maintenance (not docs/images).
SOURCE_EXTS = [
    ".py", ".java", ".c", ".cpp", ".h",
    ".js", ".ts", ".jsx", ".tsx",
    ".go", ".rs", ".cs", ".rb", ".php", ".kt", ".swift"
]

def is_source_file(filename):
    filename = filename.lower()
    for ext in SOURCE_EXTS:
        if filename.endswith(ext):
            return True
    return False


# GitHub Authentication function (same style as your code)
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct


# Collect (file, author, date) touches for source files
def collect_author_touches(lsttokens, repo):
    ipage = 1
    ct = 0
    touches = []  # list of tuples: (filename, author, date)

    try:
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            if jsonCommits is None:
                print("Error receiving commit page")
                break

            if len(jsonCommits) == 0:
                break

            for shaObject in jsonCommits:
                sha = shaObject['sha']

                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                if shaDetails is None:
                    continue

                # Get author name + date from commit metadata
                commitObj = shaDetails.get("commit", {})
                authorObj = commitObj.get("author", {}) or {}
                author = authorObj.get("name", "Unknown")
                date = authorObj.get("date", "")

                # Files touched in this commit
                filesjson = shaDetails.get('files', [])
                for filenameObj in filesjson:
                    filename = filenameObj.get('filename', '')
                    if filename and is_source_file(filename):
                        touches.append((filename, author, date))
                        print(filename, author, date)

            ipage += 1

    except:
        print("Error receiving data")
        exit(0)

    return touches


# -----------------------------
# Main
# -----------------------------
repo = 'scottyab/rootbeer'

# put your tokens here (DO NOT COMMIT THEM)
lstTokens = ["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"]

touches = collect_author_touches(lstTokens, repo)

print("Total source-file touch events:", len(touches))

repo_name = repo.split('/')[1]
fileOutput = 'data/file_' + repo_name + '_touches_by_author.csv'

fileCSV = open(fileOutput, 'w', newline='', encoding="utf-8")
writer = csv.writer(fileCSV)
writer.writerow(["Filename", "Author", "Date"])
for (filename, author, date) in touches:
    writer.writerow([filename, author, date])
fileCSV.close()

print("Wrote:", fileOutput)