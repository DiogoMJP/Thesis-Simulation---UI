from flask import Flask, render_template, redirect, request, url_for
import json

from DataManager import DataManager
from simulation.Simulation import Simulation
from simulation.Training import Training



app = Flask(__name__)


data_manager = DataManager()


@app.route('/')
def index():
	training_vals = [training.get_list_data() for training in data_manager.get_trainings().values()]
	sim_vals = [sim.get_list_data() for sim in data_manager.get_simulations().values()]
	temp_vals = data_manager.get_templates().keys()
	return render_template('index.html', simulation_templates=temp_vals, simulations=sim_vals, training=training_vals)

@app.route('/error_page', methods=['POST'])
def error():
	message = request.args['message']
	return render_template('error_page.html', error_message=message)

@app.route('/create_simulation_template', methods=['POST'])
def create_simulation_template():
	# Obtain the values submitted in the POST request and set to correct types
	data = request.form.to_dict()

	if "created-type" in data:
		if data["created-type"] == "simulation":
			if data["name"] not in data_manager.get_simulations():
				Simulation.create_from_user_data(data, data_manager)
				return redirect(f'/simulations/{data["name"]}')
			else:
				return redirect('/')
		elif data["created-type"] == "training":
			if data["name"] not in data_manager.get_trainings():
				Training.create_from_user_data(data, data_manager)
				return redirect(f'/training/{data["name"]}')
			else:
				return redirect('/')


@app.route('/simulation_templates/<template>')
def simulation_template(template):
	if template in data_manager.get_templates():
		return render_template('simulation_template.html', template=data_manager.get_templates()[template].to_dict())
	else:
		return redirect("/")

@app.route('/delete_simulation_template', methods=['POST'])
def delete_simulation_template():
	# Obtain the values submitted in the POST request
	template_name = request.form['template-name']

	if template_name in data_manager.get_templates():
		data_manager.delete_template(template_name)
	
	return redirect("/")


@app.route('/create_simulation', methods=['POST'])
def create_simulation():
	# Obtain the values submitted in the POST request
	simulation_name = request.form['simulation-name']
	template_name = request.form['template-name']
	
	if simulation_name in data_manager.get_simulations():
		# Return to the main page if a simulation with the same name already exists
		return redirect("/")
	else:
		# Otherwise, create a new simulation
		template = data_manager.get_templates()[template_name]
		template.create_simulation(simulation_name, data_manager)
		# Send the user to the corresponding simulation's page
		return redirect("/simulations/" + simulation_name)

@app.route('/simulations/<simulation>')
def simulation(simulation):
	if simulation in data_manager.get_simulations():
		simulation = data_manager.get_simulation(simulation)
		if simulation.finished and simulation.saved:
			return render_template('finished_simulation.html', data=simulation.get_finished_page_data())
		else:
			return render_template('live_simulation.html', data=simulation.to_dict())
	else:
		return redirect("/")

@app.route('/delete_simulation', methods=['POST'])
def delete_simulation():
	# Obtain the values submitted in the POST request
	simulation_name = request.form['simulation-name']

	if simulation_name in data_manager.get_simulations():
		data_manager.delete_simulation(simulation_name)
	
	return redirect("/")


@app.route('/simulations/live_simulation_data', methods=['POST'])
def update_simulation_data():
	simulation_name = request.json['simulation-name']

	if simulation_name in data_manager.get_simulations():
		return json.dumps(data_manager.get_simulation(simulation_name).get_live_data())
	else:
		return json.dumps({})


@app.route('/training/<training>')
def training_generations(training):
	if training in data_manager.get_trainings():
		training_obj = data_manager.get_training(training)
		return render_template('training_generations.html', training=training, generations=training_obj.get_gens_data())
	else:
		return redirect("/")

@app.route('/training/<training>/<generation>')
def training_generation(training, generation):
	if training in data_manager.get_trainings():
		training_obj = data_manager.get_training(training)
		return render_template('training_generation.html', training=training, generation=generation,
						 simulations=training_obj.get_gen_data(generation))
	else:
		return redirect("/")

@app.route('/training/<training>/<generation>/<simulation>')
def training_simulation(training, generation, simulation):
	if training in data_manager.get_trainings():
		training = data_manager.get_training(training)
		simulation = training.get_simulation(generation, simulation)
		if simulation == None:
			return redirect("/")
		if simulation.finished:
			return render_template('finished_training_simulation.html', data=training.get_finished_page_data(generation, simulation))
		else:
			return render_template('live_training_simulation.html', data=training.get_live_page_data(generation, simulation))
	else:
		return redirect("/")

@app.route('/simulations/live_training_simulation_data', methods=['POST'])
def update_training_simulation_data():
	training_name = request.json["training-name"]
	generation = request.json["generation"]
	simulation_name = request.json['simulation-name']

	if training_name in data_manager.get_trainings():
		training = data_manager.get_training(training_name)
		simulation = training.get_simulation(generation, simulation)
		if simulation == None:
			return json.dumps({})
		else:
			return json.dumps(simulation.get_live_data())
	else:
		return json.dumps({})

@app.route('/delete_training', methods=['POST'])
def delete_training():
	# Obtain the values submitted in the POST request
	training_name = request.form['training-name']

	if training_name in data_manager.get_trainings():
		data_manager.delete_training(training_name)
	
	return redirect("/")