from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import requests
import json
import os
import shutil
from static.assets.scripts import source_text

# print(source_text.parse_source_file("uploads/climate.txt", "what is climate change"))

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # print(request.files)
        # Check if the POST request has the file part
        if "file" not in request.files:
            return render_template("index.html", message="No file part")
        # print(request.files)
        file = request.files["file"]

        # If the user does not select a file, browser submits an empty file
        if file.filename == "":
            return render_template("index.html", message="No selected file")

        # If the file is present and has an allowed extension, save it
        if file:
            print("******************DOWNLOADED***********************")
            # You can customize the upload path as needed

            # if str(file.filename).split(".")[1] != "txt":
            #     return render_template("index.html", confirmation_message="accept only .txt files")

            try:
                shutil.rmtree("uploads")
            except FileNotFoundError: pass

            os.mkdir("uploads")

            file.save("uploads/" + file.filename)
            message = "File successfully uploaded: " + file.filename

            print(message)

            # generated_text = source_text.parse_source_file(f"uploads/{file.filename}", "what is climate change")
            socketio.emit("ass-response", {"current_condition": 0})

            print(">>>>>>>>>>>>>>>>>>>>>>>>>         I'm here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return render_template("index.html", confirmation_message=f"{file.filename} was successfully uploaded.")

    return render_template("index.html", message=None)


@socketio.on("activee")
def handle_my_custom_event(json):
    print("received json: " + str(json))


# @app.route('/alarms')
# def alarms():
#     @after_this_request
#     def add_header(response):
#         response.headers['Access-Control-Allow-Origin'] = '*'
#         return response

#     with open("data/alarms.json", mode="r") as f:
#         data = json.load(f)
#         return data


@socketio.on("weather-request")
def fetch_weather(json_data):
    print(f"recieved: {json_data}")
    phrase = str(json_data["data"]).strip()
    if phrase.endswith("weather"):
        location = phrase.split(" ")[0]
    else:
        location = phrase.split(" ")[-1]

    try:
        r = requests.get(f"http://wttr.in/{location}", params={"format": "j1"})
        emit("weather-response", json.loads(r.text))
        print(r.url, r.text)
    except requests.exceptions.ConnectionError:
        emit("weather-response", {"current_condition": 0})
        print("server fault :/")


@socketio.on("alarm-set")
def alarm_set(json_data):
    print(f"recieved: {json_data}")
    phrase = str(json_data["data"]).strip()  # set an alarm for 5:04 p.m.

    hourNminute = __import__("re").search("\d+:\d+", phrase).group()
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
            emit("alarm-response", alarm_data)


@socketio.on("alarm-modify")  # this is for removing the alarm that finished ringing
def alarm_modify(json_data):
    print(f"recieved: {json_data}")  # {'data': '8:21:00 PM'}
    current_alarmaaaa = json_data["data"]

    with open("data/alarms.json", mode="r") as f:
        alarm_data = json.load(f)

    with open("data/alarms.json", mode="w") as f:
        current_alarms = alarm_data["alarms"]
        current_alarms.remove(current_alarmaaaa)
        alarm_data["alarms"] = current_alarms
        json.dump(alarm_data, f, indent=4)
        emit("alarm-response", alarm_data)



@socketio.on("creative-query")
def creative_parse(json_data):
    print(f"recieved: {json_data}")
    phrase = str(json_data["data"]).strip()

    generated_text = source_text.parse_source_file(f"uploads/{os.listdir('uploads')[0]}", phrase)
    emit('creative-response', {"response": generated_text})


if __name__ == "__main__":
    socketio.run(app, debug=True)
