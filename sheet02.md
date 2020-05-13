# Exercise 3

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

This linear graph is visible in the plot above: For $u_0 = 0.1$, we can calculate
a slope of

$$
\left. u_0 (1-u_0) \right|_{u_0=0.1} = 0.1 \cdot 0.9 = 0.09.
$$

## Plot for $u_0 = 0.5$

![](sheet02_mu0.5.png)

Special case $u_0 = 0.5$.

## Plot for $u_0 = 0.3$

![](sheet02_mu0.3.png)

## Plot for $u_0 = 0.7$

![](sheet02_mu0.7.png)

Due to the symmetry of the logistic map, the iterations for two systems with
initial states $u_0$ and $u_0'$ behave exactly the same if they are of equal
distance to $0.5$:

$$
|0.5 - u_0| = |0.5 - u_0'|.
$$

This is shown in the two plots for $u_0 = 0.3$ and $u_0 = 0.7$ above.
