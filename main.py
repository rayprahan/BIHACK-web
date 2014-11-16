import pandas as pd
from flask import Flask, request, url_for, render_template, redirect, flash, jsonify, abort

app = Flask(__name__)
df = pd.read_csv('./data/dummy_data.csv')

@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/map')
def show_map():
    return render_template('map.html')

@app.route('/calls')
def calls():
    return render_template('calls.html')

@app.route('/add', methods=['POST'])
def add_entry():
	address = request.form['Address'].upper()
	r = df[df.Street == address]
	s = zip(r['Event Date/Time'].tolist(), r.Event.tolist(), r['Event Nature'].tolist())
	return render_template('AddressExists.html', p=r.P.max(), name='Al Pacino', dates_records_details=s)

@app.route('/api/get_all', methods=['GET'])
def get_all():
	master_dict = {}
	for address in df.Street.drop_duplicates():
		temp_dict = {}
		temp_table = df[df.Street == address].ix[:,1:]

		temp_dict['probability'] = temp_table.P.max()
		temp_dict['incidents'] = temp_table.ix[:,:-1].to_dict('records')

		master_dict[address] = temp_dict

	return jsonify({'get_all': master_dict})

@app.route('/api/get_profile/<string:address>', methods=['GET'])
def get_profile(address):
	"""Input address, get all the events as JSON. One event consists of arrest/call, date, and p. P pertains to the address, which is the unique ID here."""
	address = address.upper()

	if address not in df.Street.values:
		abort(404)
	else:
		temp_dict = {}
		temp_table = df[df.Street == address].ix[:,1:]

		temp_dict['probability'] = temp_table.P.max()
		temp_dict['incidents'] = temp_table.ix[:,:-1].to_dict('records')

		return jsonify({'get_profile': temp_dict})

# For running Flask locally
if __name__ == '__main__':
    app.run(debug=True)