# YouTube History Extractor

This tool extracts YouTube URLs from Google Takeout HTML history files. It's especially useful when recovering playlists after account deletion or when transferring data to a new account.

## Purpose

If your YouTube account was deleted and you need to recreate your playlists, this tool can help. It extracts all YouTube links from your Google Takeout history data and saves them to a CSV file, which can then be processed with tools like n8n to recreate your playlists.

## Features

- Handles large HTML files (50MB+) by processing in chunks
- Extracts YouTube, YouTube Music, and YouTube Studio URLs
- Identifies which service each URL belongs to
- Saves results to a CSV file that can be used in workflow automation tools
- Removes duplicate URLs

## Requirements

- Python 3.6 or higher
- beautifulsoup4
- pandas

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Arthurkhan/youtube-history-extractor.git
   cd youtube-history-extractor
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```
   python extract_youtube_urls.py
   ```

2. When prompted, enter the full path to your HTML history file from Google Takeout
3. Enter the path where you want to save the CSV file (or press Enter to use the default)
4. The script will process the file and save the results

## Output

The script creates a CSV file with two columns:
- "service" - Contains "YouTube", "YouTube Music", or "YouTube Studio"
- "url" - Contains the full YouTube URL

## Next Steps

You can use the generated CSV file with workflow automation tools like n8n to:
- Fetch video information for each URL
- Categorize videos by genre or content type
- Recreate playlists based on categories
- Resubscribe to channels

## License

MIT
