It is a communication framework with a set of conventions and a build system that runs on top of Linux for building robots using a pub sub mechanism. 
# Terminology 
1. **Node**: A specialist script for each part of the robot.
2. **Topics**: How they communicate (concept of pub sub). 
3. **Services**: The requests and responses.
4. **Actions**: Long running requests with progress updates.

## Nodes
Nodes describes the core functionalities of the part of the robot. For instance a node for a toy car it can have a node for the motor, to control the speed and acceleration of the car (torque). Therefore the logic of how this motor node should operate should be implemented in the node. 

Node subscribes to topics (like kafka and other distribute system tools) to communicate to other nodes in the same robot. When nodes want to expose something to other nodes, it publishes to the topic.

Nodes can also have parameters for changing for tuning, an example would be a parameter to change the acceleration ratio of the car. 

# Bag Files
Bag files are captures of the topics which are cast to a sql lite and you can replay it as it was the real thing. 
# Services
Are one shot request and response patterns, thing like save current configuration or things like that. It has a pre defined request and response pattern a single server and any number of clients. The syntax is as following:

```
# CalibrateCamera.srv
string mode      # request: what kind of calibration
---
bool success     # response
string message   # response: status/error description
```
Where dash line separates request and response.

I can be thread blocking and can cause deadlock, you can also use an async call to stop it. 
# Actions
Are long running requests with feedback, like a macro task. Example: Drive to point X. It can be canceled. It takes a progress update and have a a definite endpoint. The syntax is as following:

```
# DriveToPoint.action
geometry_msgs/Point target    # goal: where to go
---
bool success                  # result: did we make it?
float32 final_distance_error
---
float32 current_distance      # feedback: published periodically during execution
float32 current_speed
```

Where the first block of dash lines is the goal, which is sent once. The result which is sent in the end, and the feedback which is streamed through.  