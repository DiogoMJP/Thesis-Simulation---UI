from flask import Flask, render_template, redirect, request
import json

from DataManager import DataManager
from SimulationTemplate import SimulationTemplate
from Simulation import Simulation



app = Flask(__name__)


data_manager = DataManager()


@app.route('/')
def index():
	sim_vals = [sim.get_list_data() for sim in data_manager.get_simulations().values()]
	temp_vals = data_manager.get_templates().keys()
	return render_template('index.html', simulation_templates=temp_vals, simulations=sim_vals)

@app.route('/create_simulation_template', methods=['POST'])
def create_simulation_template():
	# Obtain the values submitted in the POST request
	template_name = request.form['template-name']
	n_agents = int(request.form['n-agents'])
	width = int(request.form['width'])
	height = int(request.form['height'])
	food_spawn_rate = float(request.form['food-spawn-rate'])
	food_detection_radius = float(request.form['food-detection-radius'])
	max_time_steps = int(request.form['max-time-steps'])

	if template_name in data_manager.get_templates():
		# Return to the main page if a template with the same name already exists
		return redirect("/")
	else:
		# Otherwise, create a new template
		data_manager.create_template(SimulationTemplate(template_name, n_agents, width, height,
											food_spawn_rate, food_detection_radius, max_time_steps))
		return redirect("/simulation_templates/" + template_name)

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
		simulation = Simulation()
		simulation.set_data_manager(data_manager)
		simulation.set_name(simulation_name)
		simulation.set_n_agents(template.get_n_agents())
		simulation.set_width(template.get_width())
		simulation.set_height(template.get_height())
		simulation.set_food_spawn_rate(template.get_food_spawn_rate())
		simulation.set_food_detection_radius(template.get_food_detection_radius())
		simulation.set_max_time_steps(template.get_max_time_steps())
		simulation.create_agents()
		data_manager.create_simulation(simulation)
		simulation.start_loop()
		# Send the user to the corresponding simulation's page
		return redirect("/simulations/" + simulation_name)

@app.route('/simulations/<simulation>')
def simulation(simulation):
	if simulation in data_manager.get_simulations():
		simulation = data_manager.get_simulations()[simulation]
		if simulation.get_finished():
			return render_template('finished_simulation.html', simulation=simulation.to_dict())
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


@app.route('/simulations/<simulation>/update_simulation_data/<time_step>')
def update_simulation_data_from_time_step(simulation, time_step):
	if simulation in data_manager.get_simulations():
		time_step = int(time_step)
		return data_manager.get_simulations()[simulation].get_update_data_from_time_step(time_step)
	else:
		return redirect("/")