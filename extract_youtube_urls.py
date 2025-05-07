import re
import os
import csv
from bs4 import BeautifulSoup
import pandas as pd

# Ask for the HTML file path
html_file_path = input("Enter the full path to your HTML history file: ")
output_file_path = input("Enter the path where you want to save the CSV file: ") or "youtube_links.csv"

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

# Read the HTML file and extract YouTube URLs
youtube_data = []
youtube_pattern = re.compile(r'(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s"\'\\\/<>]+)')
service_pattern = re.compile(r'youtube music|youtube', re.IGNORECASE)

try:
    # Process in chunks
    html_content = ""
    with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for chunk in read_in_chunks(file):
            # Find all YouTube URLs in this chunk
            youtube_matches = youtube_pattern.findall(chunk)
            
            # For each match, try to find the service name near the URL
            for url in youtube_matches:
                # Look for service name within 200 characters before the URL
                context_start = max(0, chunk.find(url) - 200)
                context_end = chunk.find(url)
                context = chunk[context_start:context_end]
                
                name = "YouTube"  # Default
                service_match = service_pattern.search(context)
                if service_match:
                    matched_text = service_match.group(0).lower()
                    if "music" in matched_text:
                        name = "YouTube Music"
                    else:
                        name = "YouTube"
                
                youtube_data.append({
                    'name': name,
                    'url': url
                })
    
    # Create a DataFrame and save to CSV
    if youtube_data:
        df = pd.DataFrame(youtube_data)
        # Remove duplicates
        df = df.drop_duplicates(subset=['url'])
        df.to_csv(output_file_path, index=False, quoting=csv.QUOTE_ALL)
        print(f"Successfully extracted {len(youtube_data)} YouTube URLs and saved to {output_file_path}")
        print(f"After removing duplicates: {len(df)} unique URLs")
    else:
        print("No YouTube URLs found in the file.")
        
except Exception as e:
    print(f"An error occurred: {e}")
