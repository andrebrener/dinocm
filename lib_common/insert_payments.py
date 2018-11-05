from datetime import date, datetime

import pandas as pd

from db_handle import get_df_from_query, insert_values


def get_user_id(username):
    user_id = get_df_from_query(
        "select id from clients where ig_username= '{}'".format(username)
    )['id'].loc[0]

    return user_id


def insert_data():
    data_dict = {}
    for val in ['ig_username', 'amount', 'date']:
        key = val
        if val == 'ig_username':
            key = get_user_id(val)
        data_dict[key] = [input("Please input {}: ".format(val))]

    if data_dict['date'] == '':
        data_dict['date'] = date.today()

    return data_dict


def get_payments():
    data_dict = insert_data()
    print("\nThese are the values inserted")
    for k, v in data_dict.items():
        print('{}:'.format(k), v[0])

    values_ok = input("Are these values ok? y/n ")
    if values_ok not in ['y', 'n']:
        values_ok = input("Are these values ok? y/n ")

    if values_ok == 'y':
        data_dict['created_on'] = datetime.now()
        data_df = pd.DataFrame(data_dict)
        insert_values(data_df, 'payments')
        print("Data inserted ok :)")
    else:
        get_payments()


if __name__ == '__main__':
    get_payments()
