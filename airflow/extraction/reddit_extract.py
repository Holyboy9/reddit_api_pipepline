import pandas as pd
import numpy as np
import praw
import datetime
import pathlib
import sys
from validation import validation_input
import configparser


parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.resolve()
config_file = "configuration.conf"
parser.read(f"{script_path}/{config_file}")

#configuration variables
CLIENT_SECRET = parser.get("reddit_config","secret")
CLIENT_ID = parser.get("reddit_config","client_id")

POST_FIELDS = (
    "id",
    "title",
    "score",
    "num_comments",
    "author",
    "created_utc",
    "url",
    "upvote_ratio",
    "over_18",
    "edited",
    "spoiler",
    "stickied",
)

try:
    output_name = sys.argv[1]
except Exception as e:
    print(f"Error with file input. Error {e}")
    sys.exit(1)
date_dag_run = datetime.datetime.strptime(output_name, "%Y%m%d")


def main():
    """Extract Reddit data and load to CSV"""
    validation_input(output_name)
    reddit_instance = api_connect()
    subreddit_posts_object = subreddit_posts(reddit_instance)
    extracted_data = extract_data(subreddit_posts_object)
    transformed_data = transform_basic(extracted_data)
    load_to_csv(transformed_data)

#function to connect to reddit
def api_connect():
    """connect to reddit api"""
    try:
        reddit = praw.reddit(
            client_id = CLIENT_ID,
            client_secret = CLIENT_SECRET,
            user_agent = "my user agent"

        )
        return reddit
    except Exception as e:
        print(f"Unable to connect to API.Error {e} ")
        sys.exit(1)


def subreddit_posts(reddit_instance):
    """create posts object for reddit instance"""
    try:
        subreddit = reddit_instance.subreddit("dataengineering")
        posts = subreddit.top(time_filter="day",limit=None)
        
    except Exception as e:
        print(f"There has been an issue.Error {e}")
        sys.exit(1)


def extract_data(posts):
    """Extract Data to Pandas DataFrame object"""
    list_of_items = []
    try:
        for submission in posts:
            to_dict = vars(submission)
            sub_dict = {field: to_dict[field] for field in POST_FIELDS}
            list_of_items.append(sub_dict)
            extracted_data_df = pd.DataFrame(list_of_items)
    except Exception as e:
        print(f"There has been an issue. Error {e}")
        sys.exit(1)

    return extracted_data_df

def transform_basic(df):
    """Some basic transformation of data. To be refactored at a later point."""

    # Convert epoch to UTC
    df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")
    # Fields don't appear to return as booleans (e.g. False or Epoch time). Needs further investigation but forcing as False or True for now.
    # TODO: Remove all but the edited line, as not necessary. For edited line, rather than force as boolean, keep date-time of last
    # edit and set all else to None.
    df["over_18"] = np.where(
        (df["over_18"] == "False") | (df["over_18"] == False), False, True
    ).astype(bool)
    df["edited"] = np.where(
        (df["edited"] == "False") | (df["edited"] == False), False, True
    ).astype(bool)
    df["spoiler"] = np.where(
        (df["spoiler"] == "False") | (df["spoiler"] == False), False, True
    ).astype(bool)
    df["stickied"] = np.where(
        (df["stickied"] == "False") | (df["stickied"] == False), False, True
    ).astype(bool)
    return df


def load_to_csv(extracted_data_df):
    """Save extracted data to CSV file in /tmp folder"""
    extracted_data_df.to_csv(f"/tmp/{output_name}.csv", index=False)


if __name__ == "__main__":
    main()