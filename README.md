## Transitive Citation

### Introduction

Transitive citation creates a citation tree for a given article entry.

<img src="images/transitiveimg.png?raw=true"/>

### Dependencies
networkx and requests and their dependencies

### Example
```{python}
cmst = get_cmst('2016ApJ...817..91B')
make_plot(cmst, savename='eg.png')
```
