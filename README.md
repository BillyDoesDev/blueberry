# 'Sup, Bartowski!

**Bartowski** */bAr-tow-ski/* is designed to be a virtual assistant, capable of doing the usual virtual assistant tasks, and more.


### Approach
The entire thing is designed to work on a client-server model. All the processing of the audio is done on a python backend, and the results and also the overall GUI interface is a web based one.

This works through a series of stages:
- **Stage 1:** Audio data is streamed in real time from the client to the server using websockets.
- **Stage 2:** Audio data is processed by a Speech-to-Text library/framework, to get the relevant data in text form.
- **Stage 3:** Our custom AI model analyses the text and triggers an appropriate function accordingly. (This could be a web search, weather information lookup, etc.)
- **Stage 4:** The result of the function is converted to audio using a Text-to-Speech library/framework.
- **Stage 5:** The audio is emitted to the client in real time again, using websockets. 


### Setup and Implementation details
> Everything here is subject to change.

Clone the repository and `cd` into the appropriate directory
```shell
git clone https://github.com/aisoc-internal-hackathon/aisoc_T9.git
cd aisoc_T9
```

Set up a virtual python environment and install required dependencies
```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Start the backend server using `python server.py` and follow the generated URL to get to the frontend.

> ***NOTE:*** 
> - The current implementation uses a `Flask` server as the backend, using websockets for real time inteactions. There is the possibility of switching over to `aiohttp` later on, in case of increased complexities.
> - The current implementation uses **CMUSphinx** for offline speech to text. This might require the installation of the [pocketsphinx](https://cmusphinx.github.io/wiki/download/) packagae.
> - There is the option to switch over to [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/v2/docs/streaming-recognize). (More references [here](https://github.com/saharmor/realtime-transcription-playground/blob/main/backend/demo_web_app.py)) However, this runs the drawback of having the need to always be online.
>> **Supported audio file types when using SpeechRecognition along with pocketsphinx are, as of now:**
>> - WAV: must be in PCM/LPCM format
>> - AIFF
>> - AIFF-C
>> - FLAC: must be native FLAC format; OGG-FLAC is not supported
>> </br></br> If you are working on x-86 based Linux, macOS or Windows, you should be able to work with FLAC files without a problem. On other platforms, you will need to install a FLAC encoder and ensure you have access to the flac command line tool. You can find more information [here](https://xiph.org/flac/) if this applies to you.
