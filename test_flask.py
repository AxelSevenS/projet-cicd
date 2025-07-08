import os
import requests
import time
import subprocess

os.environ['FLASK_DEBUG'] = 'TRUE'

# Start Flask in background
proc = subprocess.Popen(['flask', 'run'])
time.sleep(3)

try:
	response = requests.get('http://localhost:5000')
	assert response.status_code == 200
	print('Health check passed')
finally:
	proc.terminate()