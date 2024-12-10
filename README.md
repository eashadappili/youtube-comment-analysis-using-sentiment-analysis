# Sentiment Analysis on Youtube Comments
This project performs sentiment analysis on comments retrieved from a YouTube video using the Lexicon-based method. It leverages APIs and libraries to fetch, preprocess, filter, and analyze YouTube comments. A graphical representation of the sentiment distribution is provided.

## Features
1. Fetch comments from any YouTube video using its URL.
2. Clean and preprocess comments by removing URLs, special characters, and excessive whitespace.
3. Filter out irrelevant comments based on text-to-emoji ratio.
4. Perform sentiment analysis using the VADER Sentiment Analyzer.
5. Save comments and analysis results to text files.
6. Visualize sentiment scores with matplotlib.

## How It Works
1. Fetching YouTube Comments
Uses the googleapiclient.discovery module to interact with the YouTube API.
Retrieves the video metadata and comments.
Handles pagination to fetch all available comments.
2. Preprocessing Comments
Cleans comments by:
Removing URLs and special characters using re.
Stripping whitespace and converting text to lowercase.
3. Filtering Comments
Filters comments with a text-to-emoji ratio threshold (default: 65% text).
Uses the emoji library to count emojis in each comment.
4. Sentiment Analysis
Analyzes comment sentiments using the VADER Sentiment Analyzer.
Categorizes comments as Positive, Negative, Neutral, or Mixed.
5. Visualization
Visualizes sentiment distribution using matplotlib, Excel.

## Prerequisites
1. googleapiclient
2. re
3. emoji
4. vaderSentiment
5. matplotlib

## Install modules using pip:
pip install google-api-python-client emoji vaderSentiment matplotlib

## Setup and Usage
1. Get an API Key
Obtain an API key from the Google Cloud Console.
2. Run the Script
Clone the repository.
Replace the api_key variable in the script with your Google API key.
3. Run the script:
python youtube_comments_analysis.py
Enter the YouTube video URL when prompted.

# Outputs
youtubecomments.txt: Contains the filtered comments.
Sentiment Analysis Results: Displays sentiment scores and visualizations.

## Sample Result
Example of sentiment analysis results:

Positive: 65%
Neutral: 25%
Negative: 10%

