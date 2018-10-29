import os
import sys
import logging
import logging.config

from time import sleep
from random import randint, sample
from datetime import datetime

import tweepy
import pandas as pd

TWITTER_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = TWITTER_DIR[:TWITTER_DIR.index('twitter')]
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
        f"select id from clients where tw_username= '{username}'"
    )['id'].loc[0]

    return user_id


def get_interaction_id(interaction):
    int_id = get_df_from_query(
        f"select id from interaction_ids where name = '{interaction}'"
    )['id'].loc[0]

    return int_id


def take_a_nap(min_time=1, max_time=7):
    wait = randint(min_time, max_time)
    sleep(wait)


def like_tweets(api, username, kws, likes_per_kw, media_id, max_interactions):
    user_id = get_user_id(username)
    int_id = get_interaction_id('like')
    n = 1
    random_kws = list(sample(kws, len(kws)))
    for kw in random_kws:
        search = kw
        for tweet in tweepy.Cursor(api.search, search).items(likes_per_kw):
            if n > max_interactions:
                return None
            try:
                tweet.favorite()
                tweet_dict = {
                    'client_id': [user_id],
                    'content_id': [tweet.id],
                    'content_text': [tweet.text],
                    'username': [tweet.user.screen_name],
                    'user_followers': [tweet.user.followers_count],
                    'user_follows': [tweet.user.friends_count],
                    'likes_in_content': [tweet.favorite_count],
                    'created_on': [datetime.now()],
                    'interaction_id': [int_id],
                    'kw_searched': [kw],
                    'user_location': [tweet.user.location],
                    'media_id': [media_id]
                }
                tweet_df = pd.DataFrame(tweet_dict)
                insert_values(tweet_df, 'interactions')
                n += 1

                take_a_nap()
            except tweepy.TweepError as e:
                logger.info(e)
            except StopIteration:
                break

    return None


def remove_favs(api, username, media_id, max_interactions):
    user_id = get_user_id(username)
    int_id = get_interaction_id('unlike')
    n = 1
    for tweet in tweepy.Cursor(api.favorites).items():
        if n > max_interactions:
            return None

        api.destroy_favorite(tweet.id)

        tweet_dict = {
            'client_id': [user_id],
            'content_id': [tweet.id],
            'content': [tweet.text],
            'user_name': [tweet.user.screen_name],
            'user_followers': [tweet.user.followers_count],
            'user_follows': [tweet.user.friends_count],
            'likes_in_content': [tweet.favorite_count],
            'created_on': [datetime.now()],
            'interaction_id': [int_id],
            'user_location': [tweet.user.location],
            'media_id': [media_id]
        }
        tweet_df = pd.DataFrame(tweet_dict)
        insert_values(tweet_df, 'interactions')
        n += 1

        take_a_nap()

    return None


def follow_users(
    api, username, users, media_id, max_interactions, not_follow_users=[]
):

    user_id = get_user_id(username)
    int_id = get_interaction_id('follow')
    my_followers = [
        x.screen_name for x in tweepy.Cursor(api.followers).items()
    ]

    my_follows = [x.screen_name for x in tweepy.Cursor(api.friends).items()]

    total_not_follow = not_follow_users + my_followers + my_follows

    unique_not_follow = set(total_not_follow)

    n = 1
    for u in sample(users, len(users)):
        followers = tweepy.Cursor(api.followers, screen_name=u).items()

        followers_list = list(followers)
        for f in sample(followers_list, len(followers_list)):
            if n > max_interactions:
                return None

            if f.screen_name not in unique_not_follow:
                try:
                    f.follow()

                    f_dict = {
                        'client_id': [user_id],
                        'id': [f.id],
                        'username': [f.screen_name],
                        'user_followers': [f.followers_count],
                        'user_follows': [f.friends_count],
                        'created_on': [datetime.now()],
                        'interaction_id': [int_id],
                        'user_to_follow': [u],
                        'user_location': [f.location],
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
    api, username, untouchable_users, media_id, max_interactions
):
    user_id = get_user_id(username)
    int_id = get_interaction_id('unfollow')

    n = 1
    for f in tweepy.Cursor(api.friends).items():
        if n > max_interactions:
            return None
        if f.screen_name not in untouchable_users:
            try:
                api.destroy_friendship(f.screen_name)
                f_dict = {
                    'client_id': [user_id],
                    'content_id': [f.id],
                    'username': [f.screen_name],
                    'user_followers': [f.followers_count],
                    'user_follows': [f.friends_count],
                    'created_on': [datetime.now()],
                    'interaction_id': [int_id],
                    'user_location': [f.location],
                    'media_id': [media_id]
                }

                follow_df = pd.DataFrame(f_dict)
                insert_values(follow_df, 'interactions')
                n += 1
                take_a_nap()
            except Exception as e:
                logger.info(e)

    return None
