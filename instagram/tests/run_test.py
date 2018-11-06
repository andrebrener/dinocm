import os
import sys
import logging
import logging.config

from instapy import InstaPy

from test_user import test_user

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
INSTAGRAM_DIR = TEST_DIR[:TEST_DIR.index('tests')]

sys.path.append(INSTAGRAM_DIR)

from main import get_dino_follows, get_media_id
from functions import (
    follow_users, get_user_id, PROJECT_DIR, take_a_nap, unfollow_haters
)
from user_data import user_data

sys.path.append(PROJECT_DIR)

from config import config

logger = logging.getLogger('main_logger')

LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
os.chdir(LOGS_DIR)


def turn_follow_on(test_user, max_interactions, media_id, follow_for_like):

    for username, vals in user_data.items():
        if username != test_user:
            continue
        logger.info("Following for {}".format(username))
        key = vals['key']
        users_to_copy = vals['users_to_copy']
        min_followers = vals['min_followers']
        max_followers = vals['max_followers']
        min_following = vals['min_following']

        session = InstaPy(
            username=username, password=key, headless_browser=True
        )

        follow_users(
            session, username, users_to_copy, media_id, max_interactions,
            min_followers, min_following, max_followers, follow_for_like
        )

    logger.info("Finished following")

    return None


def turn_unfollow_on(
    test_user, max_interactions, media_id, unfollow_num='dino'
):

    for username, vals in user_data.items():
        if username != test_user:
            continue

        logger.info("Unfollowing for {}".format(username))

        key = vals['key']

        client_id = get_user_id(username)

        session = InstaPy(
            username=username, password=key, headless_browser=True
        )
        if unfollow_num == 'dino':
            unfollow_list = get_dino_follows(client_id, media_id, 'follow')
        else:
            unfollow_list = session.grab_followers(
                username=username,
                amount=unfollow_num,
                live_match=False,
                store_locally=False
            )

        if len(unfollow_list) == 0:
            continue

        unfollow_haters(
            session, username, unfollow_list, media_id, max_interactions
        )

        logger.info("Finished unfollowing")

    return None


def run_test(test_user, max_interactions, cons_runs=4, follow_for_like=False):
    media_id = get_media_id()
    n = 1
    while n <= cons_runs:
        turn_follow_on(test_user, max_interactions, media_id, follow_for_like)
        take_a_nap(3000, 10000)
        n += 1
    turn_unfollow_on(test_user, max_interactions, media_id)
    take_a_nap(3000, 10000)
    run_test(max_interactions)


if __name__ == '__main__':
    logging.config.dictConfig(config['logger'])
    run_test(test_user, 40)
