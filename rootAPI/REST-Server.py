import cv2
import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
from katy_mainControl import global_controller as gc

app = Flask(__name__)
CORS(app) 


def exit():
    print('\nexiting program ', time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()))
    cv2.destroyAllWindows()

# Funktionen für die verschiedenen Befehle
def test(times):
    start()
    for x in range(times):
        print(x)

def start(zielID=0):
    #hier Katy functionality einbinden.
    #zum testen mal blinken:
    # script_path = '../luwiBlaulicht/blaulicht.py'
    # blaulicht = subprocess.Popen(['python3', script_path])
    # time.sleep(5)
    # blaulicht.terminate()
    # blaulicht.wait()
    gc.start()


# REST-Endpunkte für die verschiedenen Befehle
@app.route('/test', methods=['POST'])
def api_test():
    times = request.get_json().get('times')
    print("TEST: ", times)
    test(times)
    return jsonify({'result': 'success'})

@app.route('/start', methods=['POST'])
def api_start():
    zielID = request.get_json().get('id')
    print("START\nID: ", zielID)
    start(zielID)
    return jsonify({'result': 'success'})

@app.route('/exit', methods=['POST'])
def api_exit():
    exit()
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5500, threaded=True)
