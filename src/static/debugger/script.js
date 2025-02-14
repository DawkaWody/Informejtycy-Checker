const socket = io({
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: Infinity,
});

const ping_back_after = 3000; // Delay before ping after server's PONG reponse
var authorization = "";

// Enable debugging gui and disable pre-debugging gui
async function turn_gui_into_debugging() {
    document.getElementById("debugCode").readOnly = true;
    document.getElementById("debugStart").disabled = true;

    await document.querySelectorAll("#panelGorny button").forEach((btn) => btn.disabled = false);
}

// Disable debugging gui and enable pre-debugging gui
async function turn_gui_back_from_debugging() {
    document.getElementById("debugCode").readOnly = false;
    document.getElementById("debugStart").disabled = false;

    await document.querySelectorAll("#panelGorny button").forEach((btn) => btn.disabled = true);
}

// Function to sleep in async function
function sleep(time_in_miliseconds) {
    return new Promise((resolve) => setTimeout(resolve, time_in_miliseconds));
}

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
    if (data.compilation_error) {
        turn_gui_back_from_debugging();
        document.getElementById("status").textContent = "błąd kompilacji! Przerywanie debugowania!";
    } else {
        turn_gui_into_debugging();
        document.getElementById("status").textContent = "sukces. Rozpoczęto debugowanie!";

        auth = data.authorization;
        console.log("Started debugging, auth:", auth);

        socket.emit("ping", {authorization: auth});
    }
})

// When server responds on pinging
socket.on("pong", async (data) => {
    console.log("Server responded! Status:", data.status);

    await sleep(ping_back_after);

    console.log("Now we ping back");
    socket.emit("ping", {authorization: auth});
})

// Start of debugging
document.getElementById("debugStart").addEventListener("click", function start_debugging() {
    socket.emit("start_debugging", {code: document.getElementById("debugCode").value, input: ""});
})

turn_gui_back_from_debugging()
