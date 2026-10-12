It's an algorithm for continuously calculate the error value between a current measured value and a target value. Use a lot as a normalization of a signal. 

It is computed by:
$$
pid(t) = K_p \ e(t) + K_i \int_0^t e(t) \ dt + K_d \ e'(t)
$$
