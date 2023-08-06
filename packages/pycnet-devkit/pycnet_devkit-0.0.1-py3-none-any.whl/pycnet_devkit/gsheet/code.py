import requests
import pandas as pd
from io import StringIO
import os


def download(code,table,key):
    """Download the requested google sheet table. Return as pd.DataFrame.
    
    Args:
        code (str): Identify the google sheet
        table (str): Names of tables, separated by ','
        key (str): Secret key for authentication
    
    Returns:
        pd.DataFrame: The requested google sheet table.
    """
    master_url = os.getenv('GSHEET_URL',None)

    data = {
        'code': code,
        'table': table,
        'elementsep': '<element>',
        'rowsep': '<row>',
        'key': key,
    }

    r = requests.post(master_url, data=data).text

    if '\n' in r:
        r = r.replace('\n','<br>')

    r = r.replace('<row>','\n')
    return pd.read_csv(StringIO(r), sep='<element>', engine='python')

