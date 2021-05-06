"""
COVID-19 Pandemic: Examining Relationship Between Its Various Factors
========================================================================================================
* Factors:                                                                                             *
* COVID-19 General Effect Variables: 'total_cases','new_cases', 'total_deaths','new_deaths'.           *
* COVID-19 Preventive Variables: 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated'. *
* COVID-19 Intensive Variables: 'icu_patients', 'hosp_patients', 'total_tests', 'new_tests'.           *
========================================================================================================
By Malik Salami
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
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
#%matplotlib inline

def load_data(filename, col: list) -> pd.DataFrame:
    """
    Load full data and filter the columns of interest into dataframe
    :param filename:  loads dataframe of countries' records
    :param col: columns of interest that are needed
    :return: a dataFrame of records after filtering the columns

    >>> xcol = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']
    >>> data = pd.read_csv('owid-covid-data.csv')
    >>> data = data.filter(items =xcol)
    >>> data.iloc[2000]['total_cases']
    8192.0

    >>> len(data)
    82838

    """
    col = ['iso_code', 'continent', 'location', 'date']+col
    data = pd.read_csv(filename)
    out_file = data.filter(items =col)
    return out_file

def get_last_row(df:  pd.DataFrame) -> pd.DataFrame:
    """
    Read the record on the last row for each country
    :param df: loads dataframe of countries' records
    :return: a dataframe of last row records for each country if the date postdate 2021,3,31

    >>> gen_effect_var = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']
    >>> intensive_var = ['icu_patients', 'hosp_patients', 'total_tests', 'new_tests']
    >>> preventive_var = ['total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']
    >>> data = load_data('owid-covid-data.csv', gen_effect_var+preventive_var )
    >>> data.dropna(inplace = True)
    >>> data['date']= pd.to_datetime(data['date'],format='%Y/%m/%d')
    >>> x = data.groupby(['location']).last().reset_index()
    >>> res = x[x['date'] >  pd.Timestamp(2021,3,31)]
    >>> res.iloc[0]['continent']
    'Europe'

    >>> res.iloc[5]['date']
    Timestamp('2021-04-18 00:00:00')

    >>> len(res)
    90
    """
    df.dropna(inplace = True)
    df['date']= pd.to_datetime(df['date'],format='%Y/%m/%d')
    result = df.groupby(['location']).last().reset_index()
    result = result[result['date'] >  pd.Timestamp(2021,3,31)]
    return result

def analyze_1(df:  pd.DataFrame):
    """
    Analyzes DataFrame to find the correlation and display in table and heatmap
    :param df: loads dataframe of countries' records
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


def check_var_inf_fact(df: pd.DataFrame,  drop_var:list):
    """

    It checks Variance Inflation Factor (VIF) of independents variables to ascertain right variables are  chosen.
    It prints the VIF result before and after dropping the highly correlated variables.
    :param df: loads dataframe of countries' records
    :param drop_var: remove columns/variables that are highly correlated
    """
    independent_var_before = df
    independent_var_after = df.drop(drop_var, axis=1)

    # the VFI does expect a constant term in the data, so we need to add one using the add_constant method
    X1 = sm.tools.add_constant(independent_var_before)
    X2 = sm.tools.add_constant(independent_var_after)

    # create the series for both
    series_before = pd.Series([variance_inflation_factor(X1.values, i) for i in range(X1.shape[1])], index=X1.columns)
    series_after = pd.Series([variance_inflation_factor(X2.values, i) for i in range(X2.shape[1])], index=X2.columns)

    # display the series
    print('DATA BEFORE')
    print('-'*100)
    display(series_before)

    print('DATA AFTER')
    print('-'*100)
    display(series_after)

    pd.plotting.scatter_matrix(independent_var_after, alpha=1, figsize=(7, 5))
    # show the plot
    plt.show()


def create_OLS_Model(dep_var: str, ind_var: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    """

    :param dep_var:
    :param ind_var:
    :return:
    >>> gen_effect_var = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']
    >>> intensive_var = ['icu_patients', 'hosp_patients', 'total_tests', 'new_tests']
    >>> preventive_var = ['total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']
    >>> data = load_data('owid-covid-data.csv', gen_effect_var+preventive_var )
    >>> data.dropna(inplace = True)
    >>> data['date']= pd.to_datetime(data['date'],format='%Y/%m/%d')
    >>> x = data.groupby(['location']).last().reset_index()
    >>> res = x[x['date'] >  pd.Timestamp(2021,3,31)]
    >>> dv = res[res.columns[4:8]]
    >>> iv = res[res.columns[8:]]
    >>> X = sm.add_constant(iv)
    >>> y = sm.OLS(dv, X).fit()
    >>> type(y)
    <class 'statsmodels.regression.linear_model.RegressionResultsWrapper'>
    """
    X2 = ind_var  # X is the input variables (or independent variables)
    y2 = dep_var  # is the output/dependent variable
    X2 = sm.add_constant(X2)  # Adding an intercept (beta_0) to the model

    # create a OLS model 'sm.OLS(y2, X2)' and fit the data '.fit()'
    model_ind_var = sm.OLS(y2, X2).fit()  ## sm.OLS(output, input)

    return model_ind_var

if __name__ == '__main__':
    gen_effect_var = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']
    intensive_var = ['icu_patients', 'hosp_patients', 'total_tests', 'new_tests']
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
    used_data2 = load_data('owid-covid-data.csv', gen_effect_var + intensive_var)
    display(used_data2.head())
    data4analysis2 = get_last_row(used_data2)

    #printing out result of the analysis for Hypothesis two
    #analyze_1(data4analysis2)