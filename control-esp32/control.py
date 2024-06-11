from flask import Flask, render_template, request, redirect, url_for, flash
import paho.mqtt.client as mqtt
import json
import os

NODES = ['node1', 'node2', 'node3']  # Lista de nodos

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY2"]

# Obtener las variables de entorno para la conexión MQTT
SERVIDOR = os.environ["SERVIDOR"]
PUERTO_MQTTS = int(os.environ["PUERTO_MQTTS"])
MQTT_USR = os.environ["MQTT_USR"]
MQTT_PASS = os.environ["MQTT_PASS"]

# Configurar el cliente MQTT
mqtt_client = mqtt.Client("cliente-web")
mqtt_client.tls_set()  # Configura TLS si es necesario
mqtt_client.username_pw_set(MQTT_USR, MQTT_PASS)
mqtt_client.connect(SERVIDOR, PUERTO_MQTTS, 60)

@app.route('/')
def index():
    return render_template('index.html', nodes=NODES)

@app.route('/send_command', methods=['POST'])
def send_command():
    node = request.form['node']
    command = request.form['command']
    value = request.form.get('value', '')

    if command == 'setpoint':
        payload = json.dumps({"setpoint": int(value)})
        topic = f"{node}/setpoint"
    elif command == 'destello':
        payload = json.dumps({"action": "destello"})
        topic = f"{node}/destello"
    else:
        flash('Comando no válido', 'error')
        return redirect(url_for('index'))

    mqtt_client.publish(topic, payload)
    flash(f'Comando {command} enviado al nodo {node}', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)

