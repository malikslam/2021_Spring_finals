# <p align ="center">  2021_Spring_finals
## COVID-19 Pandemic: Examining its Impact & Vaccination
## IS 597: Progr Analytics & Data Process (Type II Project)
### <p align ="center">  By Malik Salami

<img width="400" height="400" src = "covid-19img.png" >
![alt text](covid-19img.png)
<p> Data source: https://ourworldindata.org/covid-vaccinations </p>
### Variables Definition:
<ol> COVID-19 General Effect Variables: these are COVID-19 infection indicators that could to led to death. They are 
    'total_cases','new_cases', 'total_deaths','new_deaths'. </ol>
<ol> COVID-19 Preventive Variables: these are COVID-19  protective indicators. They are:
    'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated'.</ol>
<ol> COVID-19 Intensive Variables: these are COVID-19 infection indicators that led to hospital admission. They are: 'icu_patients', 'hosp_patients', 'total_tests', 'new_tests'. </ol>


### Hypotheses:
<ol> H1: There is no significant relationship between COVID-19 Preventive Variables and COVID-19 General Effect Variable.</ol>
<ol> H2: There is no significant relationship between COVID-19 Intensive Variables and COVID-19 General Effect Variable. </ol>

### Interpretation Guide:
<p> A value of ± 1 indicates a perfect degree of association between the two variables. As the correlation coefficient value goes towards 0, the relationship between the two variables will be weaker. The direction of the relationship is indicated by the sign of the coefficient; a + sign indicates a positive relationship and a – sign indicates a negative relationship. </p>

### Preliminary Conclusion:
<p>There are strong indication in the above analysis that COVID-19 Prevention Variables and COVID-19 General Effect Variables are strongly related except for new cases and people_fully_vaccinated that is  0.421675; and new death and people_fully_vaccinated that is 0.365751, that are weakly correlated. Nevertheless, total_vaccinations have been strongly correlated all through.
Therefore, H1 is rejected which says:there is no significant relationship between COVID-19 Preventive Variables and COVID-19 General Effect Variable. </p>

<p>There are strong indication in the above analysis that COVID-19 Intensity Variables and COVID-19 General Effect Variables are strongly related except for new cases and COVID-19 General Effect Variables that are weakly correlated. Nevertheless, total_vaccinations have been strongly correlated all through.
Therefore, H2 is rejected which says:there is no significant relationship between COVID-19 Intensitive Variables and COVID-19 General Effect Variable.</p>