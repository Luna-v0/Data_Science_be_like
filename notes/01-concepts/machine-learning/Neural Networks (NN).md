It is important to note that the Neural Network is a abstract thing, that has many different types of implementation, one of the most famous it the Multi Layer Perceptron.

# Multi Layer Perceptron (MLP)
As the name implies it uses multiple [[Perceptron|Perceptrons]], it is a Bipartite Graph, that can have many layers and many nodes in each layer. It has 3 main layers, the input layer, the hidden layers, and the output layer. 

It is computed the same way as before, but the output of a perceptron is the input of the next perceptron, notice that the input layer **is not** a perceptron. 

For the most simple version of this process it uses the Stochastic Gradient Descent, the idea is to minimize the Loss, aka, the difference between what was predicted to the real value. For that you use a Loss function. This gradient is computed using the following:

$$
\begin{gather}
w_u = w_u + \Delta w_u \\ \\
\Delta w_u = - \eta \nabla J(w_u)
\end{gather}
$$

And for learning this it is used the following algorithm called backpropagation.
