from functions import evaluate_model
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.max_columns', None)

df = pd.read_csv(f'datasets/dataset_ML.csv')
print(df.head())
print()


df['is_superhost'] = df['is_superhost'].replace('false',0).replace('true',1)
df.drop(columns='ad_id', axis=1, inplace=True)
y = df['price']
X = df.drop('price', axis=1)

y = df['price']
X = df.drop('price', axis=1)


# train, test, split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1000)

model_rf = RandomForestRegressor()
model_lr = LinearRegression()
model_et = ExtraTreesRegressor()

models = {'RandomForest': model_rf,
          'LinearRegression': model_lr,
          'ExtraTrees': model_et}

for model_name, model in models.items():
    #train
    model.fit(X_train, y_train)
    
    #test
    predict = model.predict(X_test)
    print(evaluate_model(model_name, y_test, predict))

