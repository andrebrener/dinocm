import os
import sys
import logging
import logging.config

from time import sleep
from random import randint, sample
from datetime import datetime

import pandas as pd

from instapy import InstaPy
from instapy.util import smart_run

from user_data import user_data

INSTAGRAM_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = INSTAGRAM_DIR[:INSTAGRAM_DIR.index('instagram')]
LIB_COMMON_DIR = os.path.join(PROJECT_DIR, 'lib_common')

for p in [LIB_COMMON_DIR, PROJECT_DIR]:
    sys.path.append(p)

from db_handle import get_df_from_query, insert_values

logger = logging.getLogger('main_logger')

LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
os.chdir(LOGS_DIR)


def get_user_id(username):
    user_id = get_df_from_query(
        "select id from clients where ig_username= '{}'".format(username)
    )['id'].loc[0]

    return user_id


def get_interaction_id(interaction):
    int_id = get_df_from_query(
        "select id from interaction_ids where name = '{}'".format(interaction)
    )['id'].loc[0]

    return int_id


def take_a_nap(min_time=1, max_time=7):
    wait = randint(min_time, max_time)
    sleep(wait)


def get_account_data(session, user):
    with smart_run(session):
        my_followers = session.grab_followers(
            username=user,
            amount="full",
            live_match=False,
            store_locally=False
        )
        my_follows = session.grab_following(
            username=user,
            amount="full",
            live_match=False,
            store_locally=False
        )

        return my_followers, my_follows


def follow_users(
    session,
    username,
    users,
    media_id,
    max_interactions,
    min_followers,
    min_following,
    follow_for_like,
    not_follow_users=[]
):

    user_id = get_user_id(username)
    int_id = get_interaction_id('follow')

    my_followers, my_follows = get_account_data(session, username)

    total_not_follow = not_follow_users + my_followers + my_follows

    unique_not_follow = set(total_not_follow)

    n = 1
    for u in sample(users, len(users)):

        new_session = InstaPy(
            username=username,
            password=user_data[username]['key'],
            headless_browser=True
        )

        with smart_run(new_session):

            followers = new_session.grab_followers(
                username=u,
                amount="full",
                live_match=False,
                store_locally=False
            )
            new_session.set_relationship_bounds(
                enabled=True,
                delimit_by_numbers=True,
                min_followers=0,
                min_following=0
            )

            new_session.set_do_follow(enabled=True, times=1)

            for f in sample(followers, len(followers)):
                if n > max_interactions:
                    return None

                if f not in unique_not_follow:
                    try:
                        user_followers = new_session.grab_followers(
                            username=f,
                            amount="full",
                            live_match=False,
                            store_locally=False
                        )
                        user_follows = new_session.grab_following(
                            username=f,
                            amount="full",
                            live_match=False,
                            store_locally=False
                        )

                        if not (
                            len(user_followers) >= min_following
                            and len(user_follows) >= min_following
                        ):
                            continue

                        if follow_for_like:
                            new_session.follow_likers(
                                [f],
                                photos_grab_amount=3,
                                follow_likers_per_photo=25,
                                randomize=True
                            )
                        else:
                            new_session.follow_by_list(followlist=[f])

                        f_dict = {
                            'client_id': [user_id],
                            'username': [f],
                            'user_followers': [len(user_followers)],
                            'user_follows': [len(user_follows)],
                            'created_on': [datetime.now()],
                            'interaction_id': [int_id],
                            'user_to_follow': [u],
                            'media_id': [media_id]
                        }
                        follow_df = pd.DataFrame(f_dict)
                        insert_values(follow_df, 'interactions')
                        n += 1

                        take_a_nap()
                    except Exception as e:
                        logger.info(e)
                        continue

    return None


def unfollow_haters(
    session, username, untouchable_users, media_id, max_interactions
):
    user_id = get_user_id(username)
    int_id = get_interaction_id('unfollow')

    n = 1

    with smart_run(session):
        my_follows = session.grab_following(
            username=username,
            amount="full",
            live_match=False,
            store_locally=False
        )
        for f in my_follows:
            if n > max_interactions:
                return None
            if f not in untouchable_users:
                try:
                    session.unfollow_users(customList=(True, [f], "all"))
                    user_followers, user_follows = get_account_data(session, f)

                    f_dict = {
                        'client_id': [user_id],
                        'content_id': [f.id],
                        'username': [f],
                        'user_followers': [len(user_followers)],
                        'user_follows': [len(user_follows)],
                        'created_on': [datetime.now()],
                        'interaction_id': [int_id],
                        'media_id': [media_id]
                    }

                    follow_df = pd.DataFrame(f_dict)
                    insert_values(follow_df, 'interactions')
                    n += 1
                    take_a_nap()
                except Exception as e:
                    logger.info(e)

    return None
