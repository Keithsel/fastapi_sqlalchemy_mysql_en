# fmt: off
# Listen on internal network port
bind = '0.0.0.0:8001'

# Working directory
chdir = '/fsm/backend/'

# Number of parallel worker processes
workers = 1

# Listen queue size
backlog = 512

# Timeout (seconds)
timeout = 120

# Set daemon process, hand over process to supervisor management;
# If set to True and supervisor logs show:
# gave up: fastapi_server entered FATAL state, too many start retries too quickly
# then set this to False
daemon = False

# Worker mode: coroutine
worker_class = 'uvicorn.workers.UvicornWorker'

# Set maximum concurrency
worker_connections = 2000

# Set process PID file directory
pidfile = '/fsm/gunicorn.pid'

# Set access log and error log paths
accesslog = '/var/log/fastapi_server/gunicorn_access.log'
errorlog = '/var/log/fastapi_server/gunicorn_error.log'

# Set this value to true to record print output to error log
capture_output = True

# Set log level
loglevel = 'debug'

# Python program path
pythonpath = '/usr/local/lib/python3.10/site-packages'

# Start gunicorn with: gunicorn -c gunicorn.conf.py main:app
