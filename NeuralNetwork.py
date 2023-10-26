import cupy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x <= 0, 0, 1)

class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim, activation="sigmoid"):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim

        # Initialize weights and biases
        self.weights_input_hidden = np.random.randn(self.input_dim, self.hidden_dim)
        self.bias_hidden = np.random.randn(self.hidden_dim)
        self.weights_hidden_output = np.random.randn(self.hidden_dim, self.output_dim)
        self.bias_output = np.random.randn(self.output_dim)

        # Select activation function and its derivative
        if activation == "sigmoid":
            self.activation_function = sigmoid
            self.activation_derivative = sigmoid_derivative
        elif activation == "relu":
            self.activation_function = relu
            self.activation_derivative = relu_derivative

    def forward_propagation(self, input_data):
        # Hidden layer activation
        hidden_output = self.activation_function(np.dot(input_data, self.weights_input_hidden) + self.bias_hidden)

        # Output layer activation
        output = self.activation_function(np.dot(hidden_output, self.weights_hidden_output) + self.bias_output)

        return output

    def train(self, input_data, target_data, learning_rate=0.1, epochs=10000):
        for epoch in range(epochs):
            # Forward propagation
            hidden_output = self.activation_function(np.dot(input_data, self.weights_input_hidden) + self.bias_hidden)
            output = self.activation_function(np.dot(hidden_output, self.weights_hidden_output) + self.bias_output)

            # Backpropagation
            output_error = target_data - output
            output_delta = output_error * self.activation_derivative(output)

            hidden_error = output_delta.dot(self.weights_hidden_output.T)
            hidden_delta = hidden_error * self.activation_derivative(hidden_output)

            # Update weights and biases
            self.weights_hidden_output += hidden_output.T.dot(output_delta) * learning_rate
            self.bias_output += np.sum(output_delta, axis=0) * learning_rate
            self.weights_input_hidden += input_data.T.dot(hidden_delta) * learning_rate
            self.bias_hidden += np.sum(hidden_delta, axis=0) * learning_rate

            # Calculate loss (optional)
            loss = np.mean(np.square(output_error))
            if epoch % 1000 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")

        print("Training completed.")

    def predict(self, input_data):
        return self.forward_propagation(input_data)