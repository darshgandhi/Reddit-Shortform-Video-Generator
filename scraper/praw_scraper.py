import praw
import json
import os
from dotenv import load_dotenv
from better_profanity import profanity
import pandas as pd
from text_cleaner import sanitize_text

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

# Set up xl Workbook
reddit_data = [["Title", "Description"]]

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

posts = list(posts)  # Convert to list to count and reuse
print(f"Fetched {len(posts)} posts from r/{subreddit_name}")

for post in posts:
    if not config["filters"].get("nsfw") and post.over_18:
        continue  # skip NSFW if filter is off
    print(f"Title: {post.title}")
    title = post.title
    title = title.replace("AITA", "Am I the Asshole")

    description_text = post.selftext
    print(f"Cleaned Description: {description_text}\n")

    cleaned_text = sanitize_text(description_text)
    cleaned_text = cleaned_text.replace("AITA", "Am I the Asshole")

    reddit_data.append([title, cleaned_text])

df = pd.DataFrame(reddit_data)
df = pd.DataFrame(reddit_data[1:], columns=reddit_data[0])
df.to_excel('./data/audio/output.xlsx', index=False)