![blueberry.svg](static/assets/blueberry.svg)

# Hello, Blueberry!

**Blueberry** is designed to be a virtual assistant, capable of doing the usual virtual assistant tasks, and more. 🫐

### Working Demo
https://github.com/BillyDoesDev/blueberry/assets/64155209/46efa0be-6d0b-4efb-b074-d6e671a4d8cd

> **Stuff to Note:**
> - The "creative mode" feature is still in development, and as a result, is highly unstable.
> - Adding on to the above, a view dependencies **may require additional tools on `windows` for its proper functioning.** Thus, consult the error logs for the same. An updated `requirements.txt` file will be released later on.
> - Fortunately, all the build tools exist by default on most Linux distros.
> - **THE SRS DOCUMENTATION FOR THE PROJECT IS IN THE `docs/` DIRECTORY.**



### Approach
The entire thing is designed to work on a client-server model. All the processing of the audio is done on a python backend, and the results and also the overall GUI interface is a web based one.

**This works through a series of stages:**
- **Stage 1:** Audio data is processed in real time `on the client side`, suing the [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API).
- **Stage 2:** The transcribed text data is then parsed for the `wake-word` and on detection, is stremed to the `python server` in real time, for further processing using websockets.
- **Stage 3:** Our backend analyses the text and triggers an appropriate function accordingly. (This could be a web search, weather information lookup, etc.)
- **Stage 4:** The result of the function is emitted to the client in real time.
- ~**Stage 5:** An audio output is generated on the frontend using the [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API).~

![blueberry.png](static/assets/workflow.png)


### Setup Instructions

**Dependencies:**
- `python 3.11.*`
- `git`
- A chromium based browser.
- The `HUGGINGFACEHUB_API_TOKEN` environment variable in your system PATH.

Clone the repository and `cd` into the appropriate directory

**Unix:**
```shell
git clone https://github.com/aisoc-internal-hackathon/aisoc_T9.git
cd aisoc_T9

# activate python virtual env and install dependencies
python -m venv env
source env/bin/activate

# run server and follow the generated URL to get to the frontend.
python server.py
```

**Windows:**

> **NOTE:** There have been multiple issues with installing the appropriate dependencies on windows natively, so it is recommended to set it up in a WSL environment.

**Start WSL:**</br>
*Instructions on how to set up WSL can be found [here](https://learn.microsoft.com/en-us/windows/wsl/install).*
```shell
wsl
```
Follow the rest of the steps as usual as it is described above for Unix machines.

### Disclaimer
> The above implementation is cross-platform, thanks to the fact that it relies on a browser based frontend. That being said, however, the **[Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) is currently only supported in chromium based browsers**, and this project, as a result, is heavily experimental. Expect minor glitches.</br></br>
>```shell
>#Logs for nerds: [Development Environment]
>$ python --version
>Python 3.11.5
>```
>```shell
>$ uname -a    
>Linux billy 6.6.10-arch1-1 #1 SMP PREEMPT_DYNAMIC Fri, 05 Jan 2024 16:20:41 +0000 x86_64 GNU/Linux
>```


### License and Open Source Information

>Blueberry - your personalized AI assistant.</br>
Copyright (C) 2024  BillyDoesDev</br>
Email: DarkKnight450@protonmail.com</br></br>
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the , or (at your option) any later version.</br></br>
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.</br></br>
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

[![blueberry.svg](static/assets/gpl-logo.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)
