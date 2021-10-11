# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:10:50 2020

@author: KGU2BAN
"""
#%% clean data and split into train and test
import pandas as pd
from sklearn.model_selection import train_test_split
x = pd.read_csv('train.csv')
x.isna().sum()
mean_age = x['Age'].mean()
x.fillna({'Age': mean_age}, inplace=True)
x.isna().sum()
x = x.loc[x['Embarked'].notna(),:]
x.isna().sum()
x.dtypes
x['PassengerId'] = x['PassengerId'].astype('float64')
x.drop(['Name', 'Ticket', 'Cabin'], axis=1, inplace=True)
y = x.pop('Survived')
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42)
cat_column = ['Pclass', 'Sex', 'SibSp', 'Parch', 'Embarked']
num_column = ['PassengerId', 'Age', 'Fare']


#%% create dataflow and model pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
ct = ColumnTransformer([('ohe', OneHotEncoder(sparse=False, handle_unknown='ignore'), cat_column),
                        ('scale',StandardScaler(), num_column)], remainder='drop')
pipeline = Pipeline([('column_transform', ct),
                     ('model', SVC(C=1.5, kernel='rbf'))])

pipeline.fit(x_train, y_train)
pipeline.score(x_test, y_test)

cross_val_score(pipeline, x_train, y_train, cv=5)

#%%save the model in pickle format
import joblib
joblib.dump(pipeline, 'model.pkl')

#%% test the data, json in postman app will only take double quotes
sample_input = [{"PassengerId":1, "Pclass":3, "Sex":"male", "Age":22, "SibSp":1, "Parch":0, "Fare":7.25, "Embarked":"S"},
                {"PassengerId":2, "Pclass":1, "Sex":"female", "Age":38, "SibSp":1, "Parch":0, "Fare":71.2833, "Embarked":"C"}]

df_sample_input = pd.DataFrame(sample_input, columns=['PassengerId', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare','Embarked'])
model = joblib.load('model.pkl')
prediction = {"prediction": model.predict(df_sample_input).tolist()}
print(prediction)
