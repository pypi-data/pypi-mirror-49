import pandas as pd

def senior():
    """list of senior subjs.
    """
    return ['CHIN', 'ENG', 'MATH', 'M1', 'M2', 'LIBS', 'CHIS', 'HIST', 'CLIT', 'GEOG', 'ECON', 'BAFS', 'TH', 'PHY', 'CHEM', 'BIO', 'ICT',  'VA']


def exam():
    """list of all exam subjs. 
    """
    return ['CHIN', 'ENG', 'MATH', 'M1', 'M2', 'LIBS', 'CHIS', 'HIST', 'CLIT', 'GEOG', 'ECON', 'BAFS', 'TH', 'IS', 'PHY', 'CHEM', 'BIO', 'ICT', 'VA', 'PTH', 'OMF']


def categorize(df,main_subjs,keep=False):
    def _subj_col(df):
        if 'subj' in df.columns:
            return 'subj'
        elif 'subject' in df.columns:
            return 'subject'
        else:
            raise Exception('subject column not found!')
    df = df.copy()
    s = _subj_col(df)
    ls = main_subjs
    if keep:
        ls += [subj for subj in df[s].unique() if subj not in main_subjs]
    df[s] = pd.Categorical(df[s],ls)
    return df

def reindex_columns(df,main_subjs,keep=False):
    df = df.copy()
    ls = main_subjs
    if keep:
        ls += [subj for subj in df.columns if subj not in main_subjs]
    return df.reindex(columns=ls)

    