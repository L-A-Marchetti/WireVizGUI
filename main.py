import subprocess
import webview
import time
import os
import threading
from flask import Flask, request, Response
import requests

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))


# Configurer le chemin GraphViz et les variables d'environnement
graphviz_bin = os.path.join(base_dir, "graphviz_bin")
os.environ["PATH"] = graphviz_bin + os.pathsep + os.environ["PATH"]
# Importante pour wireviz - indique explicitement où trouver dot.exe
os.environ["GRAPHVIZ_DOT"] = os.path.join(graphviz_bin, "dot.exe")

wireviz_web_exe = os.path.join(base_dir, "wireviz-web.exe")

# Create a Flask app that will act as a proxy
app = Flask(__name__)

# Route to serve the HTML file
@app.route('/')
def serve_html():
    with open(os.path.join(base_dir, "index.html"), 'r', encoding='utf-8') as f:
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