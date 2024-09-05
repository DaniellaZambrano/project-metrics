# project-metrics / GitHub Issues Analysis and Visualization

## Overview

This project provides a Python script to analyze and visualize GitHub issues from a specified repository. The script uses the GitHub API to fetch issues with a specific label (e.g., "bug"), saves the data to a CSV file, and generates a bar chart showing the number of issues per day.

## Features

- Fetches issues from a GitHub repository using the GitHub API.
- Filters issues based on a specific label.
- Saves the filtered issues to a CSV file.
- Generates a bar chart visualizing the number of issues per day.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `requests`
  - `pandas`
  - `matplotlib`
  - `python-dotenv`

## Installation

1. Clone the repository or download the script files.

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project directory with the following content:

    ```plaintext
    GITHUB_TOKEN=your_github_token
    ```

   Replace `your_github_token` with your actual GitHub token. Ensure the token has the necessary permissions to access the repository.

## Usage

1. Edit the script to set the correct `USER_GITHUB` and `REPOSITORY` variables in the script:

    ```python
    USER_GITHUB = 'your_repository_owner'
    REPOSITORY = 'your_repository_name'
    ```

   Replace `your_repository_owner` with the username or organization name, and `your_repository_name` with the repository name.

2. Run the script:

    ```bash
    python generate_stadistics.py
    ```

3. The script will:
   - Fetch issues from the specified GitHub repository.
   - Filter issues with the label "bug".
   - Save the data to `issues.csv`.
   - Generate and save a bar chart as `issues_per_day_bars.png`.

## Output

- `issues.csv`: A CSV file containing issue details (number, title, and creation date).
- `issues_per_day_bars.png`: A bar chart image showing the number of issues per day.

## Troubleshooting

- **Error 401**: If you encounter a 401 error, ensure that your GitHub token is correct and has the appropriate permissions. Verify that the token is correctly set in the `.env` file.

- **Missing Libraries**: Ensure all required libraries are installed. You can use `pip install -r requirements.txt` if you have a `requirements.txt` file listing the libraries.