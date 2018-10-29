import os

from datetime import datetime

from db_handle import db, PROJECT_DIR


def insert_data():
    data_dict = {}
    for val in [
        'tw_username', 'ig_username', 'phone', 'firstname', 'lastname',
        'email', 'tw_password', 'ig_password'
    ]:
        data_dict[val] = input("Please input {}: ".format(val))

    return data_dict


def insert_into_db(data_dict):
    sql_path = os.path.join(PROJECT_DIR, 'sql', 'insert_client_data.sql')
    query = open(sql_path, 'r').read().format(**data_dict)
    db.execute(query)


def get_client_values():
    data_dict = insert_data()
    print("These are the values inserted")
    for k, v in data_dict.items():
        print(f'{k}:', v)

    values_ok = input("Are these values ok? y/n ")
    if values_ok not in ['y', 'n']:
        values_ok = input("Are these values ok? y/n ")

    if values_ok == 'y':
        data_dict['created_on'] = datetime.now()
        insert_into_db(data_dict)
        print("Data inserted ok :)")
    else:
        get_client_values()


if __name__ == '__main__':
    get_client_values()
