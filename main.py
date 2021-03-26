import praw
import os
import pandas as pd

import dotenv
dotenv.load_dotenv()


def submission_to_dict(submission):
    """
    Convert a Submission object to a dictionary.
    """
    return {
        'Title': submission.title,
        'Category': submission.link_flair_text,
        'Comments': submission.num_comments,
        'Upvotes': submission.score,
        'Upvote Ratio': submission.upvote_ratio,
        'Created At': submission.created_utc,
        'Link': submission.url
    }


def submissions_to_csv(submissions, filename):
    """
    Convert the array of submissions to a CSV.
    """
    print(f'Working on {filename}...')
    df = pd.DataFrame.from_records([submission_to_dict(s) for s in submissions])
    print(df.head())
    print()
    df.to_csv(filename)


def make_data_dir():
    os.makedirs('data', exist_ok=True)


def main():
    make_data_dir()
    reddit = praw.Reddit(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        password=os.environ['PASSWORD'],
        username=os.environ['USERNAME'],
        user_agent='scraper by u/preyneyv'
    )

    reddit.read_only = True

    s = reddit.subreddit('leagueoflegends')

    submissions_to_csv(s.top('all', limit=100), 'data/top-all.csv')
    submissions_to_csv(s.top('month', limit=100), 'data/top-month.csv')
    submissions_to_csv(s.top('week', limit=100), 'data/top-week.csv')
    submissions_to_csv(s.hot(limit=100), 'data/hot.csv')
    submissions_to_csv(s.controversial('all', limit=100), 'data/controversial-all.csv')
    submissions_to_csv(s.controversial('month', limit=100), 'data/controversial-month.csv')


if __name__ == '__main__':
    main()
