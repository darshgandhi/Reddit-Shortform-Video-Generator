import praw
import os
from dotenv import load_dotenv
from better_profanity import profanity
import pandas as pd
from .text_cleaner import sanitize_text

# Load environment variables at module level
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

def get_posts(config):

    # Set up Reddit Client (readonly)
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT  
    )

    # Set up reddit data list (used for output.xlsx)
    reddit_data = [["Title", "Description", "Comments", "Post URL"]]

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

        title = post.title
        title = title.replace("AITA", "Am I the A-hole")

        description_text = post.selftext
        cleaned_text = sanitize_text(description_text)
        cleaned_text = cleaned_text.replace("AITA", "Am I the A-hole")

        comments_str = ""
        if config["comments"].get("get_comments"):
            comment_limit = config["comments"].get("comment_limit", 5)  # Default to 5
            post.comments.replace_more(limit=0)  # Remove 'MoreComments'
            comments = []
            count = 0
            for comment in post.comments:
                if count >= comment_limit:
                    break
                if comment.body:  # Ensure it's a real comment
                    comments.append(f"id: {comment.id} - {comment.body.strip()}")
                    count += 1
            comments_str = "\n".join(comments)

        reddit_data.append([title, cleaned_text, comments_str, post.url])
    
    return reddit_data