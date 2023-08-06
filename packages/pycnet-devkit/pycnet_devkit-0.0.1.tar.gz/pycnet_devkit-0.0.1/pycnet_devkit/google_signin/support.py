from .. import mysql

def pycnet_permission(email):
    pyccode = email.split('@')[0]
    df= mysql.query(f"select pyccode,permission from usertbl where pyccode = '{pyccode}'")
    if 'permission' not in df.columns:
        return None
    s = df['permission'][0]
    return s.split('-')[1]


