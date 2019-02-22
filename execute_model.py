import pickle
import pandas as pd
import numpy as np
import pickle
import os


colnames = ['floor_area_sqm', 'lease_commence_date', 'age_at_transaction',
'distance_mrt', 'distance_city_hall', 'flat_model_Adjoined flat',
'flat_model_Apartment', 'flat_model_DBSS', 'flat_model_Improved',
'flat_model_Improved-Maisonette', 'flat_model_Maisonette',
'flat_model_Model A', 'flat_model_Model A-Maisonette',
'flat_model_Model A2', 'flat_model_Multi Generation',
'flat_model_New Generation', 'flat_model_Premium Apartment',
'flat_model_Premium Apartment Loft', 'flat_model_Premium Maisonette',
'flat_model_Simplified', 'flat_model_Standard', 'flat_model_Terrace',
'flat_model_Type S1', 'flat_model_Type S2', 'storey_range_01 TO 03',
'storey_range_04 TO 06', 'storey_range_07 TO 09',
'storey_range_10 TO 12', 'storey_range_13 TO 15',
'storey_range_16 TO 18', 'storey_range_19 TO 21',
'storey_range_22 TO 24', 'storey_range_25 TO 27',
'storey_range_28 TO 30', 'storey_range_31 TO 33',
'storey_range_34 TO 36', 'storey_range_37 TO 39',
'storey_range_40 TO 42', 'storey_range_43 TO 45',
'storey_range_46 TO 48', 'storey_range_49 TO 51', 'flat_type_1 ROOM',
'flat_type_2 ROOM', 'flat_type_3 ROOM', 'flat_type_4 ROOM',
'flat_type_5 ROOM', 'flat_type_EXECUTIVE', 'flat_type_MULTI-GENERATION',
'town_ANG MO KIO', 'town_BEDOK', 'town_BISHAN', 'town_BUKIT BATOK',
'town_BUKIT MERAH', 'town_BUKIT PANJANG', 'town_BUKIT TIMAH',
'town_CENTRAL AREA', 'town_CHOA CHU KANG', 'town_CLEMENTI',
'town_GEYLANG', 'town_HOUGANG', 'town_JURONG EAST', 'town_JURONG WEST',
'town_KALLANG/WHAMPOA', 'town_MARINE PARADE', 'town_PASIR RIS',
'town_PUNGGOL', 'town_QUEENSTOWN', 'town_SEMBAWANG', 'town_SENGKANG',
'town_SERANGOON', 'town_TAMPINES', 'town_TOA PAYOH', 'town_WOODLANDS',
'town_YISHUN']

def model_predict(sqm,lease_sd,age,dist_mrt,dist_city_hall,flat_model_CAT,storey_range_CAT,flat_type_CAT,town_CAT):
  with open('./rf_pickled_model.pkl','rb') as file_handler:
    fitted_model = pickle.load(file_handler)
  flat_model_discretize = 'flat_model_' + str(flat_model_CAT)
  print(flat_model_discretize)
  storey_range_discretize = 'storey_range_' + str(storey_range_CAT)
  print(storey_range_discretize)
  flat_type_discretize = 'flat_type_' + str(flat_type_CAT)
  town_discretize = 'town_' + str(town_CAT)
  dictionary = {'floor_area_sqm' : [float(sqm)], 
    'lease_commence_date': [int(lease_sd)],
    'age_at_transaction': [int(age)],
    'distance_mrt': [float(dist_mrt)],
    'distance_city_hall': [float(dist_city_hall)],
  flat_model_discretize: [1], 
  storey_range_discretize: [1],
  flat_type_discretize: [1],
  town_discretize: [1]}
  print(dictionary.keys())
  diff = np.setdiff1d(colnames,list(dictionary.keys()))
  print(diff)
  df = pd.DataFrame.from_dict(dictionary)
  print(df)
  for col in diff:
    df.loc[0,col] = int(0)
  df = df[colnames]
  #print(df.columns)
  #print(fitted_model.predict(df.loc[0].values.reshape(1,-1)))
  prediction = fitted_model.predict(df.loc[0].values.reshape(1,-1))
  return(int(round(prediction[0])))


