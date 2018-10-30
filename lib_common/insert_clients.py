from datetime import datetime

import pandas as pd

from db_handle import insert_values


def insert_data():
    data_dict = {}
    for val in [
        'tw_username', 'ig_username', 'phone', 'firstname', 'lastname', 'email'
    ]:
        data_dict[val] = [input("Please input {}: ".format(val))]

    return data_dict


def get_client_values():
    data_dict = insert_data()
    print("\nThese are the values inserted")
    for k, v in data_dict.items():
        print(f'{k}:', v[0])

    values_ok = input("Are these values ok? y/n ")
    if values_ok not in ['y', 'n']:
        values_ok = input("Are these values ok? y/n ")

    if values_ok == 'y':
        data_dict['created_on'] = datetime.now()
        data_df = pd.DataFrame(data_dict)
        insert_values(data_df, 'clients')
        print("Data inserted ok :)")
    else:
        get_client_values()


if __name__ == '__main__':
    get_client_values()
