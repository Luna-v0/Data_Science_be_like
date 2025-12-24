The trick for computing this is to use a negative loss in you neural network since you want to maximize the reward instead of minimize the error

$$


\begin{gather*}
\tau = (s_0,a_0,s_1,a_1,s_2, ...,s_n)\\\\
R(t) = \sum_0^t R_t 
\end{gather*}
$$