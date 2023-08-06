"""
This module contains various utilities shared across most of the other
*chainladder* modules.

"""
import pandas as pd
import numpy as np
import joblib
import os
from chainladder.core.triangle import Triangle


def load_dataset(key):
    """ Function to load datasets included in the chainladder package.

        Arguments:
        key: str
        The name of the dataset, e.g. RAA, ABC, UKMotor, GenIns, etc.

        Returns:
    	pandas.DataFrame of the loaded dataset.

   """
    path = os.path.dirname(os.path.abspath(__file__))
    origin = 'origin'
    development = 'development'
    columns = ['values']
    index = None
    if key.lower() in ['mcl', 'usaa', 'quarterly', 'auto', 'usauto']:
        columns = ['incurred', 'paid']
    if key.lower() == 'clrd':
        origin = 'AccidentYear'
        development = 'DevelopmentYear'
        index = ['GRNAME', 'LOB']
        columns = ['IncurLoss', 'CumPaidLoss', 'BulkLoss', 'EarnedPremDIR',
                   'EarnedPremCeded', 'EarnedPremNet']
    if key.lower() in ['liab', 'auto']:
        index = ['lob']
    if key.lower() in ['cc_sample', 'ia_sample']:
        columns = ['loss', 'exposure']
    df = pd.read_csv(os.path.join(path, 'data', key.lower() + '.csv'))
    return Triangle(df, origin=origin, development=development,
                    columns=columns, index=index)


def read_pickle(path):
    return joblib.load(path)


def parallelogram_olf(values, date, start_date=None, end_date=None,
                      grain='M', vertical_line=False):
    """ Parallelogram approach to on-leveling.  Need to fix return grain
    """
    date = pd.to_datetime(date)
    if not start_date:
        start_date = '{}-01-01'.format(date.min().year-1)
    if not end_date:
        end_date = '{}-12-31'.format(date.max().year+1)
    date_idx = pd.date_range(start_date, end_date)
    y = pd.Series(np.array(values), np.array(date))
    y = y.reindex(date_idx, fill_value=0)
    idx = np.cumprod(y.values+1)
    idx = idx[-1]/idx
    y = pd.Series(idx, y.index)
    if not vertical_line:
        y = y.to_frame().rolling(365).mean()
    y = y.groupby(y.index.to_period(grain)).mean().reset_index()
    y.columns = ['Origin', 'OLF']
    y['Origin'] = y['Origin'].astype(str)
    return y.set_index('Origin')
