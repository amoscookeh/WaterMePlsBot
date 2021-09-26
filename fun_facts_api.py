import os

import praw
import random

# PASSWORD = os.environ['REDDIT_PASSWORD']
PASSWORD = "Weilsoma13"

reddit = praw.Reddit(client_id="8ZETxx_lxHX5b6exbgMBzw",  # your client id
                     client_secret="88ZP0r0jT56J_jpCI5h5fc_eZr798g",  # your client secret
                     user_agent="watermeplsbot",  # user agent name
                     username="watermeplsbot",  # your reddit username
                     password=PASSWORD)  # your reddit password


def get_nature_facts():
    sub = ['Awwducational']  # make a list of subreddits you want to scrape the data from

    for s in sub:
        subreddit = reddit.subreddit(s)  # Chosing the subreddit

    queries = ['plants', 'arctic', 'beach', 'environment', 'island', 'sea', 'fish', 'insects', 'fungus']

    random_idx = random.randint(0, len(queries) - 1)
    random_query = [queries[random_idx]]
    query_limit = 50
    random_idx = random.randint(0, query_limit / 2)
    posts = []

    for item in random_query:
        post_dict = {
            "title": [],  # title of the post
            # "score": [],  # score of the post
            # "id": [],  # unique id of the post
            "url": [],  # url of the post
            # "comms_num": [],  # the number of comments on the post
            # "created": [],  # timestamp of the post
            "body": []  # the description of post
        }
        for submission in subreddit.search(random_query, sort="top", limit=query_limit):
            post_dict["title"].append(submission.title)
            # post_dict["score"].append(submission.score)
            # post_dict["id"].append(submission.id)
            post_dict["url"].append(submission.url)
            # post_dict["comms_num"].append(submission.num_comments)
            # post_dict["created"].append(submission.created)
            post_dict["body"].append(submission.selftext)

            posts.append(post_dict)

    return posts[random_idx]


def main():
    print(get_nature_facts())


if __name__ == '__main__':
    main()
