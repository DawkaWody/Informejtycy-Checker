const socket = io();

socket.on("started_debugging", (auth) => {
	console.log(auth);
})

document.getElementById("submissionButton").addEventListener("click", function submission() {
	socket.emit("start_debugging")
});
