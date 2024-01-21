from flask import Flask, render_template, after_this_request
from flask_socketio import SocketIO, emit
import requests
import json

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('activee')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


# @app.route('/alarms')
# def alarms():
#     @after_this_request
#     def add_header(response):
#         response.headers['Access-Control-Allow-Origin'] = '*'
#         return response
    
#     with open("data/alarms.json", mode="r") as f:
#         data = json.load(f)
#         return data


@socketio.on('weather-request')
def fetch_weather(json_data):
    print(f"recieved: {json_data}")
    phrase = str(json_data["data"]).strip()
    if phrase.endswith("weather"):
        location = phrase.split(" ")[0]
    else:
        location = phrase.split(" ")[-1]
    
    try:
        r = requests.get(f"http://wttr.in/{location}", params={"format": "j1"})
        emit('weather-response', json.loads(r.text))
        print(r. url, r.text)
    except requests.exceptions.ConnectionError:
        emit('weather-response', {"current_condition": 0})
        print("server fault :/")


@socketio.on('alarm-set')
def alarm_set(json_data):
    print(f"recieved: {json_data}")
    phrase = str(json_data["data"]).strip() # set an alarm for 5:04 p.m.

    hourNminute = __import__('re').search('\d+:\d+', phrase).group()
    time_string = f"{hourNminute}:00 {'PM' if 'p.m.' in phrase else 'AM'}"
    print(time_string)
    
    with open("data/alarms.json", mode="r") as f:
        alarm_data = json.load(f)
    
    with open("data/alarms.json", mode="w") as f:
        current_alarms = alarm_data["alarms"]
        if time_string not in current_alarms:
            current_alarms.append(time_string)
            alarm_data["alarms"] = current_alarms        
            json.dump(alarm_data, f, indent=4)
            emit('alarm-response', alarm_data)
    

@socketio.on('alarm-modify') # this is for removing the alarm that finished ringing
def alarm_modify(json_data):
    print(f"recieved: {json_data}") # {'data': '8:21:00 PM'}
    current_alarmaaaa = json_data['data']

    with open("data/alarms.json", mode="r") as f:
        alarm_data = json.load(f)
    
    with open("data/alarms.json", mode="w") as f:
        current_alarms = alarm_data["alarms"]
        current_alarms.remove(current_alarmaaaa)
        alarm_data["alarms"] = current_alarms
        json.dump(alarm_data, f, indent=4)
        emit('alarm-response', alarm_data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
