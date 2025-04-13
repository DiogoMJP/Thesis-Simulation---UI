function updateData() {
	fetch("/simulations/live_training_simulation_data", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},		
		body: JSON.stringify({"training-name": training_name, "generation": generation, "simulation-name": simulation_name}),
	})
		.then(response => response.json())
		.then(d => {
			if (!(d["finished"] && d["saved"]))
				window.setTimeout(updateData, 10);
			else
				location.reload();
			
			time_step_span.innerText = d["time_step"];
			n_agents_span.innerText = d["n_agents"];
			finished_span.innerText = d["finished"];
			saved_span.innerText = d["saved"];
		});
}

const time_step_span = document.getElementById("time-step");
const n_agents_span = document.getElementById("n-agents");
const finished_span = document.getElementById("finished");
const saved_span = document.getElementById("saved");

updateData();