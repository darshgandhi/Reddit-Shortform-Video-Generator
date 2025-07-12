import json
import pandas as pd
from reddit.praw_scraper import get_posts

if __name__ == "__main__":
    # Load config
    with open("./json/scraper_config.json", "r") as f:
        config = json.load(f)

    # Retrieve reddit data and store to output
    reddit_data = get_posts(config)

    print(reddit_data)