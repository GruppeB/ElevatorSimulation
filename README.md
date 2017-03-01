# Heis

## Output
A dump of the simulation is available in text format. First line will contain:
```
E F
```
Where `E` is the number of elevators and `F` is the number of floors.

Every line from then on will represent a snapshot of the simulation and will be on the format
```
t ep0 ep1 ep2 ... ep<E-1> #pe0 #pe1 #pe2 ... #pe<E-1> #pf0 #pf1 #pf2 ... #pf<F-1>
```
Where
* `t` is float describing how many seconds have passed since the simulation started.
* `ep<i>` is a float in the interval [0, F - 1] describing where elevator i is. 0 is the first floor and F - 1 is the top floor.
* `#pe<i>` is an integer describing how many persons are currently in elevator i.
* `#pf<j>` is an integer describing how many persons are waiting for an elevator in floor j.

### Example
```
2 3
0.0 0 0 0 0 0 0 0
1.2 0 0 0 0 2 0 0
1.2 0 0 2 0 0 0 0
1.7 0 0 2 0 0 0 0
3.7 1 0 2 0 0 0 0
4.2 1 0 1 0 0 0 0
4.7 1 0 1 0 0 0 0
6.7 2 0 1 0 0 0 0
7.2 2 0 0 0 0 0 0
```

Two elevators and three floors. At t = 1.2 two persons arrive at the first floor (0). Then they are picked up and taken to floor 1 and 2.
