<!-- 
Instructions: 
- The report (report.md/report.ipynb ) should be in the root of your repository of a project
- The link to the repository have to be shared with us 
- Weekly report can be built in md-file or ipynb file 
- All reports for each week should be written into one file 
- Each week should be in a separated section in the file, see as shown in this file 
- The report should contain subsections TODO / WIP (work in progress) / Done / Issues 
- Each section should contain a list of works and their descriptions 
- Adding pictures / graphs / code inserts to md / ipynb cells can improve your report 
- The deadline is 11.59 pm UTC -12h (anywhere on earth)
 -->
 
 
# Week 1

TODO:
 - I have an idea, to implement a Home Assistant that has an ability to have conversations
 with the user. There is also an idea to implement functionality of reacting to
user's requests and controlling Smart Home devices accordingly.
 - The Smart home devices could be imitated by a file with name of the devices, their type (radiator/light)
and current state (heating/turned off)

 - Below are examples of 
possible scenarios:
   - User wakes up the assistant with a command and tells that he/she is leaving home,
 the assistant checks if there are any lights that are turned on and turns them off. After
 this it asks the user when to expect his/her arrival. After receiving approximate time of
 arrival it sets a timer to turn on the heating/cooling system beforehand.
   - User asks about the weather outside and the assistant gives some basic information, and
 asks if the user wants to have a more detailed information. Upon receiving a confirmation
 intent it acts accordingly and gives more information.
 

WIP:
 - At this point my main goal is creation of intent, response and condition functions
in order to add different functionality for the dialogs. The assistant first needs to
distinguish between intents of user and react to certain key phrases.
   - Creating ideas of scenarios to implement them later in code
   
Done:
 - Started with creation of basic functions
   - In annotators.basic.py I implemented a binary_intent function which helps to determine if user
 confirms or denies, after that it writes the intent inside ctx.misc. Added binary_intent 
 inside annotate function in main.py
   - Created multiple conditions (weather, greeting, appreciation)
   - Extended plot graph in scenario.main.py, added greeting flow and weather flow + 
 simple appreciation
   - Created responses for weather questions that use a helper function. 
 to access Open Weather API to get information about current weather conditions.
   - run_test.py is updated for the added features.
   

Issues:
- After second thought I think that the topic that I chose is not entirely suitable for this idea.
Is there an option to add additional topic (Home Assistant) or should I rethink the theme of the project?
- In the scenario folder there is a label.py file. Which functionality do I need to implement in there?
Couldn't figure it out.
- How do I reset the conversation correctly? For example after getting the info about the weather I want to 
start anew, do I need to create additional flow to implement this?


# Week 2

TODO:
- Create more skills for home assistant that can interact with the home devices and act upon predetermined scenarios
- Create a Q&A chat about home assistant functionality and features:
  - User asks "Can you do ..." and gets information about possible commands to the assistant.

WIP:
- Adding more device types to the Home Assistant config file (radiators, fans)
   
Done:
- Light flow is created
- Added another annotator for the light's skill that determines user intent of either turning on/off the lights.
- light_groups.yaml file is created that stores all the lights grouped up by each room with its current state/brightness.
- Created helper function for light's manipulation in the yaml file that writes the state of the lights into this
file or updating the brightness of the dimmable lights as well.
- Weather request function optimized
- Updated requirements to contain yaml library to work with this file format
- Test file is updated to have new light flow
- Condition functions simplified

Issues:
- After initializing the run_interactive.py it sends multiple requests using OpenWeather API, need to fix this,
because in some cases it results in an error.
- Still have issues with label.py file, need to schedule a 1 on 1 to ask th question about its functionality.


# Week 3
TODO:
- Need to implement a second version of translator
- Still working on Q&A

WIP:
- Implementing a working translator from english to russian and vice versa for multilingual support
   
Done:
- rearranged previous intent annotators by groups, added new ones
- added dimmable light support and climate device support to helper functions
- added config files for climate devices and temperature sensors
- updated run_test.py
- multiple new conditions implemented
- climate_flow and dim_flow added to the plot
- new responses and a little rework on the previous ones

Issues:
- After initializing the run_interactive.py it sends multiple requests using OpenWeather API, need to fix this,
because in some cases it results in an error.
- Could not implement a reliable translator

# Week 4
Done:
- added functionality to automatically reset ctx upon returning to starting node in basic.py
- added home_presence context in basic.py so the bot can distinct between user coming into house and getting away
- changes in helper_functions.home_devices.manipulations:
  - added heat_floor function
  - little changes to existing functions
- weather api_key is now stored as an .env file in the root of the project
- simple_Q&A added to helper_functions
- fixed a bug in translator function (had zero width whitespaces in some translations)
- run_test.py remade to store and compile the dialogues in helper_functions.test_prepare
- translator implemented for russian language
- TTS implemented for home assistant responses in both languages
- added multiple new conditions
- implemented previous_fallback in label.py to have additional functionality (return to the node 
before we went to the fallback node)
- remade scenario.main:
  - added more global transitions to get rid of unnecessary transitions from every end node in each flow
  - added new flow (home_presence)
  - made use of priority labels for transitions between nodes
  - added ability to stop conversation at any time
  - added ability to enable/disable TTS at the start node
- response.py remade:
  - added structure for easy viewing
  - moved some responses into main one
  - added new responses for new features

WIP:
- working on readme.md to add instructions before release