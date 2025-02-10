const socket = io({
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: Infinity,
});

const ping_back_after = 3000; // Delay before ping after server's PONG reponse
var authorization = "";

// Connection debuginfo
socket.on("connect", () => {
    console.log("Socket is connected!");
})

// Deconnection debuginfo
socket.on("disconnect", () => {
    console.log("Socket is disconnected! Attempting to reconnect...");
})

// When server responds after start_debugging
socket.on("started_debugging", (data) => {
    auth = data.authorization;
    console.log("Started debugging, auth", auth);

    socket.emit("ping", {authorization: auth});
})

// Function to sleep in async function
function sleep(time_in_miliseconds) {
    return new Promise((resolve) => setTimeout(resolve, time_in_miliseconds));
}

// When server responds on pinging
socket.on("pong", async (data) => {
    console.log("Server responded! Status:", data.status);

    await sleep(ping_back_after);

    console.log("Now we ping back");
    socket.emit("ping", {authorization: auth});
})

// Start of debugging
document.getElementById("debugStart").addEventListener("click", function start_debugging() {
    document.getElementById("debugCode").readOnly = true;
    document.getElementById("debugStart").disabled = true;

    document.querySelectorAll("#panelGorny button").forEach((btn) => btn.disabled = false);

    socket.emit("start_debugging")
})

// Disabling all debugging buttons
document.querySelectorAll("#panelGorny button").forEach((btn) => btn.disabled = true);
