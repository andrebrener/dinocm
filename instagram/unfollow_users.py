import os
import sys
import logging
import logging.config

from instapy import InstaPy

from functions import (
    get_user_id, LIB_COMMON_DIR, PROJECT_DIR, take_a_nap, unfollow_haters
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


def get_dino_follows(client_id, media_id, int_name):
    followers = get_df_from_query(
        """select username
           from interactions
           where client_id = {cl_id}
           and media_id= {m_id}
           and interaction_id in
           (
            select id
            from interaction_ids where name = '{int_name}'
           )
           """.format(cl_id=client_id, m_id=media_id, int_name=int_name)
    )['username'].tolist()

    return followers


def turn_unfollow_on(max_interactions, media_id, unfollow_num='dino'):

    for username, vals in user_data.items():
        is_test = vals['is_test']
        # if is_test:
        # continue
        if username != 'nicobarii':
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


def unfollow_dino_users(max_interactions):
    media_id = get_media_id()
    turn_unfollow_on(max_interactions, media_id)
    take_a_nap(3000, 10000)


if __name__ == '__main__':
    logging.config.dictConfig(config['logger'])
    unfollow_dino_users(100)
