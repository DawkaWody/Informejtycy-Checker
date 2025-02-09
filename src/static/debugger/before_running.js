async function debug_submission() {
	const response = await fetch("/debug", {
		method: "POST",
		headers: {
			"content-type": "text/plain"
		},
		body: document.getElementById("debugCode").value
	});
	const data = await response.json();
	// data.where is location to redirect
	// data.authorization should be passed as iframe parameter
	// or just given to that page
	console.log(data.authorization);
};

document.getElementById("submissionButton").addEventListener("click", () => {
	debug_submission();
});
