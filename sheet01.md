Betriebssysteme und Netzwerke (IBN)

# Übungsblatt 1

## Aufgabe 1

Beispieltabelle falls nötig:

|            | Wert für $t_{ave}$ | Wahrscheinlichkeit |
| ---------- | ------------------ | ------------------ |
| cache hit  | $t_+ = t_c$        | $p_+$              |
| cache miss | $t_- = t_c + t_r$  | $p_- = 1 - p_+$    |

Beispielformeln falls nötig:

\begin{align*}
\Rightarrow t_{ave} & = \sum_{i \in \{+, -\}} t_i p_i \\
                    & = t_+ p_+ + t_- p_- \\
                    & = t_c p_+ + (t_c + t_r)(1 - p_+) \\
                    & = t_c p_+ + t_c + t_r - t_c p_+ - t_r p_+ \\
                    & = t_c + t_r - t_r p_+ \\
                    & = t_c + t_r (1 - p_+) \\
                    & = t_c + t_r p_-
\end{align*}

\newpage
## Aufgabe 2

\newpage
## Appendix

\lstinputlisting[language=python]{sheet01.py}
