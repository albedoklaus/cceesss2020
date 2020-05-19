# Exercise 3

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
