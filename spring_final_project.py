"""

"""
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
from IPython.display import display

import statsmodels.api as sm
from statsmodels.stats import diagnostic as diag
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
#%matplotlib inline

def load_data(filename: str, col: list) -> pd.DataFrame:
    """
    """
    col = ['iso_code', 'continent', 'location', 'date']+col
    data = pd.read_csv(filename)
    out_file = data.filter(items =col)
    return out_file

def get_last_row(df:  pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """
    df.dropna(inplace = True)
    df['date']= pd.to_datetime(df['date'],format='%Y/%m/%d')
    result = df.groupby(['location']).last().reset_index()
    result = result[result['date'] >  pd.Timestamp(2021,3,31)]
    return result

def analyze_1(df:  pd.DataFrame):
    """

    :param df:
    :return:
    """
    display(df.describe())
    pearsoncorr = df.corr(method='pearson')
    ht_map = sns.heatmap(pearsoncorr,
    xticklabels=pearsoncorr.columns,
    yticklabels=pearsoncorr.columns,
    cmap='RdBu_r',
    annot=True,
    linewidth=0.5)
    plt.show()
    display(pearsoncorr)


if __name__ == '__main__':
    gen_effect_var = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']
    intensity_var = ['icu_patients', 'hosp_patients', 'total_tests', 'new_tests']
    preventive_var = ['total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']

    print("************ Hypothesis One Analysis ************")
    used_data = load_data('owid-covid-data.csv', gen_effect_var + preventive_var)
    display(used_data.head())
    data4analysis = get_last_row(used_data)

    # printing out result of the analysis for Hypothesis one
    #analyze_1(data4analysis)

    print("""
    Interpretation Guide:
    A large positive value (near to 1.0) indicates a strong positive correlation, i.e., 
    if the value of one of the variables increases, the value of the other variable increases as well. 
    A negative value 1.0 indicates a strong negative correlation and a value near to 0 (both positive or negative) 
    indicates the absence of any correlation between the two variables.
    """)

    print("************ Hypothesis Two Analysis ************")
    used_data2 = load_data('owid-covid-data.csv', gen_effect_var + intensity_var)
    display(used_data2.head())
    data4analysis2 = get_last_row(used_data2)

    #printing out result of the analysis for Hypothesis two
    #analyze_1(data4analysis2)