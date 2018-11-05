import os
import sys
import json
import logging
import logging.config

from datetime import datetime

import pandas as pd

from instapy import InstaPy

from main import get_media_id
from functions import (
    get_account_data, get_user_id, LIB_COMMON_DIR, PROJECT_DIR
)
from user_data import user_data

for p in [LIB_COMMON_DIR, PROJECT_DIR]:
    sys.path.append(p)

from config import config
from db_handle import insert_values

logger = logging.getLogger('main_logger')

LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
os.chdir(LOGS_DIR)


def get_users_accounts():
    media_id = get_media_id()

    for username, vals in user_data.items():
        logger.info("Getting data for {}".format(username))
        key = vals['key']

        session = InstaPy(
            username=username, password=key, headless_browser=True
        )

        client_id = get_user_id(username)
        followers, follows = session.get_follow_count(username)
        import pdb; pdb.set_trace()  # noqa # yapf: disable
        followers, follows = get_account_data(session, username)
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
    logging.config.dictConfig(config['logger'])
    get_users_accounts()
