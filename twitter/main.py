import os
import sys
import logging
import logging.config

import tweepy

from functions import (
    follow_users, LIB_COMMON_DIR, PROJECT_DIR, take_a_nap, unfollow_haters
)
from user_data import user_data

for p in [LIB_COMMON_DIR, PROJECT_DIR]:
    sys.path.append(p)

from config import config
from db_handle import get_df_from_query

logger = logging.getLogger('main_logger')

LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
os.chdir(LOGS_DIR)


def get_media_id():
    media_id = get_df_from_query(
        "select id from media_ids where name = 'twitter'"
    )['id'].loc[0]

    return media_id


def turn_follow_on(max_interactions, media_id):

    for username, vals in user_data.items():
        logger.info("Following for {}".format(username))
        ck = vals['consumer_key']
        cs = vals['consumer_secret']
        at = vals['access_token']
        ats = vals['access_token_secret']
        users_to_copy = vals['users_to_copy']

        auth = tweepy.OAuthHandler(ck, cs)
        auth.set_access_token(at, ats)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        follow_users(api, username, users_to_copy, media_id, max_interactions)

    logger.info("Finished following")

    return None


def turn_unfollow_on(max_interactions, media_id):

    for username, vals in user_data.items():
        logger.info("Unfollowing for {}".format(username))
        ck = vals['consumer_key']
        cs = vals['consumer_secret']
        at = vals['access_token']
        ats = vals['access_token_secret']
        untouchable_users = vals['untouchable users']

        auth = tweepy.OAuthHandler(ck, cs)
        auth.set_access_token(at, ats)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        unfollow_haters(
            api, username, untouchable_users, media_id, max_interactions
        )

    logger.info("Finished unfollowing")

    return None


def main(max_interactions):
    media_id = get_media_id()
    turn_follow_on(max_interactions, media_id)
    take_a_nap(3000, 10000)
    turn_unfollow_on(max_interactions, media_id)
    take_a_nap(3000, 10000)
    main(max_interactions)


if __name__ == '__main__':
    logging.config.dictConfig(config['logger'])
    main(2)
