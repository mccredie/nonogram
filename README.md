
# Nonogram Solver

I have been playing nonograms on my phone, and it got me thinking about how I
might write an algorithm for solving them.  This is a simple algorithm, in that
it won't solve certain cases of problems.

To call it on the command line

```sh
> solve 1 2 3 x 1 2 3
..#
.##
###
```

There is also an example input file `puzzle.txt` assuming you are using a `*nix` like shell, you can call solve with that input using:

```sh
solve $(cat puzzle.txt)
```
