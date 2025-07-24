import json
import pandas as pd
from reddit.praw_scraper import get_posts
from reddit.get_screenshots import get_screenshots
from video_gen.video_generation import generate_video
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
        show_screenshots = get_screenshots(post_url, comments, config["comments"].get("screenshot", False))
        print(f"Generating Video...")
        generate_video(comments, show_screenshots)

    print(f"Done!")