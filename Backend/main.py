from flask import Flask, request, jsonify
from flask_cors import CORS
from server import Server

# vytvoření backendu
server = Server()
print(server.nastav_rgb(255, 0, 0))   # červená
print(server.nastav_rgb(0, 255, 0))   # zelená
print(server.nastav_rgb(0, 0, 255))   # modrá

print(server.posli_prikaz("LIGHT"))   # test čidla

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


@app.route('/api/led-status', methods=['GET'])
def led_status():
    return jsonify({
        "status": server.ziskej_svetlo_status()
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

    result = server.nastav_rgb(
        data.get('r', 0),
        data.get('g', 0),
        data.get('b', 0)
    )

    return jsonify(result)


@app.route('/api/temp', methods=['GET'])
def temp():
    teplota = server.ziskej_teplotu()

    if teplota is None:
        return jsonify({
            "status": "error",
            "message": "Nepodařilo se přečíst intenzitu světla"
        }), 500

    return jsonify({
        "status": "ok",
        "temp": teplota
    })


@app.route('/api/light', methods=['GET'])
def light():
    svetlo = server.ziskej_svetlo()

    if svetlo is None:
        return jsonify({
            "status": "error",
            "message": "Nepodařilo se přečíst intenzitu světla"
        }), 500

    return jsonify({
        "status": "ok",
        "light": svetlo
    })

from flask import request, jsonify

from flask import request, jsonify

@app.route('/api/threshold', methods=['POST'])
def threshold():
    data = request.get_json()

    if data is None:
        return jsonify({
            "status": "error",
            "message": "Nebyl poslán žádný JSON"
        }), 400

    threshold_value = data.get("threshold")

    if threshold_value is None:
        return jsonify({
            "status": "error",
            "message": "Chybí hodnota threshold"
        }), 400

    print(threshold_value)

    try:
        server.set_threshold(threshold_value)

        return jsonify({
            "status": "ok",
            "threshold": threshold_value
        })

    except Exception as e:
        print("Neco nefunguje s thresholdem:", e)

        return jsonify({
            "status": "error",
            "message": "Nepodařilo se nastavit threshold"
        }), 500

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
