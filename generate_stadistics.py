import os
import requests
import pandas as pd
import csv
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GitHub token is not configured in environment variables.")

token = GITHUB_TOKEN

username =  os.getenv('USER_GITHUB')
repo = os.getenv("REPOSITORY")
url = f"https://api.github.com/repos/{username}/{repo}/issues"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}


def get_issues(state='all', labels=None):

    params = {
        "state": state,  # 'open', 'closed' o 'all'
        "labels": labels,
        "per_page": 100
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    return response

response = get_issues("all", "QA")

if response.status_code == 200:
    issues_filtered = response.json()
    
    # Create a DataFrame from the issues
    df = pd.DataFrame(issues_filtered)
    
    df['created_at'] = pd.to_datetime(df['created_at'])
    # Year and week
    df['week'] = df['created_at'].dt.strftime('%Y-%U') 

    # Save the data to a CSV file
    df.to_csv('issues_per_label.csv', columns=['number', 'title', 'created_at'], index=False)
    print("Saved data in 'issues_per_label.csv'.")
    
    # Read the csv data
    # df = pd.read_csv('issues_per_label.csv')
    # df['created_at'] = pd.to_datetime(df['created_at'])
    
    # Group by date and count issuess
    #issue_counts = df.groupby(df['created_at'].dt.date).size()
    
    # Group by week and count issuess
    issue_counts = df.groupby('week').size()

    # Ploting
    plt.figure(figsize=(10, 6))
    plt.bar(issue_counts.index, issue_counts.values, color='b', edgecolor='black')
    plt.xlabel('Date')
    plt.ylabel('Number of Issues')
    plt.title('Number of Issues per Day')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    
    # Saving
    plt.tight_layout()
    plt.savefig('issues_per_week.png')
    print("Saved as 'issues_per_week.png'.")
    plt.show()

else:
    print(f"Error in the request to the API: {response.status_code}")
