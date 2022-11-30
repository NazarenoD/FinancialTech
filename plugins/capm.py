import pandas as pd
import numpy as np
#pip install pandas-datareader
from pandas_datareader import data
from typing import List

def rate(df):
    dfr = pd.DataFrame()
    for i in df.columns.values:
        dfr[f"{i}"] = df[f"{i}"] / df[f"{i}"].shift(1) - 1
    return dfr


def get_df(tikets:List[str],date:str)->dict:
    df = pd.DataFrame()
    invalid_tikets = []
    for i in tikets:
        try:
            df[f'{i}'] = data.DataReader(i,'yahoo',date)['Close']
        except:
            invalid_tikets.append(i)
    return {'dfr':rate(df),'df':df,'invalid_tikets':invalid_tikets}

def VM (R,dfr):
    vm_matrix=2*dfr.cov()
    vm_matrix["E(R)"]=dfr.mean()
    vm_matrix["w"]=1
    vm_matrix.loc[-2]=dfr.mean()
    vm_matrix.loc[-1]=1
    vm_matrix["w"][-2]=0
    vm_matrix["w"][-1]=0
    vm_matrix['E(R)'][-2]=0
    vm_matrix['E(R)'][-1]=0
    vm_matrix.rename(index={-2:'E(R)',-1:'w'}, inplace=True)
    vm_matrix_inv = pd.DataFrame(np.linalg.inv(vm_matrix.values), vm_matrix.columns, vm_matrix.index)
    vm_matrix_inv["w*"]=vm_matrix_inv["E(R)"]*(((1+R)**(1/252)-1))+vm_matrix_inv["w"]
    weight=vm_matrix_inv["w*"][:-2]
    return weight.to_dict()