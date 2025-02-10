import os
import time
import eventlet
from threading import Thread, Lock
from flask import Flask, request, Response, jsonify, copy_current_request_context, render_template, url_for, make_response, redirect
from flask_socketio import SocketIO, emit
from uuid import uuid4

from server import IP, PORT, RECEIVED_DIR, COMPILED_DIR, DEBUG_DIR, SECRET_KEY, RECEIVE_SUBMISSION_TIME, RECEIVE_DEBUG_PING_TIME, CLEANING_RESULTS_TIME, CLEANING_UNUSED_DBG_PROCESSES_TIME
from code_checking.checker import Checker
from code_checking.check_result import CheckResult, UnauthorizedCheckResult
from code_checking.pack_loader import PackLoader
from code_checking.commands import Compiler
from debugger.debugger import Debugger

app = Flask(__name__, static_url_path="", static_folder="static/", template_folder="templates/")
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app, logger=True, async_mode="eventlet")
connected_socket_ids = set()

# For returning results on http://localhost/status/<auth>
# Server gets the auth given in url and give corresponding CheckResult
results: dict[str: CheckResult] = {}
results_lock = Lock()

# To make sure app.config["debug_processes"] wouldn't be used by two processes in the same time
debug_processes_lock = Lock()

'''
Server functions
'''

# Creates a .cpp source code file from request body.
def make_source_code_file(data: bytes, problem_id: int) -> tuple[str, str]:
	code = data.decode('utf-8')
	auth = str(uuid4())
	file_name = f"{problem_id}_{auth}.cpp"
	with open(os.path.join(RECEIVED_DIR, file_name), 'w') as f:
		f.write(code)
	return file_name, auth

# Prints code result and puts int into the results holding dictionary.
def print_code_result(result: CheckResult, auth: str) -> None:
	with results_lock:
		print(f"Results: {result}")
		results[auth] = (result.as_dict(), time.time())
		print(len(results), "submissions are waiting")

# After RECEIVE_SUBMISSION_TIME seconds clears the result from results holding dictionary.
def clean_results() -> None:
	while True:
		eventlet.sleep(CLEANING_RESULTS_TIME)
		with results_lock:
			for res in dict(results): # dict(...) to make copy
				if time.time() - results[res][1] >= RECEIVE_SUBMISSION_TIME:
					results.pop(res)
					print("Cleaning, left", len(results), "submissions")

# Cleans debug processes from app.config["debug_processes"], if they wasn't pinged for a long time
def clean_unused_debug_processes() -> None:
	while True:
		eventlet.sleep(CLEANING_UNUSED_DBG_PROCESSES_TIME)
		with debug_processes_lock:
			for auth in dict(app.config["debug_processes"]): # dict(...) to make copy
				if time.time() - app.config["debug_processes"][auth].last_ping_time >= RECEIVE_DEBUG_PING_TIME:
					print(f"Debug class with authorization '{auth}' wasn't pinged for {RECEIVE_DEBUG_PING_TIME} seconds")
					print("This class is being cleaned...")
					app.config["debug_processes"][auth].stop()
					app.config["debug_processes"].pop(auth)
					print(f"Cleaned successfully!")

'''
To be executed, after the server has started
'''

# Setups server, after app.run() is called.
with app.app_context():
	pl = PackLoader('../tests', '.test', 'in', 'out', 'CONFIG')
	compiler = Compiler('g++', RECEIVED_DIR, COMPILED_DIR, DEBUG_DIR)
	checker = Checker(compiler, pl, DEBUG_DIR)
	
	lt = Thread(target=checker.listen) # Listens for checker queued elements
	lt.start()
	lt2 = Thread(target=clean_results) # Listens for cleaning results from dictionary, which are on /status/<auth>
	lt2.start()
	lt3 = Thread(target=clean_unused_debug_processes)
	lt3.start()

	# For debugging
	# Server use it to indentify debugging processes
	app.config["debug_processes"]: dict[str: Debugger] = {}

	print(f"Server is running on {IP}:{PORT}")

'''
Flask & SocketIO functions
'''

# Captures code submissions.
@app.route('/submit', methods=["POST"])
def code_submission() -> tuple[str, int]:
	print("POST request for code checking received")

	problem_id = request.headers.get("Problem")
	if not problem_id:
		return "Problem id is missing", 404

	try:
		problem_id = int(problem_id)
	except:
		return "Couldn't convert problem id to integer!", 404
	
	if problem_id >= pl.get_pack_count():
		return "Invalid problem id", 404

	filename, auth = make_source_code_file(request.data, problem_id)
	checker.push_check(filename, problem_id, auth, print_code_result)
	
	return jsonify(
        status="Accepted, wait for results",
		authorization=auth
    ), 202

# Captures demo site request.
@app.route('/', methods=["GET"])
def send_index():
	return render_template("index.html")

# Captures request for submission results.
@app.route('/status/<auth>', methods=["GET"])
def get_task_results(auth: str) -> tuple[str, int]:
	res: tuple[str, int] = results.get(auth, (UnauthorizedCheckResult(), 0))
	if not res[0].unauthorized:
		results.pop(auth)
	return jsonify(res[0].as_dict()), 200

# Captures websocket connection for debugging.
@socketio.on('connect')
def handle_connect() -> None:
	print(f"Client connected: {request.sid}")

# Captures websocket disconnection.
@socketio.on('disconnect')
def handle_disconnect() -> None:
	print(f"Client disconnected: {request.sid}")

@socketio.on('ping')
def handle_debug_ping(data: dict[str: str]) -> None:
	authorization = data["authorization"]
	print(f"Client pinged debugger with authorization: {authorization}")
	if authorization in app.config["debug_processes"]:
		with debug_processes_lock:
			app.config["debug_processes"][authorization].ping()
			emit("pong", {"status": "ok"})
	else:
		emit("pong", {"status": "invalid auth"})

# Captures websocket debugging request.
@socketio.on('start_debugging')
def handle_debugging() -> Response:
	print(f"Client requested debugging: {request.sid}")

	auth = str(uuid4())
	debuger_class = Debugger(compiler, DEBUG_DIR)
	app.config["debug_processes"][auth] = debuger_class

	emit("started_debugging", {"authorization": auth})

# Captures debugging request.
@app.route('/debug', methods=["POST"])
def handle_debugging() -> Response:
	print("POST request for debugging received")

	auth = str(uuid4())

	debuger_class = Debugger(compiler, DEBUG_DIR)
	app.config["debug_processes"][auth] = debuger_class

	return jsonify(
		authorization=auth
	), 202

'''
Running the server
'''

if __name__ == "__main__":
	socketio.run(app, host=IP, port=PORT)
	
