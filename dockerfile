FROM python:latest

COPY src/ /src/
COPY received/ /received/

RUN pip install flask flask-socketio

CMD [ "python", "src/app.py" ]