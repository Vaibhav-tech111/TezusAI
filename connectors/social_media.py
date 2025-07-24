# connectors/social_media.py

from socialreaper import Facebook, Twitter, Reddit, Youtube

class SocialMediaConnector:
    def __init__(self):
        self.facebook = Facebook(api_key="your_fb_api_key")
        self.twitter = Twitter(app_key="xxx", app_secret="xxx", oauth_token="xxx", oauth_token_secret="xxx")
        self.reddit = Reddit(client_id="xxx", client_secret="xxx")
        self.youtube = Youtube(api_key="your_yt_api_key")

    def get_facebook_comments(self, page: str, post_count: int = 10):
        return self.facebook.page_posts_comments(page, post_count=post_count)

    def get_twitter_tweets(self, username: str, count: int = 10):
        return self.twitter.user(username, count=count)

    def get_reddit_comments(self, subreddit: str, thread_count: int = 5):
        return self.reddit.subreddit_thread_comments(subreddit, thread_count=thread_count)

    def get_youtube_comments(self, channel_name: str, keywords: list):
        channel_id = self.youtube.api.guess_channel_id(channel_name)[0]['id']
        return self.youtube.channel_video_comments(channel_id, comment_text=keywords)
