import praw
import requests
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
PW = os.environ.get("PW")
USERNAME = os.environ.get("USERNAME")

def scrape_carousel_images(post_url, output_folder="./pics"):
    # Initialize the Reddit API client
    reddit = praw.Reddit(client_id=ID,
                         client_secret=SECRET,
                         user_agent=USERAGENT,
                         password=PW,
                         username=USERNAME)
    print(reddit.user.me())
    submission_id = reddit.submission(url=post_url).id

    # Get the submission data
    submission = reddit.submission(id=submission_id)

    # Check if the submission has media_metadata (indicating it's an album)
    if submission.media_metadata:
        for media_id, media_data in submission.media_metadata.items():
            if 's' in media_data and 'u' in media_data['s']:
                image_url = media_data['s']['u']
                # Download the image
                download_image(image_url, output_folder)
    else:
        print("The post doesn't contain a carousel.")

def download_image(url, output_folder="\pics"):
    os.makedirs(output_folder, exist_ok=True)
    url = url.split("?")[0].replace("preview", "i")
    image_response = requests.get(url)
    if image_response.status_code == 200:
        image_filename = os.path.join(output_folder, os.path.basename(url))
        with open(image_filename, 'wb') as image_file:
            image_file.write(image_response.content)
        print(f"Image downloaded and saved as {image_filename}")
    else:
        print(f"Failed to download image from {url}")

if __name__ == '__main__':
    url = "some carousel"
    scrape_carousel_images(url)
