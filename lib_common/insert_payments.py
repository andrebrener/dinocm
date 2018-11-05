from datetime import date, datetime

import pandas as pd

from db_handle import get_df_from_query, insert_values


def get_user_id(username):
    user_id = get_df_from_query(
        "select id from clients where ig_username= '{}'".format(username)
    )['id'].loc[0]

    return user_id


def check_in_values(d, val, val_list):
    if val in val_list:
        return val
    else:
        val = input("Please input {}: ".format(d))
        return check_in_values(d, val, val_list)


def insert_data():
    data_dict = {}
    for d in [
        'ig_username', 'amount', 'date (dd-mm-yy)',
        'method (mp, mp susc, cash, pp, btc)'
    ]:
        inp = input("Please input {}: ".format(d))
        key = d
        if d == 'ig_username':
            key = 'client_id'
            inp = get_user_id(inp)
        if 'date' in d:
            key = 'date'
            if inp == '':
                inp = date.today()
            else:
                inp = datetime.strptime(inp, '%d-%m-%Y')

        if 'method' in d:
            inp = check_in_values(
                d, inp, ['mp', 'mp susc', 'cash', 'pp', 'btc']
            )

        data_dict[key] = [inp]

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
