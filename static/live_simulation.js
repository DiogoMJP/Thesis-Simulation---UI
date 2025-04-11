function updateData() {
	fetch("/simulations/live_simulation_data", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},		
		body: JSON.stringify({"simulation-name": simulation_name}),
	})
		.then(response => response.json())
		.then(d => {
			if (!d["finished"])
				window.setTimeout(updateData, 10);
			else
				location.reload();
			
			time_step_span.innerText = d["time_step"];
			n_agents_span.innerText = d["n_agents"];
		});
}

const time_step_span = document.getElementById("time-step");
const n_agents_span = document.getElementById("n-agents");

updateData();