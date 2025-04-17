function countLiveAgents() {
	let count = 0;
	for (let i = 0; i < data["agents"].length; i++) {
		if (data["agents"][i]["last-time-step"] > time_step) {
			count++;
		}
	}
	return count;
}


function updateCanvas() {
	context.fillStyle = "white";
	context.fillRect(0, 0, canvas.width, canvas.height);
	
	context.fillStyle = "black";
	context.fillRect(midpoint + canvas_x * zoom,
		midpoint + canvas_y * zoom,
		data["width"] * zoom,
		data["height"] * zoom);
	
	for (let i = 0; i < data["food"].length; i++) {
		if (data["food"][i]["first-time-step"] <= time_step && data["food"][i]["last-time-step"] >= time_step) {
			context.globalAlpha = 0.2;
			context.fillStyle = "yellow";
			context.beginPath();
			let x = midpoint + (data["food"][i]["x"] + canvas_x) * zoom;
			let y = midpoint + (data["food"][i]["y"] + canvas_y) * zoom;
			context.arc(x, y, data["food-detection-radius"] * zoom, 0, 2*Math.PI);
			context.fill();
			context.stroke();

			context.globalAlpha = 1.0;
			context.fillStyle = "green";
			context.beginPath();
			x = midpoint + (data["food"][i]["x"] + canvas_x) * zoom;
			y = midpoint + (data["food"][i]["y"] + canvas_y) * zoom;
			context.arc(x, y, 5, 0, 2*Math.PI);
			context.fill();
			context.stroke();
		}
	}

	for (let i = 0; i < data["agents"].length; i++) {
		if (data["agents"][i]["last-time-step"] >= time_step) {
			context.fillStyle = "red";
			context.beginPath();
			let x = midpoint + (data["agents"][i]["history"][time_step][0] + canvas_x) * zoom;
			let y = midpoint + (data["agents"][i]["history"][time_step][1] + canvas_y) * zoom;
			context.arc(x, y, 5, 0, 2*Math.PI);
			context.fill();
			context.stroke();
		}
	}
}


function updateData() {
	time_step_span.innerText = time_step;
		
	if (playing) {
		if (time_step == 1) {
			document.getElementById("prev-time-step").className = "";
		}
		if (time_step == data["last-time-step"] - 1) {
			playing = false;
			document.getElementById("play").innerHTML = "&#9658;";
			document.getElementById("play").className = "unavailable";
			document.getElementById("next-time-step").className = "unavailable";
		} else {
			time_step += 1;
			window.setTimeout(updateData, 10);
		}
	}

	updateCanvas();
	document.getElementById("n-agents").innerText = countLiveAgents();
}


function get_prev_time_step() {
	playing = false;
	document.getElementById("play").innerHTML = "&#9658;";
	if (time_step > 0) {
		time_step--;
		updateData();
	}
	if (time_step == 0) {
		document.getElementById("prev-time-step").className = "unavailable";
	}
	if (time_step == data["last-time-step"] - 2) {
		document.getElementById("play").className = "";
		document.getElementById("next-time-step").className = "";
	}
}

function get_next_time_step() {
	playing = false;
	document.getElementById("play").innerHTML = "&#9658;";
	if (time_step < data["last-time-step"] - 1) {
		time_step++;
		updateData();
	}
	if (time_step == 1) {
		document.getElementById("prev-time-step").className = "";
	}
	if (time_step == data["last-time-step"] - 1) {
		document.getElementById("next-time-step").className = "unavailable";
		document.getElementById("play").className = "unavailable";
	}
}

function toggle_play() {
	if (time_step < data["last-time-step"] - 1) {
		playing = !playing;
		if (playing)
			document.getElementById("play").innerHTML = "&#9208;";
		else
			document.getElementById("play").innerHTML = "&#9658;";
		time_step += 1;
		updateData();
	}
}

function reset() {
	time_step = 0;
	playing = false;

	document.getElementById("prev-time-step").className = "unavailable";
	document.getElementById("next-time-step").className = "";
	document.getElementById("play").innerHTML = "&#9658;";
	document.getElementById("play").className = "";

	updateData();
}

const time_step_span = document.getElementById("time-step");
const canvas = document.getElementById("simulation-canvas");
const context = canvas.getContext('2d', {willReadFrequently: true});

let time_step = 0;
let playing = false;

let zoom = 1;
let midpoint = 300;
let canvas_x = 0;
let canvas_y = 0;
let moving = false;
let mouse_x = 0;
let mouse_y = 0;

canvas.onwheel = (event) => {
	event.preventDefault();
	if (event.deltaY > 0)
		zoom /= 1.125
	else if (event.deltaY < 0)
		zoom *= 1.125
	updateCanvas();
};
canvas.onmousedown = (event) => {	
	moving = true;
	mouse_x = event.screenX;
	mouse_y = event.screenY;
}
document.onmousemove = (event) => {
	if (moving) {
		canvas_x += (event.screenX - mouse_x) / zoom;
		canvas_y += (event.screenY - mouse_y) / zoom;
		mouse_x = event.screenX;
		mouse_y = event.screenY;
		updateCanvas();
	}
}
document.onmouseup = document.onmouseleave = (event) => {
	moving = false;
}
function get_distance(e) {
	var diffX = e.touches[0].clientX - e.touches[1].clientX;
	var diffY = e.touches[0].clientY - e.touches[1].clientY;
	return Math.sqrt(diffX * diffX + diffY * diffY); // Pythagorean theorem
}
document.ontouchstart = (event) => {
	if (event.touches.length > 1) {
		event.preventDefault();
		finger_dist = get_distance(e);
	}
	mouse_x = event.touches[0].clientX;
	mouse_y = event.touches[0].clientY;
}
document.ontouchmove = (event) => {
	event.preventDefault();
    if (event.touches.length > 1) {
    	var new_finger_dist = get_distance(e);
    	zoom = zoom * Math.abs(finger_dist / new_finger_dist);
    	finger_dist = new_finger_dist;
    } else {
    	canvas_x = canvas_x + (zoom * 0.25 *(mouse_x - event.touches[0].clientX));
    	canvas_y = canvas_y + (zoom * 0.25 *(mouse_y - event.touches[0].clientY));
    	mouse_x = e.touches[0].clientX;
    	mouse_y = e.touches[0].clientY;
    }
    update_canvas();
}
document.ontouchend = (event) => {
	event.preventDefault();
	mouse_x = event.touches[0].clientX;
    mouse_y = event.touches[0].clientY;
}

updateData();