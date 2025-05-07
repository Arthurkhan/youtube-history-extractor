import re
import os
import csv
from bs4 import BeautifulSoup
import pandas as pd

# Ask for the HTML file path
html_file_path = input("Enter the full path to your HTML history file: ")
output_file_path = input("Enter the path where you want to save the CSV file: ") or "youtube_music_links.csv"

print(f"Reading HTML file from: {html_file_path}")
print(f"Results will be saved to: {output_file_path}")

# Read the HTML file in chunks to handle large files
def read_in_chunks(file_object, chunk_size=1024*1024*10):  # 10MB chunks
    """Read a file in chunks to avoid memory issues with large files"""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

# Read the HTML file and extract YouTube Music URLs
youtube_music_data = []
# Pattern specifically for music.youtube.com URLs
youtube_music_pattern = re.compile(r'(https?://(?:www\.)?music\.youtube\.com/[^\s"\'\\\/<>]+)')

try:
    # Process in chunks
    with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for chunk in read_in_chunks(file):
            # Find all YouTube Music URLs in this chunk
            youtube_music_matches = youtube_music_pattern.findall(chunk)
            
            # Add each URL to our dataset
            for url in youtube_music_matches:
                youtube_music_data.append({
                    'name': "YouTube Music",
                    'url': url
                })
    
    # Create a DataFrame and save to CSV
    if youtube_music_data:
        df = pd.DataFrame(youtube_music_data)
        # Remove duplicates
        df = df.drop_duplicates(subset=['url'])
        df.to_csv(output_file_path, index=False, quoting=csv.QUOTE_ALL)
        print(f"Successfully extracted {len(youtube_music_data)} YouTube Music URLs and saved to {output_file_path}")
        print(f"After removing duplicates: {len(df)} unique URLs")
    else:
        print("No YouTube Music URLs found in the file.")
        
except Exception as e:
    print(f"An error occurred: {e}")
