# Exercise 3

\lstinputlisting[language=Python]{sheet3_3.py}

\newpage

![](sheet3_plot_n=10.png)

Looking at 10 random numbers, we cannot spot any particular
behavior of the different generation methods.

![](sheet3_plot_n=100.png)

For 100 random numbers, there is still not much difference
to report.

![](sheet3_plot_n=1000.png)

For 1000 random numbers, the plot suggests a non-linear progress
for the numbers which were generated with the logistic map.

![](sheet3_plot_n=10000.png)

This behavior is amplified in the plot for 10000 numbers. While
every other method runs more or less close to the reference line,
the numbers generated with the logistic map show a distinct non-linear
behavior: Numbers close to 0 and 1 (so both ends of the interval) are
overrepresentated. There is a steep slope at the middle of the curve
which means we won't generate those numbers as frequently as the ones
towards either interval bounds.

![](sheet3_trans_n=1000_shift=1.png)

In the transition/transfer plot shifted by 1, we can see the function
graph of the logistic map.

![](sheet3_trans_n=1000_shift=2.png)

In the transition/transfer plot shifted by 2, we can see the function
graph of the second iterate of the logistic map.

![](sheet3_trans_n=1000_shift=5.png)

If we shift the transition/transfer plot by 5, the expected function
graph begins to disappear.

![](sheet3_trans_n=10000_shift=5.png)

However, after increasing the number of points, the characteristic
reappears.

![](sheet3_trans_n=10000_shift=10.png)

In the transition/transfer plot shifted by 10, we can see the
concentration of points and overrepresentation of numbers towards
the interval bounds.
