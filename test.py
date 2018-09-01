from execute_model import model_predict

# def model_predict(sqm,lease_sd,age,dist_mrt,dist_city_hall,flat_model_CAT,storey_range_CAT,flat_type_CAT,town_CAT):
#   with open('./rf_pickled_model.pkl','rb') as file_handler:
#     fitted_model = pickle.load(file_handler)
#   flat_model_discretize = 'flat_model_' + str(flat_model_CAT)
#   print(flat_model_discretize)
#   storey_range_discretize = 'storey_range_' + str(storey_range_CAT)
#   print(storey_range_discretize)
#   flat_type_discretize = 'flat_type_' + str(flat_type_CAT)
#   town_discretize = 'town_' + str(town_CAT)
#   dictionary = {'floor_area_sqm' : [float(sqm)], 
#     'lease_commence_date': [int(lease_sd)],
#     'age_at_transaction': [int(age)],
#     'distance_mrt': [float(dist_mrt)],
#     'distance_city_hall': [float(dist_city_hall)],
#   flat_model_discretize: [1], 
#   storey_range_discretize: [1],
#   flat_type_discretize: [1],
#   town_discretize: [1]}
#   print(dictionary.keys())
#   diff = np.setdiff1d(colnames,list(dictionary.keys()))
#   print(diff)
#   df = pd.DataFrame.from_dict(dictionary)
#   print(df)
#   for col in diff:
#     df.loc[0,col] = int(0)
#   df = df[colnames]
#   #print(df.columns)
#   #print(fitted_model.predict(df.loc[0].values.reshape(1,-1)))
#   prediction = fitted_model.predict(df.loc[0].values.reshape(1,-1))
#   return(prediction[0])

x = model_predict(100,1990,20,100,1000,'Adjoined flat','04 TO 06','4 ROOM','ANG MO KIO')
print(x)