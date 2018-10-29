import os
import sys
import json
import logging
import logging.config

from datetime import datetime

import tweepy
import pandas as pd

from main import get_media_id
from functions import get_user_id, LIB_COMMON_DIR, PROJECT_DIR
from user_data import user_data

for p in [LIB_COMMON_DIR, PROJECT_DIR]:
    sys.path.append(p)

from db_handle import insert_values

logger = logging.getLogger('main_logger')

LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
os.chdir(LOGS_DIR)


def get_account_data(api):

    my_followers = [
        x.screen_name for x in tweepy.Cursor(api.followers).items()
    ]

    my_follows = [x.screen_name for x in tweepy.Cursor(api.friends).items()]

    return my_followers, my_follows


def get_users_accounts():
    media_id = get_media_id()
    for username, vals in user_data.items():
        ck = vals['consumer_key']
        cs = vals['consumer_secret']
        at = vals['access_token']
        ats = vals['access_token_secret']

        auth = tweepy.OAuthHandler(ck, cs)
        auth.set_access_token(at, ats)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        client_id = get_user_id(username)
        followers, follows = get_account_data(api)
        client_dict = {
            'client_id': [client_id],
            'media_id': [media_id],
            'followers': [len(followers)],
            'follows': [len(follows)],
            'follower_users': [json.dumps(followers)],
            'created_on': [datetime.now()]
        }

        client_df = pd.DataFrame(client_dict)
        insert_values(client_df, 'clients_accounts')

    return None


if __name__ == '__main__':
    get_users_accounts()
