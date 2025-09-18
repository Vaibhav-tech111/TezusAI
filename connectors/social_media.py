import os
from typing import List, Dict, Any
from socialreaper import Facebook, Twitter, Reddit, Youtube

class SocialMediaConnector:
    def __init__(self, facebook_api_key: str, twitter_app_key: str, twitter_app_secret: str, 
                 twitter_oauth_token: str, twitter_oauth_token_secret: str, reddit_client_id: str,
                 reddit_client_secret: str, youtube_api: Youtube):
        self.facebook = Facebook(api_key=facebook_api_key)
        self.twitter = Twitter(app_key=twitter_app_key, app_secret=twitter_app_secret, 
                               oauth_token=twitter_oauth_token, oauth_token_secret=twitter_oauth_token_secret)
        self.reddit = Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret)
        self.youtube = youtube_api

    def get_facebook_comments(self, page: str, post_count: int = 10) -> List[Dict[str, Any]]:
        if not page:
            raise ValueError("Page name cannot be empty.")
        if not isinstance(post_count, int) or post_count <=0:
            raise ValueError("Post count must be a positive integer.")
        try:
            return self.facebook.page_posts_comments(page, post_count=post_count)
        except Exception as e:
            raise RuntimeError(f"Error fetching Facebook comments: {e}")

    def get_twitter_tweets(self, username: str, count: int = 10) -> List[Dict[str, Any]]:
        if not username:
            raise ValueError("Username cannot be empty.")
        if not isinstance(count, int) or count <= 0:
            raise ValueError("Count must be a positive integer.")
        try:
            return self.twitter.user(username, count=count)
        except Exception as e:
            raise RuntimeError(f"Error fetching Twitter tweets: {e}")

    def get_reddit_comments(self, subreddit: str, thread_count: int = 5) -> List[Dict[str, Any]]:
        if not subreddit:
            raise ValueError("Subreddit name cannot be empty.")
        if not isinstance(thread_count, int) or thread_count <= 0:
            raise ValueError("Thread count must be a positive integer.")
        try:
            return self.reddit.subreddit_thread_comments(subreddit, thread_count=thread_count)
        except Exception as e:
            raise RuntimeError(f"Error fetching Reddit comments: {e}")

    def get_youtube_comments(self, channel_id: str, keywords: List[str]) -> List[Dict[str, Any]]:
        if not channel_id:
            raise ValueError("Channel ID cannot be empty.")
        if not keywords:
            raise ValueError("Keywords list cannot be empty.")
        try:
            return self.youtube.channel_video_comments(channel_id, comment_text=keywords)
        except Exception as e:
            raise RuntimeError(f"Error fetching YouTube comments: {e}")