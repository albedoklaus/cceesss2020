# Exercise 3

In the following plots, we're still looking at the same logistic map from the previous
exercise - however, this time, we don't discard the first 4000 iterations. Therefore,
the following observations and explanations focus on the details which are unique to
the first few iterations of the logistic map and we won't repeat what was already
mentioned in the previous exercise, yet also applies here.

## Plot for $u_0 = 0.1$

![](sheet02_mu0.1.png)

For the logistic map
$$
x_{n+1} = r x_n (1-x_n)
$$

we can deduce the first iteration as a linear function:
$$
u_1(\mu) = (u_0 (1-u_0)) \mu
$$

For $u_0 = 0.1$, we can calculate a slope of
$$
\left. u_0 (1-u_0) \right|_{u_0=0.1} = 0.1 \cdot 0.9 = 0.09
$$

The corresponding linear graph is visible in the plot above and can
easily be recognised.

\newpage

## Plot for $u_0 = 0.5$

![](sheet02_mu0.5.png)

Special case $u_0 = 0.5$.

\newpage

## Plot for $u_0 = 0.3$

![](sheet02_mu0.3.png)

This plot is shown for comparison with the plot for $u_0 = 0.7$.
See below for the explanation.

\newpage

## Plot for $u_0 = 0.7$

![](sheet02_mu0.7.png)

Due to the symmetry of the logistic map, the iterations for two systems with
initial states $u_0$ and $u_0'$ behave exactly the same if they are of equal
distance to the previously discussed initial state at $0.5$:

$$
|0.5 - u_0| = |0.5 - u_0'|
$$

This is shown in the two plots for $u_0 = 0.3$ and $u_0 = 0.7$ above, which
are both $0.2$ from $0.5$.
