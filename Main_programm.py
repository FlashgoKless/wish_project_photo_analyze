import pandas as pd
from openpyxl import *
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score


df = pd.read_excel('encodings_1.xlsx')

X = df.drop('target', axis = 1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=0.8,random_state=1)


example=pd.read_excel('Primer.xlsx')


model = RandomForestRegressor()
model.fit(X_train, y_train)
y_pred=model.predict(X_test)
mae=mean_absolute_error(y_test,y_pred)
r_sq = model.score(X_train, y_train)




example_df = pd.DataFrame(example)
print('---------------------------------------------------------------------------------------|')
print('mae: ',mae)
print('coefficient of determination:', r_sq)
print('---------------------------------------------------------------------------------------|')
print('Прогноз: ',model.predict(example))
print('---------------------------------------------------------------------------------------|')
