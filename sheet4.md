# Exercise 4

\lstinputlisting[language=Python]{sheet4_ex4.py}

\newpage

![](sheet4_ex4_trajectory_begin.png)

Looking at the first 800 steps of iteration suggests that the
spinup phase is already sufficently long for the system to be converged.

![](sheet4_ex4_trajectory.png)

Even looking at the first 40000 steps reveals no significant chances later on.

![](sheet4_ex4_phase800.png)

But by checking the phase diagramm after a 800 step spinup phase one can see
that it has not fully converged yet whereas 40000 steps as a spinup phas
e are more than enough to fully converge:

![](sheet4_ex4_phase.png)

The Periodicity has already been discovered in exercise 3, where the phase
diagramm was plotted after applying a stroboscope.
There, three distinct points can be observed (the trails again mean that 
is hasn't fully converged yet).
The phase diagramm shows that for \mu=0.90 the diagramm is roughly symmetric
while with increasing \mu it shifts to the left. However, this trend violated
by the splitting of lines e.g. the transition from a period 3 to a
period 5 orbit seen at \mu=0.92.
