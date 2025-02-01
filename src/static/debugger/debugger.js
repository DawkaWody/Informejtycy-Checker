const socket = io();

document.getElementById("submissionButton").addEventListener("click", function submission() {
	socket.emit("start_debugging")
});