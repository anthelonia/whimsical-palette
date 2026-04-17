from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'palette.json'

def load_colors():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_colors(colors):
    with open(DATA_FILE, 'w') as f:
        json.dump(colors, f)

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)