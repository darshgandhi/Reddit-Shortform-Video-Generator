import json
import pandas as pd
from reddit.praw_scraper import get_posts
from reddit.get_screenshots import get_screenshots
from tts.default_tts import create_tts_subtitles

if __name__ == "__main__":
    # Load config
    with open("./json/scraper_config.json", "r") as f:
        config = json.load(f)

    # Retrieve reddit data and store to output
    print(f"Gathering Post...")
    reddit_data = get_posts(config)
    
    for post in reddit_data:
        title, cleaned_text, comments, post_url = post
        print(f"Getting Screenshots...")
        get_screenshots(post_url, comments)
        print(f"Creating TTS & Subtitles Screenshots...")
        create_tts_subtitles(title, cleaned_text, comments)
    
    print(f"Done!")