Is the process of taking a [[Model Learning|Learned Model]] like a [[Foundation Model (FM)]] and re training it for optimizing in a determinate task. There are a few different techniques for doing this, they can be subdivided in the following categories:
1. [[Reinforcement Learning based Fine Tuning (RFT)]]: Using Reinforcement learning and reward signal to optimize for specific tasks, normally used for precise and ambiguous tasks.
2. [[Supervised Learning base Fine Tuning (SFT)]]: Using more data to extend or optimize leaned model.
3. [[Distillation]]: Using a model (normally a bigger model) optimize for the task to train another model.


# Optimization on Fine Tuning 
[[LoRA]]: An optimization on fine tuning that uses [[Matrix#Rank|Rank]] Decomposition for optimizing the [[Neural Networks (NN)#Backward Propagation|Back Propagation]] it can be uses
