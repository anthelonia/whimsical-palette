import os
import json
import threading
import webview
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'palette.json')

def load_colors():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_colors(colors):
    with open(DATA_FILE, 'w') as f:
        json.dump(colors, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/colors', methods=['GET', 'POST'])
def colors_api():
    colors = load_colors()
    if request.method == 'POST':
        new_color = request.json
        colors.append(new_color)
        save_colors(colors)
        return jsonify({"status": "success"})
    return jsonify(colors)

@app.route('/api/colors/update', methods=['POST'])
def update_color_api():
    data = request.json
    colors = load_colors()
    for c in colors:
        if c['title'] == data.get('title'):
            c['hex'] = data.get('new_hex')
            c['rgb'] = data.get('new_rgb')
            break
    save_colors(colors)
    return jsonify({"status": "updated"})

def run_server():
    app.run(port=5895, debug=False, use_reloader=False)

if __name__ == '__main__':
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()

    webview.create_window(
        'Whimsical Palette', 
        'http://127.0.0.1:5895',
        width=1100, 
        height=750,
        background_color='#110A1A'
    )
    webview.start()