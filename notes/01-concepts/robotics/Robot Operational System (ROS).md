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
Are one shot request and response patterns, thing like save current configuration or things like that.

