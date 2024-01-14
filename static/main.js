// set up websockets
const socket = io();
socket.on('connect', function () {
    console.log("connecttion to websocket successful")
    socket.emit('activee', { data: 'I\'m connected!' });
});

// set up speech recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.lang = "en-US";
recognition.interimResults = false;
recognition.continuous = true;
recognition.maxAlternatives = 0;

recognition.start();

// make sure it is always active
setInterval(function () {
    try {
        recognition.start();
    } catch (error) { }
}, 1000);


let wake_word_encountered = false;
const input_field = document.querySelector(".input-field");

recognition.onresult = (event) => {
    const phrase = event.results[event.results.length - 1][0].transcript.toString().toLowerCase();

    if (wake_word_encountered) {

        const CONTAINER = document.querySelector(".container");

        // input_field.classList.toggle("active");
        input_field.textContent = phrase;
        // process the instruction here

        if (phrase.includes('weather')) {
            socket.emit('weather-request', { data: phrase });
            socket.on('weather-response', (data) => {

                if (data.current_condition == 0) {
                    input_field.classList.remove("active");
                    input_field.textContent = "sorry, our server seems to be busy :/";
                } else {
                    let feels_like = data.current_condition[0].FeelsLikeC + '°C';
                    let temp = data.current_condition[0].temp_C + '°C';
                    let humidity = data.current_condition[0].humidity + '%';
                    let precipitation = data.current_condition[0].precipMM + ' mm';
                    let visibility = data.current_condition[0].visibility + ' km';

                    let wdirection = data.current_condition[0].winddir16Point;
                    let wdegree = data.current_condition[0].winddirDegree + '°';
                    let wspeed = data.current_condition[0].windspeedKmph + ' km/h';

                    let wind = `${wspeed} from ${wdegree} ${wdirection}`
                    let description = data.current_condition[0].weatherDesc[0].value;

                    let areaName = data.nearest_area[0].areaName[0].value;
                    let region = data.nearest_area[0].region[0].value;
                    let country = data.nearest_area[0].country[0].value;

                    // let date1 = data.weather[1].date.split('-').splice(1, ).join('-');
                    // let temp1 = data.weather[1].avgtempC + '°C';
                    // let date2 = data.weather[2].date.split('-').splice(1, ).join('-');
                    // let temp2 = data.weather[2].avgtempC + '°C';

                    document.querySelector(".areaName").textContent = areaName;
                    document.querySelector(".region").textContent = region;
                    document.querySelector(".country").textContent = country;
                    document.querySelector(".desc").textContent = description;
                    document.querySelector(".temp").textContent = temp;
                    document.querySelector(".feelslike").textContent = feels_like;
                    document.querySelector(".precipitation").textContent = precipitation;
                    document.querySelector(".humidity").textContent = humidity;
                    document.querySelector(".visibility").textContent = visibility;
                    document.querySelector(".wind").textContent = wind;

                    CONTAINER.classList.toggle("invisible")
                    input_field.classList.remove("active");
                    input_field.textContent = "say 'Blueberry'!";
                }
            })
        }

        else if (phrase.includes('alarm')) {
            socket.emit('alarm-set', { data: phrase });
            input_field.classList.remove("active");
            input_field.textContent = "ALarm Set!";

            // let CURRENT_ALARMS = [];
            // fetch("http://localhost:5000/alarms")
            //     .then(response => response.json())
            //     .then(alarm_data => {
            //         CURRENT_ALARMS = alarm_data.alarms;
            //     })
            socket.on('alarm-response', (data) => {
                CURRENT_ALARMS = data.alarms;
                console.log(data);
            });
        }

        else {
            // default case
            input_field.classList.remove("active");
            input_field.textContent = "sorry, didn't get ya :/";
        }

        wake_word_encountered = false;
    }


    if (phrase.includes('blueberry')) {
        console.log(">>> HIT <<<");
        wake_word_encountered = true;
        input_field.classList.add("active");
        input_field.textContent = "listening...";
    }
};

// recognition.onspeechend = async () => {
//     console.log("Speech has stopped being detected...");

//     // console.log("recieved so far: " + instruction);

//     await new Promise(r => setTimeout(r, 2000));
//     console.log("restarting...");
//     recognition.start();
// };