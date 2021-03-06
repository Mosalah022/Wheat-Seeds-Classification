# -*- coding: utf-8 -*-
"""SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19YkguOFFbtrHKW6-nwGHAgpMmLmKJQPt

#Cover Page

**Developed by:**

**Fatma Mohamed Ali - 41810121**

**Mohamed Salah Eldin - 41810303**

#Description of data:

**This data was acquired from the 'UCI Center for Machine Learning' repository. It contains seven variables for three distinct types of wheat kernels: (Kama, Rosa, Canadian) designated as numerical variables 1, 2 & 3 respectively The last column is reserved for the Kernel type**

#Import the dataset from drive
"""

!gdown --id 1MbUWPsEZJ_Dana5RC07wUGTIgzN92Uld

"""#Importing libraries"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn import svm
from sklearn import metrics

"""# show how the data looks like"""

df = pd.read_csv("seeds.csv")
df.head()

"""# Check if all data are numbers and if there is a relations between the data

"""

df.dtypes

df.info()

df.columns

#from sklearn.preprocessing import LabelEncoder
#encoder = LabelEncoder()

"""#Heatmap"""

#df.corr()
x,y = plt.subplots(figsize=(12,9))
sns.heatmap(df.corr(),cmap='YlGnBu',square=True,linewidth=.5,annot=True)
plt.show()

"""# Check for the null """

df.isna().any()
#df.isnull().sum()
df.dropna()

"""# show mean, max , min so handle the data if there is a gap between 75% and max  

"""

df.describe()

"""# check for the outlier"""

"""
df['Area'].skew()
df['Asymmetry.Coeff'].skew()
plt.boxplot(df['Kernel.Groove'])
plt.show()
"""
df.hist(bins=50,figsize=(20,15))
plt.show()

df.shape

"""**drop the outlier**

"""

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
print (IQR)
df = df[~((df < (Q1 - 1.5 *  IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
print (df.shape)

df.hist(bins=50,figsize=(20,15))
plt.show()

"""#Normalization"""

scaler=StandardScaler()
scaler.fit(df)
dataset=scaler.transform(df)
dataset

"""#Start Split the data and train"""

df_target = df["Type"]  #save target for training set
df = df.drop("Type", axis=1) #drop target for training set

"""**train_test_split imported from sklearn.model_selection**"""

"""
#split the data for training and validation
First Way to split data 
train_set_size= int(len (df) * 0.7)
train_set = df [:train_set_size][:]
valid_set = df [train_set_size:][:]

train_target = df_target [:train_set_size]
valid_target = df_target [train_set_size:]
print(len (train_set), "train +", len(valid_set), "valid")
"""
#second way
#train_set, valid_set = train_test_split(df, test_size=0.2)
#train_target, valid_target = train_test_split (df_target, test_size=0.2)

X_train, X_valid, y_train, Y_valid = train_test_split(df, df_target, test_size = 0.2,random_state=109)
print(len(X_train), "train +", len(X_valid), "valid")

"""#Using **SVM** model for trainning

**Kernel = poly can be kernel{???linear???, ???poly???, ???rbf???, ???sigmoid???, ???precomputed???}, default=???rbf???**
"""

#Create a svm Classifier
clf = svm.SVC(kernel='poly') # poly

"""**Train the model using the training sets**

"""

clf.fit(X_train, y_train)

"""**Predict the response for test dataset**"""

y_pred = clf.predict(X_valid)

"""**Import scikit-learn metrics module for accuracy calculation**

**Model Accuracy: how often is the classifier correct?**
"""

print("Accuracy:",metrics.accuracy_score(Y_valid, y_pred))

"""#find the mean square error

**mean_squared_error imported from from sklearn.metrics**

**np.sqrt imported from numpy**
"""

lin_mse = mean_squared_error(Y_valid, y_pred)
lin_rmse = np.sqrt(lin_mse)
lin_rmse

"""**mean_absolute_error imported from from sklearn.metrics**

"""

lin_mae = mean_absolute_error(Y_valid, y_pred)
lin_mae