Its a extension of [[Covariance]] for multiple random variables, its goal is to capture how variables vary together.
$$
\begin{gather*}


\Sigma = \begin{pmatrix}
Cov(X_1,X_1) & Cov(X_1,X_2) & \ldots & Cov(X_1,X_n) \\
Cov(X_2,X_n) & Cov(X_2,X_2) & \ldots & Cov(X_2,X_n) \\
\ldots & \ldots & \ldots & \ldots \\
Cov(X_n,X_1) & Cov(X_n,X_2) & \ldots & Cov(X_n,X_n) 
\end{pmatrix} \\ \\

\Sigma = \mathbb{E}[(X-\mu) (X-\mu)^T]

\end{gather*}
$$

> [!tip] $Cov(X_i,X_i) = Var(X_i)$

> [!info] A Covariance Matrix is a [[Types of Matrices#Symmetrical Matrix|Symmetrical Matrix]]

Related to [[Expected Value]].