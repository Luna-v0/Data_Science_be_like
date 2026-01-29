RFT techniques are used to optimize [[Model Learning|Learned Models]] to pre determinate tasks. It uses feedback based learning to improve models based on input (in the case of [[Language Models]] would be the prompt), and a reward signal based on the answer. Depending on the technique this can be a multitude of implementation, from human QA, to sorting multiple answers to the same question, to defining a proper reward function.  

## RL with Human Feedback (RLHF)

## RL with AI Feedback

## RL with Verifiable [[Markov Decision Process (MDP)#Reward Function|Reward]] (RLVR)
This technique is normally used in problems like code generation via LLM, by defining code tests the LLM can receive a signal of reward based on code passing or not. 

## Direct [[Markov Decision Process (MDP)#Policy|Policy]] Optimization

## Inverse Reinforcement Learning

## Group Relative Policy Optimization