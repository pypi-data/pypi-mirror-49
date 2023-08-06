# pyTCTL
A package for TCTL model checking in Python

The initial implementation makes use of NetworkX's DiGraph for the representation of Kripke structures.

The provided algorithms implement [Lepri et al.'s](https://doi.org/10.1016/j.scico.2014.06.006) approach to continuous TCTL model checking. 
Thus, this package also implements pointwise TCTL model checking.

The code was originally developed for the [CREST](https://crestdsl.github.io) project, but it seems better to extract the code into its own library.


## Similar Projects

[@albertocasagrande](https://github.com/albertocasagrande) is working on a similar library for (untimed) CTL/LTL/CTL* model checking called [pyModelChecking](https://github.com/albertocasagrande/pyModelChecking/).

> His approach shares some of the ideas of this project. However, it seems that he chooses to implement Kripke structures directly (no networking library) and adds some features that I probably won't implement (e.g. a text parser).
On the other hand, as far as I can see there's only one algorithm hardcoded for each temporal logic.
In comparison, I plan to add the possibility to add and choose between search heuristics.

> I will keep following his project. Maybe we can merge forces once I know more clearly which path the pyTCTL project is going to take.
