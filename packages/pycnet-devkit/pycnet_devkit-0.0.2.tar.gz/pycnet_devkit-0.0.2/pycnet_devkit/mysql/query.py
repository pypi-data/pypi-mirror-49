import requests
import xml.etree.ElementTree as et
import pandas as pd
from collections import OrderedDict
import os

def query(sql):
    """Query the database.
    """
    token = os.getenv('PYCNET_MYSQL_TOKEN',None)
    url = os.getenv('PYCNET_MYSQL_URL',None)

    if token is None:
        raise Exception('Please add PYCNET_MYSQL_TOKEN to env first!')
    if url is None:
        raise Exception('Please add PYCNET_MYSQL_URL to env first!')

    token = 'Bearer ' + token
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    data = {'query': sql}
    response = requests.post(url, json=data, headers=headers).text

    try:
        xroot = et.fromstring(response)

        all_rows = []
        for _, item in enumerate(xroot):
            row = OrderedDict()
            for element in item:
                row[element.tag] = element.text
            all_rows.append(row)
        df = pd.DataFrame(all_rows)
        df = df.apply(pd.to_numeric, errors='ignore')
        return df

    except:
        raise Exception('''
        There is an error when parsing response from pycnet.
        Error msg:
        ''' + response)
