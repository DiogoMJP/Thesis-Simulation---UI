function update_food_spawn_rate_from_range(event) {
	let range_input = document.getElementById("food-spawn-rate-range");
	let number_input = document.getElementById("food-spawn-rate-number");

	number_input.value = range_input.value;
}

function update_food_spawn_rate_from_number(event) {
	let range_input = document.getElementById("food-spawn-rate-range");
	let number_input = document.getElementById("food-spawn-rate-number");

	range_input.value = number_input.value;
}