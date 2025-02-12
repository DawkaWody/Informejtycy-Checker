async function submission() {
    console.log(document.getElementById("inputCode").value);
    const response = await fetch("/checker/submit", {
            method: "POST",
            headers: {
                "content-type": "text/plain",
                "Problem": "0"
            },
            body: document.getElementById("inputCode").value
    });
    const data = response.json();
    console.log(data);
}

document.getElementById("submissionButton").addEventListener("click", () => {
    submission();
});
