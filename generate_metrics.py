import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd

# Defines the GitHub GraphQL API URL
url = "https://api.github.com/graphql"

load_dotenv()

token = os.getenv('GITHUB_TOKEN')
project_id = os.getenv('TOKEN_ID_PROJECT')


if not token or not project_id:
    raise ValueError("Be sure to set the 'GITHUB_TOKEN' and 'TOKEN_ID_PROJECT' environment variables.")


# Define the GraphQL query, making sure to replace "project_id" with the actual project ID
query = f"""
query {{
  node(id: "{project_id}") {{
    ... on ProjectV2 {{
      items(first: 100) {{
        nodes {{
          id
          createdAt
          type
          isArchived
          content {{
            ... on Issue {{
              id
              databaseId
              number
              title
              url
              createdAt
              author {{
                login
              }}
              assignees(first: 10) {{
                nodes {{
                  login
                }}
              }}
              labels(first: 10) {{
                nodes {{
                  name
                }}
              }}
              closed
              closedAt
              milestone {{
                number
                title
                state
              }}
              repository {{
                name
              }}
            }}
          }}
          fieldValues(first: 10) {{
            nodes {{
              ... on ProjectV2ItemFieldSingleSelectValue {{
                optionId
                field {{
                  ... on ProjectV2SingleSelectField {{
                    id
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}
"""

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(url, json={'query': query}, headers=headers)


if response.status_code == 200:
    data = response.json()

    items = data['data']['node']['items']['nodes']

    column_list = []
    for item in items:
        type = item.get('type', '')
        if type in ["ISSUE"]:
            content = item.get('content', {})    
            field_values = item.get('fieldValues', {}).get('nodes', [])
            for field in field_values:
              if 'optionId' in field:              
                # Filter specific fields
                filtered_content = {
                    'number': content.get('number'),
                    'title': content.get('title'),
                    'createdAt': content.get('createdAt'),
                    'optionId': field['optionId']
                }

            column_list.append(filtered_content)

    
    df = pd.DataFrame(column_list)
    
    # optionId parse to string value
    option_mapping = {}
    for key, value in os.environ.items():
        if key.startswith('STATUS_ID_'):
            option_id = key.replace('STATUS_ID_', '')  # ID
            option_mapping[option_id] = value

    option_mapping = {v: k for k, v in option_mapping.items()}

    # Mapping the ids
    df['optionId'] = df['optionId'].astype(str).map(option_mapping)
    # Handle possible NaN values ​​if some ID has no mapping
    df['optionId'] = df['optionId'].fillna('Unknown Option')

    df.to_csv('tickets_per_issues.csv', index=False)
    
    # Convert 'createdAt' column to date format
    df['createdAt'] = pd.to_datetime(df['createdAt'])
    # Extract only date (without time) from 'createdAt' column
    df['createdAt'] = df['createdAt'].dt.date
    # Group by date and count how many entries there are per day
    # date_counts = df.groupby('createdAt').size().reset_index(name='count')

    date_counts = df.groupby(['createdAt', 'optionId']).size().reset_index(name='count')

    # Save the data to excel
    df.to_excel('tickets_per_issues.xlsx', index=False)
    date_counts.to_excel('count_per_issues-day.xlsx', index=False)
    print("Saved data in 'tickets_per_issues.csv'.")


else:
    print(f"Error: {response.status_code}, {response.text}")
