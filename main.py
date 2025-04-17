import sys
import os
import threading
import time
import webview
from flask import Flask, request, Response
import requests
from wireviz_web import create_app
from wireviz_web.server import wireviz_blueprint

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

graphviz_bin = os.path.join(base_dir, "graphviz_bin")
os.environ["PATH"] = graphviz_bin + os.pathsep + os.environ["PATH"]
os.environ["GRAPHVIZ_DOT"] = os.path.join(graphviz_bin, "dot.exe")

def start_wireviz_web():
    wv_app = create_app()
    wv_app.register_blueprint(wireviz_blueprint)
    print(wv_app.url_map)
    wv_app.run(host='127.0.0.1', port=3005, debug=False)

wireviz_thread = threading.Thread(target=start_wireviz_web)
wireviz_thread.daemon = True
wireviz_thread.start()

app = Flask(__name__)

@app.route('/')
def serve_html():
    with open(os.path.join(base_dir, "index.html"), 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/render', methods=['POST'])
def proxy_render():
    headers = {'Accept': request.headers.get('Accept', 'image/svg+xml')}
    resp = requests.post('http://localhost:3005/render',
                         files={'yml_file': request.files['yml_file']},
                         headers=headers)
    response = Response(resp.content, resp.status_code)
    for key, value in resp.headers.items():
        if key.lower() not in ('content-length', 'transfer-encoding'):
            response.headers[key] = value
    return response

def start_flask():
    app.run(port=8080)

flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()

time.sleep(2)
webview.create_window("WireViz GUI", "http://localhost:8080", width=1200, height=800)
webview.start(debug=False)
