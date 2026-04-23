from flask import Flask, request, jsonify
from flask_cors import CORS
from server import Server

# vytvoření backendu
server = Server()

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return jsonify({
        "status": "running",
        **server.stav()
    })


@app.route('/api/mode', methods=['POST'])
def mode():
    return jsonify({
        "automatic_mode_on": server.prepni_rezim()
    })


@app.route('/api/led/on', methods=['POST'])
def led_on():
    if server.automatic_mode_on:
        return jsonify({"error": "AUTO MODE zapnutý"}), 403

    return jsonify({
        "response": server.posli_prikaz('1')
    })


@app.route('/api/led/off', methods=['POST'])
def led_off():
    if server.automatic_mode_on:
        return jsonify({"error": "AUTO MODE zapnutý"}), 403

    return jsonify({
        "response": server.posli_prikaz('0')
    })


@app.route('/api/rgb', methods=['POST'])
def rgb():
    if server.automatic_mode_on:
        return jsonify({"error": "AUTO MODE zapnutý"}), 403

    data = request.json
    if not data:
        return jsonify({"error": "Chybí JSON"}), 400

    try:
        r = max(0, min(255, int(data.get('r', 0))))
        g = max(0, min(255, int(data.get('g', 0))))
        b = max(0, min(255, int(data.get('b', 0))))
    except:
        return jsonify({"error": "Špatné hodnoty"}), 400

    cmd = f"RGB {r} {g} {b}"

    return jsonify({
        "rgb": [r, g, b],
        "response": server.posli_prikaz(cmd)
    })


@app.route('/api/temp')
def temp():
    odpoved = server.posli_prikaz('TEMP')

    if odpoved.startswith('TEMP:'):
        return jsonify({
            "temperature": float(odpoved[5:])
        })

    return jsonify({"error": odpoved}), 500


@app.route('/api/command', methods=['POST'])
def command():
    data = request.json
    if not data or 'cmd' not in data:
        return jsonify({"error": "Chybí cmd"}), 400

    return jsonify({
        "response": server.posli_prikaz(data['cmd'])
    })


if __name__ == '__main__':
    print("Server běží na http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)