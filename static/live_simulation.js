function updateCanvas() {
	context.fillStyle = "white";
	context.fillRect(0, 0, canvas.width, canvas.height);
	
	context.fillStyle = "black";
	context.fillRect(midpoint + (data["background"]["x"] + canvas_x) * zoom,
		midpoint + (data["background"]["y"] + canvas_y) * zoom,
		data["background"]["width"] * zoom,
		data["background"]["height"] * zoom);
	
	for (let i = 0; i < data["food"].length; i++) {
		context.globalAlpha = 0.2;
		context.fillStyle = "yellow";
		context.beginPath();
		let x = midpoint + (data["food"][i]["x"] + canvas_x) * zoom;
		let y = midpoint + (data["food"][i]["y"] + canvas_y) * zoom;
		context.arc(x, y, data["food"][i]["detection_radius"] * zoom, 0, 2*Math.PI);
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

	for (let i = 0; i < data["agents"].length; i++) {
		context.fillStyle = "red";
		context.beginPath();
		let x = midpoint + (data["agents"][i]["x"] + canvas_x) * zoom;
		let y = midpoint + (data["agents"][i]["y"] + canvas_y) * zoom;
		context.arc(x, y, 5, 0, 2*Math.PI);
		context.fill();
		context.stroke();
	}
}


function updateData() {
	fetch(update_url)
		.then(response => response.json())
		.then(d => {
			data = d;
			console.log(data);
			if (!data["finished"])
				window.setTimeout(updateData, 1000);
			else
				location.reload();
			
			time_step_span.innerText = data["time_step"];
		
			updateCanvas();
		});
}

const time_step_span = document.getElementById("time-step");
const canvas = document.getElementById("simulation-canvas");
const context = canvas.getContext('2d', {willReadFrequently: true});

let data = null;

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
		zoom /= 1.2
	else if (event.deltaY < 0)
		zoom *= 1.2
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
    	canvas_x = canvas_x + (zoom * (mouse_x - event.touches[0].clientX));
    	canvas_y = canvas_y + (zoom * (mouse_y - event.touches[0].clientY));
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