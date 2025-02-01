import os
import time
import eventlet
from threading import Thread, Lock
from flask import Flask, request, Response, jsonify, copy_current_request_context, render_template
from flask_socketio import SocketIO, emit
from uuid import uuid4

from server import IP, PORT, RECEIVED_DIR, COMPILED_DIR, SECRET_KEY, RECEIVE_SUBMISSION_TIME
from code_checking.checker import Checker
from code_checking.check_result import CheckResult, UnauthorizedCheckResult
from code_checking.pack_loader import PackLoader
from code_checking.commands import Compiler

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app, logger=True, async_mode="eventlet")
connected_socket_ids = set()

results: dict[str: CheckResult] = {}
results_lock = Lock()

'''
Server functions
'''

# Creates a .cpp source code file from request body.
def make_source_code_file(data: bytes, problem_id: int) -> tuple[str, str]:
	code = data.decode('utf-8')
	auth = uuid4()
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
		with results_lock:
			for res in dict(results):
				if time.time() - results[res][1] >= RECEIVE_SUBMISSION_TIME:
					results.pop(res)
					print("Cleaning, left", len(results), "submissions")

'''
To be executed, after the server has started
'''

# Setups server, after app.run() is called.
with app.app_context():
	pl = PackLoader('../tests', '.test', 'in', 'out', 'CONFIG')
	compiler = Compiler('g++', RECEIVED_DIR, COMPILED_DIR)
	checker = Checker(compiler, pl)
	
	lt = Thread(target=checker.listen)
	lt.start()
	lt2 = Thread(target=clean_results)
	lt2.start()

'''
Flask & SocketIO functions
'''

# Captures code submissions.
@app.route('/submit', methods=["POST"])
def code_submission() -> Response:
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
	auth = str(auth)
	checker.push_check(filename, problem_id, auth, print_code_result)
	
	return jsonify(
        status="Accepted, wait for results",
		authorization=auth
    ), 202

# Captures demo site request.
@app.route('/', methods=["GET"])
def send_index():
	return render_template("index.html")

# Captures demo site request.
@app.route('/debugger', methods=["GET"])
def send_debugger():
	return render_template("debugger.html")

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

# Captures websocket debugging request.
@socketio.on('start_debugging')
def handle_debugging() -> None:
	print(f"Client requested debugging: {request.sid}")
	

'''
Running the server
'''

if __name__ == "__main__":
	socketio.run(app, host=IP, port=PORT)
	