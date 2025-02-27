import os
import time
import eventlet
import sys
from threading import Thread, Lock
from flask import Flask, request, Response, jsonify, copy_current_request_context, render_template, url_for, make_response, redirect
from flask_socketio import SocketIO, emit
from uuid import uuid4

from server import IP, PORT, RECEIVED_DIR, COMPILED_DIR, SECRET_KEY, RECEIVE_SUBMISSION_TIME, RECEIVE_DEBUG_PING_TIME, CLEANING_RESULTS_TIME, CLEANING_UNUSED_DBG_PROCESSES_TIME
from code_checking.checker import Checker
from code_checking.check_result import CheckResult, UnauthorizedCheckResult
from code_checking.pack_loader import PackLoader
from code_checking.commands import Compiler
from logger import Logger
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app, async_mode="eventlet")
CORS(app)

# To nicely display messages
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
logger = Logger(display_logs=True)

# Make sure received directory exists
os.makedirs(RECEIVED_DIR, exist_ok=True)
os.makedirs(COMPILED_DIR, exist_ok=True)

results: dict[str: tuple[str, int]] = {}
results_lock = Lock()

'''
Server functions
'''

# Creates a .cpp source code file from request body.
def make_cpp_file_for_checker(data: bytes, problem_id: int) -> tuple[str, str]:
	code = data.decode('utf-8')
	auth = str(uuid4())
	file_name = f"{problem_id}_{auth}.cpp"
	with open(os.path.join(RECEIVED_DIR, file_name), 'w') as f:
		f.write(code)
	return file_name, auth

# Prints code result and puts int into the results holding dictionary.
def print_code_result(result: CheckResult, auth: str) -> None:
	with results_lock:
		results[auth] = (result.as_dict(), time.time())

		logger.spam(f"Results: {result}", print_code_result)
		logger.spam(f"{len(results)} submissions are waiting", print_code_result)

# After RECEIVE_SUBMISSION_TIME seconds clears the result from results holding dictionary.
def clean_results() -> None:
	global results
	while True:
		eventlet.sleep(CLEANING_RESULTS_TIME)
		with results_lock:
			for res in dict(results): # dict(...) to make copy
				if time.time() - results[res][1] >= RECEIVE_SUBMISSION_TIME:
					results.pop(res)
					logger.spam(f"Cleaning, left {len(results)} submissions", clean_results)

'''
To be executed, after the server has started
'''

# For logger, in case something is logged outside of function scope
def main() -> None:
	pass

# Setups server, after app.run() is called.
with app.app_context():
	pl = PackLoader(logger, '../tests', '.test', 'in', 'out', 'CONFIG')
	compiler = Compiler(logger, 'g++', RECEIVED_DIR, COMPILED_DIR)
	checker = Checker(logger, compiler, pl)
	
	logger.debug("Starting cleaning processes", main)

	lt = Thread(target=checker.listen) # Listens for checker queued elements
	lt.start()
	lt2 = Thread(target=clean_results) # Listens for cleaning results from dictionary, which are on /status/<auth>
	lt2.start()

	logger.debug(f"Cleaning processes have started", main)

	logger.info(f"Server is running on {IP}:{PORT}", main)

'''
Flask & SocketIO functions
'''

# Captures code submissions.
@app.route('/checker/submit', methods=["POST"])
def code_submission() -> tuple[str, int]:
	logger.debug("POST request for code checking received", code_submission)

	problem_id = request.headers.get("Problem")
	if not problem_id:
		return "Problem id is missing", 404

	try:
		problem_id = int(problem_id)
	except:
		return "Couldn't convert problem id to integer!", 404
	
	if problem_id >= pl.get_pack_count():
		return "Invalid problem id", 404

	filename, auth = make_cpp_file_for_checker(request.data, problem_id)
	checker.push_check(filename, problem_id, auth, print_code_result)
	
	return jsonify(
        status="Accepted, wait for results",
		authorization=auth
    ), 202

# Captures request for submission results.
@app.route('/checker/status/<auth>', methods=["GET"])
def get_task_results(auth: str) -> tuple[str, int]:
	res: tuple[str, int] = results.get(auth, (UnauthorizedCheckResult().as_dict(), 0))
	if not res[0]["unauthorized"]:
		results.pop(auth)
	return jsonify(res[0]), 200
	
'''
Running the server
'''

if __name__ == "__main__":
	socketio.run(app, host=IP, port=PORT)