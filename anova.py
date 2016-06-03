# Hypothesis Testing and ANOVA  
# week1 assignment for Data Analysis Tools

"""
Created on Fri Jun 03 12:10:06 2016

@author: taehee jeong
"""

# import libraries
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi 


#%% Load data
path='C:/Bigdata/Data Analysis and Interpretation/Dataset/GapMinder/'
data = pd.read_csv(path+'gapminder.csv', low_memory=False)

print data.columns

#setting variables you will be working with to numeric
data['lifeexpectancy'] = data['lifeexpectancy'].convert_objects(convert_numeric=True)
data['urbanrate'] = data['urbanrate'].convert_objects(convert_numeric=True)
data['alcconsumption'] = data['alcconsumption'].convert_objects(convert_numeric=True)

data1=data.copy()


#%% Model Interpretation for ANOVA:
# 2 Categorical explanatory variable vs Quantitative response variable

data1.urbanrate.describe()

# categorize quantitative variable based on customized splits using cut function
# splits into 3 groups (12-15, 16-18, 18-22) 
data1['urbangroup'] = pd.cut(data1.urbanrate, [0, 50,100], labels=["rural","city"] )

#crosstabs evaluating which urban rate into which urbangroup
print (pd.crosstab(data1['urbangroup'], data1['urbanrate']))
print data1['urbangroup']
print(data1['urbangroup'].value_counts(sort=False, dropna=True))

# using ols function for calculating the F-statistic and associated p value
model1 = smf.ols(formula='lifeexpectancy ~ C(urbangroup)', data=data1)
results1 = model1.fit()
print (results1.summary())

sub1 = data1[['lifeexpectancy', 'urbangroup']].dropna()

print ('means for lifeexpectancy by urban status')
m1= sub1.groupby('urbangroup').mean()
print (m1)

print ('standard deviations for lifeexpectancy by urban status')
sd1 = sub1.groupby('urbangroup').std()
print (sd1)

#%%Model Interpretation for ANOVA:
# more than 2 Categorical explanatory variable vs Quantitative response variable

data1.alcconsumption.describe()

# quartile split (use qcut function & ask for 4 groups - gives quartile split)
print 'alcohol consumption : 4 categories - quartiles'
data1['alcgroup']=pd.qcut(data1.alcconsumption, 4, labels=["1=0%tile","2=25%tile","3=50%tile","4=75%tile"])

#crosstabs evaluating which alcohol consumption into which alcgroup
print (pd.crosstab(data1['alcgroup'], data1['alcconsumption']))
print data1['alcgroup']
print(data1['alcgroup'].value_counts(sort=False, dropna=True))

sub2 = data1[['lifeexpectancy', 'alcgroup']].dropna()

print ('means for lifeexpectancy by alcohol consumption')
m2= sub2.groupby('alcgroup').mean()
print (m2)

print ('standard deviations for lifeexpectancy by alcohol consumption')
sd2 = sub2.groupby('alcgroup').std()
print (sd2)

# using ols function for calculating the F-statistic and associated p value
model2 = smf.ols(formula='lifeexpectancy ~ C(alcgroup)', data=data1)
results2 = model2.fit()
print (results2.summary())

# post-hoc test
mc1 = multi.MultiComparison(sub2['lifeexpectancy'], sub2['alcgroup'])
res1 = mc1.tukeyhsd()
print(res1.summary())

