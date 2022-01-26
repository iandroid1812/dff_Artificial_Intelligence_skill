# dff_Artificial_Intelligence_skill

## Description
This skill is made as a demo for a configurable home assistant dialogs between user and his smart home devices.
It has multilingual support (english/russian).


## Project structure

- **annotators:** Has 2 files `basic.py` and `main.py`. In `basic.py` we have functions that fill up our ctx.misc dictionary 
with useful information (current language, tts status, user intents like agreeing or denying, the current room, etc.).
I also added a function to store the translation of last user request in the ctx as well, which speeds up the process,
because it needs to translate the request only once. The `main.py` calls each function in `basic.py` to create a full
context before proceeding to condition checking.


- **helper_functions:** `translator_tts.py` is used to translate user requests and bot response as well as making it 
possible to use Google text to speach service for audio responses. `home_devices_manipulations.py` makes it possible to 
interact (control lights, check for dimmable lamps, control the temperature) with the mock config files for smart home 
devices stored in `home_devices` folder. `requesting.py` gets us weather information using Open Weather API.
`simple_Q_A.py` adds a functionality of a basic q&a feature. `test_prepare.py` has all the dialogues that are used for
testing function, but it prepares them by adding weather forecast using fstrings and sends compiled tuple to `run_test.py`


- **scenario:** `main.py` has plot creation with different dialog flows and rules, as well as actor class creation.
`condition.py` has everything to check for conditions and has functions returning boolean values that are imported 
as loc_cnd in `main.py`. `response.py` returns home assistant response as a string as well as calling for translation
and tts inside each response function, in some of the response functions we also make calls to helper functions in order
to control home devices, get weather report. `label.py` has 1 custom label which helps us to reach the node that was the
last one before encountering the error, thus resuming the progress from where we left off.


## Basic instructions
1. In order to start the bot, launch interactive mode in the terminal.
2. Commands are sent by typing in request from the keyboard.
3. To turn off TTS type in "Disable TTS", "Turn off tts", "Выключить ттс"; you can turn it back on with similar commands.
4. To stop the conversation at any point of time type "stop" in either language.
5. To change the language type in required language when you are at the starting node, for example: at the start of
conversation, when you see "waiting for commands...".
6. You can thank the bot or say bye, after the command is executed, the bot will respond and return to the starting node
clearing the context in the process.

## Examples of commands:
###
### I want to ask you a questions.
Launches a brief q&a about basic commands for home assistant. 
You can ask: **"How do I change the language?"**, **"What can you do?"** or **"How to disable TTS?"**.

### Hey, what is the weather?
Tells you a weather report for a configured location (your house) and asks 
if you want to get a more detailed forecast as well.

### Turn on the light in the kitchen.

### Dim the lights.
Asks the room that the user wants to dim the light in (mock files only have dimmable light in the bedroom)
if the wrong room is provided it keeps asking till it gets the correct one. After that asks for a brightness level.

### I am going away.
Checks for a weather report, if it is raining/snowing it warns the user about it. Additional question is
asked by the assistant if anyone else is still at home. If the response is negative, the assistant proceeds to ask
if user wants to check the lights and turns it off automatically upon receiving positive confirmation.

### Cool down the hallway.
Checks the current temperature in the room using sensors in config file, and sets climate devices in this room 
to (current temperature - 10 degrees) so it can cool down. Works similarly for "heat up" functionality as well.

### Set the temperature to 25 degrees in the living room.

### I am coming home.
Checks for a weather report, if there were precipitations offers the user to heat up the hallway before 
the arrival, so the clothes/boots/umbrella will dry much faster upon arrival.

## Quickstart
```bash
pip install -r requirements.txt
```
Run interactive mode
```bash
python run_interactive.py
```
Run tests
```bash
python run_test.py
```
## Resources

* Execution time: 0.22 sec on average based on test dialogues
* Starting time: 4.56 sec
* RAM: 100 MB