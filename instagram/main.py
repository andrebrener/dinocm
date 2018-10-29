import os
import sys
import logging
import logging.config

from instapy import InstaPy
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
        "select id from media_ids where name = 'instagram'"
    )['id'].loc[0]

    return media_id


def turn_follow_on(max_interactions, media_id):

    for username, vals in user_data.items():
        key = vals['key']
        users_to_copy = vals['users_to_copy']

        session = InstaPy(
            username=username, password=key, headless_browser=True
        )

        # follow users

    logger.info("Finished following")

    return None


def turn_unfollow_on(max_interactions, media_id):

    for username, vals in user_data.items():

        key = vals['key']

        session = InstaPy(
            username=username, password=key, headless_browser=True
        )

        # unfollow users

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
