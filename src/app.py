import os
import time
from threading import Thread, Lock
from flask import Flask, request, Response, jsonify, copy_current_request_context
from flask_socketio import SocketIO, emit
from uuid import uuid4

from server import IP, PORT, RECEIVED_DIR, COMPILED_DIR, SECRET_KEY, RECEIVE_SUBMISSION_TIME
from code_checking.checker import Checker
from code_checking.pack_loader import PackLoader
from code_checking.commands import Compiler

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app, logger=True)
connected_socket_ids = set()

results = {}
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
def print_code_result(result: dict, auth: str) -> None:
	print(f"Results: {result}")
	results[auth] = (dict(result), time.time())
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
def send_index() -> tuple[str, int]:
	c: str = ""
	with open("index.html", "r") as f:
		c = f.read()
	return c, 200

# Captures request for submission results.
@app.route('/status/<auth>', methods=["GET"])
def get_task_results(auth: str) -> tuple[str, int]:
	with results_lock:
		res = results.get(auth, ({"percent": None, "first_failed": None, "time_limit_exceeded": False, "compilation_error": False, "invalid_problem_id": False, "unauthorized": True},0))
		if not res[0]["unauthorized"]:
			results.pop(auth)
		return jsonify(res[0]), 200

# Captures websocket connection for debugging.
@socketio.on('connect')
def handle_connect() -> None:
	print(f"Client connected: {request.sid}")
	connected_socket_ids.add(request.sid)

# Captures websocket connection for debugging.
@socketio.on('disconnect')
def handle_connect() -> None:
	print(f"Client disconnected: {request.sid}")
	connected_socket_ids.discard(request.sid) # If element is not inside connected_socket_ids, discard doesn't throw an error

'''
Running the server
'''

if __name__ == "__main__":
	app.run(host=IP, port=PORT, threaded=True)
	