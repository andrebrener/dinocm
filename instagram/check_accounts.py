import os
import sys
import json
import logging
import logging.config

from datetime import datetime
from dino_data import DINO_USER, DINO_PASS

import pandas as pd

from instapy import InstaPy

from main import get_media_id
from functions import LIB_COMMON_DIR, PROJECT_DIR

for p in [LIB_COMMON_DIR, PROJECT_DIR]:
    sys.path.append(p)

from config import config
from db_handle import get_df_from_query, insert_values

logger = logging.getLogger('main_logger')

LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
os.chdir(LOGS_DIR)


def get_all_clients():
    clients = get_df_from_query(
        "select id, ig_username from clients where ig_username is not null"
    )

    return clients


def get_users_accounts():
    media_id = get_media_id()

    session = InstaPy(
        username=DINO_USER, password=DINO_PASS, headless_browser=True
    )

    clients = get_all_clients()
    for row in clients.iterrows():
        vals = row[1]
        username = vals['ig_username']
        client_id = vals['id']

        logger.info("Getting data for {}".format(username))

        followers_count, follows_count = session.get_follow_count(username)
        # followers = session.grab_followers(
        # username=username,
        # amount="full",
        # live_match=False,
        # store_locally=False
        # )

        client_dict = {
            'client_id': [client_id],
            'media_id': [media_id],
            'followers': [followers_count],
            'follows': [follows_count],
            # 'follower_users': [json.dumps(followers)],
            'follower_users': [],
            'created_on': [datetime.now()]
        }
        import pdb; pdb.set_trace()  # noqa # yapf: disable

        client_df = pd.DataFrame(client_dict)
        insert_values(client_df, 'clients_accounts')

    return None


if __name__ == '__main__':
    logging.config.dictConfig(config['logger'])
    get_users_accounts()
