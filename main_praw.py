import praw
import requests
import re
import os
from dotenv import load_dotenv

# relative path
current_directory = os.path.dirname(__file__)
os.chdir(current_directory)

# get the vars
load_dotenv()

ID = os.environ.get("ID")
SECRET = os.environ.get("SECRET")
USERAGENT = os.environ.get("USERAGENT")
PWR = os.environ.get("PWR")
USER = os.environ.get("USER")


def scrape_top_of_day(sub, output_folder="./pics"):
    # Initialize the Reddit API client
    reddit = praw.Reddit(client_id=ID,
                         client_secret=SECRET,
                         user_agent=USERAGENT,
                         password=PWR,
                         username=USER)
    print(reddit.user.me())
    subreddit = reddit.subreddit(sub)
    day_tops = subreddit.top(time_filter='day', limit=10)

    for day_top in day_tops:
        if day_top.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
            image_url = day_top.url
            download_image(image_url, output_folder)
            break
        else:
            print("Top post of the day does not contain an image.")
            
def scrape_last_posts(sub, num_posts=1, output_folder="./pics"):
    # Initialize the Reddit API client
    reddit = praw.Reddit(client_id=ID,
                         client_secret=SECRET,
                         user_agent=USERAGENT,
                         password=PWR,
                         username=USER)
    print(reddit.user.me())

    subreddit = reddit.subreddit(sub)
    new_posts = subreddit.new(limit=num_posts)
    for post in new_posts:
        if post.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
            image_url = post.url
            download_image(image_url, output_folder)
            
def clean_filename(filename):
    # Remove invalid characters from the filename
    return re.sub(r'[\/:*?"<>|]', '', filename)

def download_image(url, output_folder="\pics"):
    os.makedirs(output_folder, exist_ok=True)
    image_response = requests.get(url)
    if image_response.status_code == 200:
        image_filename = os.path.join(output_folder, os.path.basename(url))
        with open(image_filename, 'wb') as image_file:
            image_file.write(image_response.content)
        print(f"Image downloaded and saved as {image_filename}")
    else:
        print(f"Failed to download image from {url}")

if __name__ == '__main__':
    sub = "IllegallySmolCats"
    scrape_top_of_day(sub)