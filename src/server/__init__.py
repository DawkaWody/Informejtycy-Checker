# This file must be inside /server dictionary,
# otherwise python runned in docker raises an error.

IP: str = "0.0.0.0"
PORT: int = 5000
RECEIVED_DIR: str = "../received"
COMPILED_DIR: str = "../received/compiled"
SECRET_KEY: str = "gEe_5+aBG6;{4#X[bK^]k!w,mCLU-Mr" # Secret key used by flask_socketio for security
RECEIVE_SUBMISSION_TIME: int = 10 # How much results stay on status/<auth>
RECEIVE_DEBUG_PING_TIME: int = 15 # After what time will not pinged Debugger class be deleted
CLEANING_RESULTS_TIME: int = 3 # How often results from status/<auth> should be checked for possible cleaning
CLEANING_UNUSED_DBG_PROCESSES_TIME: int = 5 # How often should Debugger classes be checked for possible cleaning
DOCKER_CPU_LIMIT: float = 1.5 # Amount of cores per container