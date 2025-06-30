import praw
import json
import os
from dotenv import load_dotenv

# Load Client Data
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

# Set up Reddit Client (readonly)
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT  
)

# Load config
with open("./json/scraper_config.json", "r") as f:
    config = json.load(f)

# Apply configs
subreddit_name = config.get("subreddit")
num_posts = config["filters"].get("num_posts", 10)
time_range = config["filters"].get("time_range", "week")
sort_by = config["filters"].get("sort_by", "top")

# Fetch posts
subreddit = reddit.subreddit(subreddit_name)
if sort_by == "top":
    posts = subreddit.top(time_filter=time_range, limit=num_posts)
elif sort_by == "hot":
    posts = subreddit.hot(limit=num_posts)
else:
    posts = subreddit.new(limit=num_posts)

for post in posts:
    if not config["filters"].get("nsfw") and post.over_18:
        continue  # skip NSFW if filter is off
    print(f"Title: {post.title}")
    print(f"Description: {post.selftext}\n")