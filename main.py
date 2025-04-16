import subprocess
import webview
import time
import os
import threading
from flask import Flask, request, Response
import requests

# Create a Flask app that will act as a proxy
app = Flask(__name__)

# Route to serve the HTML file
@app.route('/')
def serve_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# Proxy route to forward requests to wireviz-web
@app.route('/render', methods=['POST'])
def proxy_render():
    # Extract relevant headers to forward
    headers = {}
    if 'Accept' in request.headers:
        headers['Accept'] = request.headers['Accept']
    else:
        # Set a default Accept header if not provided
        headers['Accept'] = 'image/svg+xml'
    
    # Forward the request to wireviz-web with headers
    resp = requests.post('http://localhost:3005/render', 
                        files={'yml_file': request.files['yml_file']},
                        headers=headers)
    
    # Create a response with the content returned by wireviz-web
    response = Response(resp.content, resp.status_code)
    
    # Copy relevant headers from the wireviz-web response
    for key, value in resp.headers.items():
        if key.lower() not in ('content-length', 'transfer-encoding'):
            response.headers[key] = value
    
    return response

# Function to start the Flask server
def start_flask():
    app.run(port=8080)

# Start wireviz-web as a subprocess
wireviz_process = subprocess.Popen(
    ['wireviz-web'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Start the Flask server in a separate thread
flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()

# Give some time for both servers to start
time.sleep(2)

# Launch the webview with the local interface
webview.create_window("WireViz GUI", "http://localhost:8080", width=1200, height=800)
webview.start(debug=False)

# Stop the wireviz-web server when the app is closed
wireviz_process.terminate()