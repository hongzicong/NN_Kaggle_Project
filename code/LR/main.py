# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:47:30 2019

@author: Dv00
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt;
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

sns.set()

train, test = pd.read_csv('../../data/train.csv'), pd.read_csv('../../data/test.csv')

missing=train.columns[train.isnull().any()].tolist()

# print(train[missing].isnull().sum() / 891)

#plt.figure()
#corrMat = train.corr()
#mask = np.array(corrMat)
#mask[np.tril_indices_from(mask)] = False
#sns.set(font_scale=1)
#sns.heatmap(corrMat, mask=mask,vmax=.8, square=True,annot=True,cmap="YlGnBu")
#plt.xticks(rotation=30)
#plt.yticks(rotation=30)

def fill_missing_age(rows):
    Age = rows[0]
    Pclass = rows[1]
    
    if pd.isnull(Age):

        if Pclass == 1:
            return 37

        elif Pclass == 2:
            return 29

        else:
            return 24

    else:
        return Age

train['isMaster'], test['isMaster'] = [(df.Name.str.split().str[1] == 'Master.').astype('int') for df in [train, test]]

sex_train = pd.get_dummies(train['Sex'],drop_first=True)
embark_train = pd.get_dummies(train['Embarked'],drop_first=True)
train = train.drop(['Sex', 'Embarked', 'Name', 'Ticket'],axis=1)
train = pd.concat([train, sex_train, embark_train],axis=1)

train['Age'] = train[['Age','Pclass']].apply(fill_missing_age, axis=1)

train.drop('Cabin',axis=1,inplace=True)

train.dropna(inplace=True)

sex_test = pd.get_dummies(test['Sex'],drop_first=True)
embark_test = pd.get_dummies(test['Embarked'],drop_first=True)
test = test.drop(['Sex', 'Embarked', 'Name','Ticket'],axis=1)
test = pd.concat([test, sex_test, embark_test],axis=1)

test['Age'] = test[['Age','Pclass']].apply(fill_missing_age, axis=1)

test.drop('Cabin',axis=1,inplace=True)

test['Fare'].fillna(test['Fare'].mean(), inplace=True)

X_train, X_test, y_train, y_test = train_test_split(train.drop('Survived',axis=1), 
                                                    train['Survived'], test_size=0.20, 
                                                    random_state=101)

logmodel = LogisticRegression()

logmodel.fit(X_train,y_train)

train_predictions = logmodel.predict(X_test)
print(classification_report(y_test, train_predictions, digits=4))

predictions = pd.DataFrame(logmodel.predict(test), columns= ['Survived'])

predictions = pd.concat([test['PassengerId'], predictions], axis=1, join='inner')

predictions.to_csv('predictions.csv' , index=False)