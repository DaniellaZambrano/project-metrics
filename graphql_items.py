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

    status_id = os.getenv('STATUS_ID_In_Testing')

    items = data['data']['node']['items']['nodes']
    
    option_ids = []
    for item in items:
        field_values = item.get('fieldValues', {}).get('nodes', [])
        for field in field_values:
            if 'optionId' in field:
                # print(f"Option ID: {field['optionId']}")
                option_ids.append(field['optionId'])

    count = 0
    for option in option_ids:
      if status_id == option:
        count = count + 1


    res = []
    content_list = []
    for item in items:
        content = item.get('content', {})
        # Filter specific fields
        filtered_content = {
            'number': content.get('number'),
            'title': content.get('title'),
            'createdAt': content.get('createdAt')
        }
        content_list.append(filtered_content)
        if 'number' in content:
            res.append(content['number'])


    column_list = []
    for item in items:
        field_values = item.get('fieldValues', {}).get('nodes', [])
        for field in field_values:
            if 'optionId' in field:
                if field['optionId'] == status_id:
                    content = item.get('content', {})                  
                    # Filter specific fields
                    filtered_content = {
                        'number': content.get('number'),
                        'title': content.get('title'),
                        'createdAt': content.get('createdAt')
                    }
                    column_list.append(filtered_content)

    df = pd.DataFrame(column_list)
    df.to_csv('issues_per_column.csv', index=False)
    print("Saved data in 'issues_per_column.csv'.")


else:
    print(f"Error: {response.status_code}, {response.text}")
