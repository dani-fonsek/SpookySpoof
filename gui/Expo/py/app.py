from flask import Flask, jsonify, send_from_directory, request 
import subprocess
import json
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

app = Flask(__name__, static_folder=ROOT_DIR, template_folder=ROOT_DIR)

@app.route('/')
def index():
    return send_from_directory(ROOT_DIR, 'main.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(ROOT_DIR, filename)

@app.route('/data')
def get_data():
    json_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '/home/user/Desktop/SpookySpoof/flowgen/datos.json')
    with open(json_path, 'r') as f:
        datos = json.load(f)
    return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/contener', methods=['POST'])
def contener_trafico():
    data = request.get_json()
    mac = data.get('mac')
    if not mac:
        return jsonify({"error": "MAC no proporcionada"}), 400

    try:
        resultado = subprocess.run(
            ['python', 'SpookyQuarentineMAC.py', mac],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True
        )
        return jsonify({
            "stdout": resultado.stdout,
            "stderr": resultado.stderr,
            "code": resultado.returncode
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
