import praw
import csv
from datetime import datetime


class RedditScraper:
    def __init__(self, client_id, client_secret, username, password, user_agent):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  username=username,
                                  password=password,
                                  user_agent=user_agent)

    def scrape_lpts(self, subreddit_name, num_posts, min_score):
        # Set up CSV file for output
        filename = f"{subreddit_name}_lpts_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Score', 'Link'])

            # Scrape data from Reddit
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                top_lpt = subreddit.top(limit=num_posts)

                print(f"Top {num_posts} LifeProTips from r/{subreddit_name} with score of at least {min_score}:")
                print("="*100)

                for post in top_lpt:
                    if post.score >= min_score:
                        writer.writerow([post.title, post.score, post.url])
                        print(f"Title: {post.title}")
                        print(f"Score: {post.score}")
                        print(f"Link: {post.url}\n")

            except Exception as e:
                print(f"Error scraping data from Reddit: {e}")



scraper = RedditScraper(client_id='your_client_id', 
                        client_secret='your_client_secret', 
                        username='your_username', 
                        password='your_password', 
                        user_agent='your_user_agent')

scraper.scrape_lpts(subreddit_name='LifeProTips', num_posts=50, min_score=1000)
