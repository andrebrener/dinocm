import os

import pandas as pd

from db_data import DB_HOST, DB_NAME, DB_USERNAME
from dbconnectors import PostgreSqlDb

LC_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = LC_DIR[:LC_DIR.index('lib_common')]

db = PostgreSqlDb(username=DB_USERNAME, host=DB_HOST, database=DB_NAME)


def create_tables(tables):
    sql_path = os.path.join(PROJECT_DIR, 'sql', '{}.sql')
    for t in tables:
        query = open(sql_path.format(t), 'r').read()
        db.execute('DROP TABLE IF EXISTS {} CASCADE'.format(t))
        db.execute(query)


def insert_values(df, t):

    db.insert_from_frame(df, t)

    return None


def get_df_from_query(query):
    df = db.get_pandas_df(query)
    return df


def build_db():
    start_from_zero = input(
        "This will restart the whole db. Are you sure you want to run it? Insert y or n: "
    )
    if start_from_zero == 'y':
        create_tables(
            [
                'clients', 'media_ids', 'interaction_ids', 'clients_accounts',
                'interactions'
            ]
        )
        for t in ['media_ids', 'interaction_ids']:
            file_path = os.path.join(PROJECT_DIR, 'csvs', '{}.csv'.format(t))
            df = pd.read_csv(file_path)

            insert_values(df, t)


if __name__ == '__main__':

    build_db()

    # import pdb; pdb.set_trace()  # noqa # yapf: disable
