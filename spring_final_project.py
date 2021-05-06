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
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.linear_model import LinearRegression


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

    # load data for General Effect Variables & Preventive Variables
    used_data = load_data('owid-covid-data.csv', gen_effect_var + preventive_var)
    display(used_data.head())

    # Get the latest record for each countries
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

    # load data for General Effect Variables & Intensive Variables
    used_data2 = load_data('owid-covid-data.csv', gen_effect_var + intensive_var)
    display(used_data2.head())

    # Get the latest record for each countries
    data4analysis2 = get_last_row(used_data2)

    #printing out result of the analysis for Hypothesis two
    #analyze_1(data4analysis2)

    """
    Taking the Analysis Further (Multiple/Mutivariate Regression Model):
    The Multiple Regression Analysis will  explain the relationship between the COVID-19 General Effect 
    Variables, and both of COVID-19 Intensive Variables and COVID-19 Preventive Variables.
    
        Factors to Consider in Multiple Regression Model:
    - Absence of Multicollinearity in the Model
    - Check for the normality of the residuals
    - Checking the Mean of the Residuals Equals 0
    """
    used_data_ = load_data('owid-covid-data.csv', gen_effect_var + intensive_var + preventive_var)
    used_data3 = get_last_row(used_data_)
    dependent_var = used_data3[used_data3.columns[4:8]]
    independent_var = used_data3[used_data3.columns[8:]]

    # Factor I: Testing multicollinearity
    analyze_1(independent_var)

    """
    Variance Inflation Factor (VIF): 
    VIF is a measure of how much a particular variable is contributing to the standard error in the regression model. 
    When significant multicollinearity exists, the variance inflation factor will be huge for the variables in the calculation.
    From the correlation table and the heat map 'icu_patients','total_tests','people_fully_vaccinated', 'people_vaccinated'
    are highly correlated some other explanatory variable e.g. 'icu_patients' and 'hosp_patients' are highly correlated, 
    so to avoid duplicate 'icu_patients' is pulled out a,ong with others
    """

    # Calling variance_inflation_factor - check_var_inf_fact to check if we pulling down the right variables.
    drop_var = ['icu_patients', 'total_tests', 'people_fully_vaccinated', 'people_vaccinated']
    check_var_inf_fact(independent_var, drop_var)

    """
    Data show that After Variance_Inflation_Factor we retaining only 
    ['hosp_patients', 'news_test', 'total_vaccinations']. I am reloading the data to expand the coverage.
    """

    remain_var = ['hosp_patients', 'new_tests', 'total_vaccinations']
    dependent_var2_ = list(dependent_var.columns[0:])
    used_data4 = load_data('owid-covid-data.csv', dependent_var2_ + remain_var)
    used_data4 = get_last_row(used_data4)

    print('size of the data before dropping multicollineared variables:', used_data3.shape)
    print('size of the data after dropping multicollineared variables:', used_data4.shape)
    dependent_var2 = used_data4[used_data4.columns[4:8]]
    independent_var2 = used_data4[used_data4.columns[8:]]

    # Recheck the Multicollinearity
    analyze_1(independent_var2)

    """
    Building Multiple Regression Model
    Statsmodel module was used to create Model for each instance of the dependent variables 
    (General Effect Variables) with the other remaining independent variables (hosp_patients, new_tests, total_vaccinations).
    """
    dep_var = list(dependent_var2.columns)
    store_model = []
    for items in dep_var:
        print('OLS Regression Model Results for ', items)
        model_OLS = create_OLS_Model(dependent_var2[items], independent_var2)
        store_model.append(model_OLS)
        display(model_OLS.summary())

    """
    Factor II: Checking for the Normality of the Residuals
    Checking if residuals are normally distributed i.e. check how the data hugs around the line
    Factor III: Checking the Mean of the Residuals Equals 0
    """

    for items in range(len(dep_var)):
        print("The normality of the residual & The mean of the residuals for ", dep_var[items])
        sm.qqplot(store_model[items].resid, line='s')
        plt.show()
        # check that the mean of the residuals is approx. 0.
        mean_residuals = sum(store_model[items].resid) / len(store_model[items].resid)
        print("The mean of the residuals is {:.4}".format(mean_residuals))