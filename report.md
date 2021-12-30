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
....

# Week 3
....

# Week 4
....
