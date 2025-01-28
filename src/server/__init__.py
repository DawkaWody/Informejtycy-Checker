# This file must be inside /server dictionary,
# otherwise python runned in docker raises an error.

IP: str = "127.0.0.1"
PORT: int = 5000
RECEIVED_DIR: str = "../received"
COMPILED_DIR: str = "../received/compiled"
SECRET_KEY: str = "gEe_5+aBG6;{4#X[bK^]k!w,mCLU-Mr"
RECEIVE_SUBMISSION_TIME: int = 10