from flask import Flask, request, render_template
import pickle
from sklearn.ensemble import RandomForestRegressor
from geocoding_api import OneMapSearch, Searcher, compute_nearest_mrt_dist, compute_distance_city_hall
import execute_model
import json
import pandas as pd
import numpy as np
import requests



app = Flask(__name__)



@app.route('/')
def flask_homepage():
	return(render_template('homepage.html'))

@app.route('/collect_data', methods = ['POST'])
def collect_data():
	error_messages_list = []



	try:
		floor_area_sqm = float(request.form['fa_sqm'])
		print('FLoor area sqm = ' + str(floor_area_sqm))
	except ValueError:
		floor_area_sqm = None
		error_messages_list.append('Floor Area needs to be numeric')
	
	try:
		lease_start_date = int(request.form['lease_sd'])
		print('Lease start date = ' + str(lease_start_date))
		age = 2017 - lease_start_date


	except ValueError:
		lease_start_date = None
		error_messages_list.append('Lease Start Date needs to be numberic')

	try:
		address_str = str(request.form['address'])
	except ValueError:
		address = None
		error_messages_list.append('Address needs to be re-entered ')

	if len(address_str) > 0: 
		address = Searcher(address_str)
	else:
		error_messages_list.append('Address needs to be re-entered ')


	town = request.form['town']
	storey_range = request.form['storey_range']
	flat_type = request.form['flat_type']
	flat_model = request.form['flat_model']

	if len(error_messages_list) != 0:
		return(render_template('error_message.html', error = error_messages_list[0]))
	elif address == 'Error':
		return(render_template('error_message.html', error = 'The address cannot be geocoded'))
	else:
		address_lon = float(address['LONGTITUDE'])
		address_lat = float(address['LATITUDE'])
		print(address_lon)
		print(address_lat)

		dist_mrt = compute_nearest_mrt_dist(address_lon, address_lat)
		dist_city_hall = compute_distance_city_hall(address_lon,address_lat)
		print(str(dist_mrt))
		print(str(dist_city_hall))

		predicted_resale_value = None
		print('Execute Model!!!')
		predicted_resale_value = execute_model.model_predict(floor_area_sqm, lease_start_date,age,dist_mrt,dist_city_hall,flat_model,storey_range,flat_type,town)
		print('resale_value' + str(predicted_resale_value))
		# pdb.set_trace()
		return(render_template('predictions.html', value = predicted_resale_value ))

if __name__ == '__main__':
	app.run()
	

