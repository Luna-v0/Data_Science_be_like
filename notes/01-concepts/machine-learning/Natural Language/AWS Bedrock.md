Its an [[AWS#Services|AWS Service]] for working with [[Language Models]], it can used via API and have built-in tools like [[LLM Agents]], [[Retrieval Augmented Generation (RAG)|RAG]], [[Fine Tuning]], etc. 

By AWS policy no input data is used to train a [[Foundation Model (FM)]]. 

## Features
- You can execute inference of LLMs, not all the models are available through it.
- You can test and compare multiple models in a playground interface and change its [[Model Learning#Hyperparameters|Hyperparameters]].
- See the amount of tokens input and outputs and latency. 
- It lets you customize a model using one of 3 [[Fine Tuning]] techniques:
	1. [[Reinforcement Learning based Fine Tuning (RFT)]]: using a reward function.
	2. [[Supervised Learning base Fine Tuning (SFT)]]: using labeled data.
	3. [[Distillation]]: By using a bigger model to train a smaller one.
- 