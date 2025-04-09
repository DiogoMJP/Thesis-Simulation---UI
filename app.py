from flask import Flask, render_template, redirect, request
import json

from DataManager import DataManager
from simulation.brain.HardCodedBrain import HardCodedBrain
from simulation.brain.NeatBrain import NeatBrain
from simulation.SimulationTemplate import SimulationTemplate
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

@app.route('/create_simulation_template', methods=['POST'])
def create_simulation_template():
	# Obtain the values submitted in the POST request and set to correct types
	data = request.form.to_dict()
	created_type = data["created-type"]
	data["n-agents"] = int(data["n-agents"])
	data["agents-lifespan-min"] = int(data["agents-lifespan-min"])
	data["agents-lifespan-range"] = int(data["agents-lifespan-range"])
	data["width"] = int(data["width"])
	data["height"] = int(data["height"])
	data["food-spawn-rate"] = float(data["food-spawn-rate"])
	data["food-lifespan-min"] = int(data["food-lifespan-min"])
	data["food-lifespan-range"] = int(data["food-lifespan-range"])
	data["food-detection-radius"] = float(data["food-detection-radius"])
	data["eating-number"] = int(data["eating-number"])
	data["max-time-steps"] = int(data["max-time-steps"])
	
	if created_type == "simulation-template":
		if data["name"] in data_manager.get_templates():
			# Return to the main page if a template with the same name already exists
			return redirect("/")
		else:
			# Otherwise, create a new template
			data_manager.create_template(SimulationTemplate(data))
			return redirect("/simulation_templates/" + data["name"])
	elif created_type == "simulation":
		if data["name"] in data_manager.get_simulations():
			# Return to the main page if a simulation with the same name already exists
			return redirect("/")
		else:
			# Otherwise, create a new simulation
			simulation = Simulation(data_manager)
			simulation.from_dict(data)
			simulation.brain = HardCodedBrain()
			simulation.create_agents()
			simulation.start_loop()
			data_manager.create_simulation(simulation)
			return redirect("/simulations/" + data["name"])
	elif created_type == "training":
		data["no-fitness-termination"] = data["no-fitness-termination"] == "True"
		data["pop-size"] = int(data["pop-size"])
		data["reset-on-extinction"] = data["reset-on-extinction"] == "True"
		data["n-generations"] = int(data["n-generations"])
		data["no-fitness-termination"] = data["no-fitness-termination"] == "True"
		data["no-fitness-termination"] = data["no-fitness-termination"] == "True"
		training = Training(data_manager)
		training.from_dict(data)
		training.set_config_file()
		training.start_training()
		data_manager.create_training(training)
		return redirect("/training/" + data["name"])

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
		if simulation.finished:
			return render_template('finished_simulation.html',
						  simulation=simulation.to_dict(), simulation_data=simulation.get_full_update_data())
		else:
			return render_template('live_simulation.html', simulation=simulation.to_dict())
	else:
		return redirect("/")

@app.route('/delete_simulation', methods=['POST'])
def delete_simulation():
	# Obtain the values submitted in the POST request
	simulation_name = request.form['simulation-name']

	if simulation_name in data_manager.get_simulations():
		data_manager.delete_simulation(simulation_name)
	
	return redirect("/")


@app.route('/simulations/<simulation>/update_simulation_data')
def update_simulation_data(simulation):
	if simulation in data_manager.get_simulations():
		return data_manager.get_simulations()[simulation].get_update_data()
	else:
		return redirect("/")


@app.route('/training/<training>')
def training_generations(training):
	if training in data_manager.get_trainings():
		training_obj = data_manager.get_training(training)
		return render_template('training_generations.html', training=training, generations=training_obj.get_gens_data())
	else:
		return redirect("/")

@app.route('/training/<training>/<generation>')
def training_generation(training, generation):
	generation = int(generation)
	if training in data_manager.get_trainings():
		training_obj = data_manager.get_training(training)
		return render_template('training_generation.html', training=training, generation=generation,
						 simulations=training_obj.get_gen_data(generation))
	else:
		return redirect("/")

@app.route('/training/<training>/<generation>/<simulation>')
def training_simulation(training, generation, simulation):
	generation = int(generation)
	if training in data_manager.get_trainings():
		training = data_manager.get_training(training)
		simulation = training.simulations[generation][int(simulation)][0]
		return render_template('training_simulation.html',
						  simulation=simulation.to_dict(), simulation_data=simulation.get_full_update_data())
	else:
		return redirect("/")

@app.route('/delete_training', methods=['POST'])
def delete_training():
	# Obtain the values submitted in the POST request
	training_name = request.form['training-name']

	if training_name in data_manager.get_trainings():
		data_manager.delete_training(training_name)
	
	return redirect("/")