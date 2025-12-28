Is the basic component of a [[Neural Networks]] (NN), each node of the NN, follows the same principal as a Perceptron. 

Its components are:
* Input [[Vector]] called $\vec{x}$, which act as the value of the other nodes (or just the input)
* The $\vec{w}$ vector, which is the importance of each input value.
* A bias which is just a fixed input and the first item in the Input Vector ($x_0$).
* An activation function ($A$), which controls how much is the output signal of the Perceptron.

Basically, you compute $A(\vec{w}^t \cdot \vec{x})$ to evaluate the model response, the idea is that the $A$ function counters the [[Linearity]] by make it not linear, therefore no $A$ should be a linear function. 

## Training
For training you get the [[Model Learning#Training a Model|Training Data]] and you use the following to update the Weights.

$$
w_i = w_i + \eta(y - \hat{y})x_i 
$$
Where $\hat{y}$ is the predicted by the model.