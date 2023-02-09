import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error


def cleaning(x):
    pattern = re.compile(r'\s+')
    x = re.sub(pattern,'',x)
    x = x.replace('[','').replace(']','').replace('}','').replace('{','').replace('-','')    
    return x

def fixName(x):
    x = x.lower().title()
    x = x.replace('á','a')
    return x

def limits(col):
    q1 = col.quantile(0.25)
    q3 = col.quantile(0.75)
    amplitude = q3-q1
    return q1 - 1.5 * amplitude, q3 + 1.5 * amplitude

def del_outliers(df, col_name):
    n_rows = df.shape[0]
    lim_inf, lim_sup = limits(df[col_name])
    df = df.loc[(df[col_name] >= lim_inf) & (df[col_name] <= lim_sup), :]
    removed_rows = n_rows - df.shape[0]
    return df, removed_rows

def box_diagram(col):    
    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.set_size_inches(15,5)
    sns.boxplot(x=col, ax=ax1)
    ax2.set_xlim(limits(col))
    sns.boxplot(x=col, ax=ax2)
    
def histogram(col):
    plt.figure(figsize=(15,5))
    sns.distplot(col,hist=True)
    
def bar_chart(col):
    plt.figure(figsize=(15,5))
    ax = sns.barplot(x=col.value_counts().index, y=col.value_counts())
    ax.set_xlim(limits(col))
    
def evaluate_model(model_name, y_test, predict):
    r2 = r2_score(y_test, predict)
    RSME = np.sqrt(mean_squared_error(y_test, predict))
    return f'\nModel {model_name}:\nR²:{r2:.2%}\nRSME:{RSME:.2f}'