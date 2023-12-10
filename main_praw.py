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
USER = os.environ.get("USER")

def download_top_image(subreddit_name, output_folder="."):
    # Initialize the Reddit API client
    reddit = praw.Reddit(client_id=ID,
                         client_secret=SECRET,
                         user_agent=USER)

    # Get the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Get the top post from the subreddit
    top_post = subreddit.top(limit=1)

    # Get the image URL from the post
    image_url = top_post.url

    # Download the image
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        # Save the image locally
        image_filename = os.path.join(output_folder, f"{subreddit_name}_top_image.jpg")
        with open(image_filename, 'wb') as image_file:
            image_file.write(image_response.content)
        print(f"Top image downloaded and saved as {image_filename}")
    else:
        print("Failed to download image.")

# Example usage
download_top_image("python")  # Replace with the desired subreddit name
