import pandas as pd 
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
import os
import sys

os.chdir(sys.path[0])


def transform_training_data(df):
	feature_columns = ['town', 'flat_type', 'block', 'street_name', 'storey_range',
	'floor_area_sqm', 'flat_model', 'lease_commence_date','age_at_transaction', 'distance_mrt','distance_city_hall']
	output_column = ['resale_price']

	predictors = df[feature_columns]
	output = df[output_column]
	predictors = predictors.drop(['block','street_name'], axis =1) 
	predictors = pd.get_dummies(predictors, columns =['flat_model','storey_range', 'flat_type','town'])
	predictors.reindex_axis(sorted(predictors.columns), axis = 1 )
	print(predictors.columns)
	return predictors, output 


def train_and_eval_random_forest(predictors, output):
	X_train, X_test, Y_train, Y_test = train_test_split(predictors.values, output.values, test_size = 0.2)
	rf_model = RandomForestRegressor(n_estimators = 100, verbose = 3)
	rf_model.fit(X_train,Y_train)
	RMSE = np.sqrt(mean_squared_error(rf_model.predict(X_test), Y_test))
	print('RMean Squared Error is ' + str(RMSE))
	print('Model Fitted')
	return rf_model

training_data = pd.read_csv(os.getcwd() + '/data/data_2017_latlong_withdist2.csv')
X,Y = transform_training_data(training_data)
fitted_model = train_and_eval_random_forest(X,Y)

with open(os.getcwd() + '/rf_pickled_model.pkl',"wb") as file_handler:
    pickle.dump(fitted_model, file_handler)

print('Model Dumped!')



