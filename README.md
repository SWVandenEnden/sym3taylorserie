# Python Taylor serie creator

A Python module to create a Taylor serie of a given formula

## Usage

### Calculate Taylor serie
The solutions is a symexpress3 object
```py
>>> import sym3taylorserie
>>> objTaylor = sym3taylorserie.Sym3TaylorSerie()
>>> objTaylor.formula = "(1+x)^^3"
>>> objTaylor.calcTaylorSerie()
>>> print( f"Taylor serie: {objTaylor.taylorSerie}\n" )
Taylor serie: 1 + 3 * x *  factorial( 1 )^^-1 + 6 * x^^2 *  factorial( 2 )^^-1 + 6 * x^^3 *  factorial( 3 )^^-1
```

### Options
Options for the Taylor serie
```py
>>> import sym3taylorserie
>>> objTaylor = sym3taylorserie.Sym3TaylorSerie()
>>> objTaylor.steps = 10 
>>> objTaylor.baseValue = 3
>>> objTaylor.diffVar = "x"
>>> objTaylor.formula = "(1+x)^^3"
>>> objTaylor.calcTaylorSerie()
>>> print( f"Taylor serie: {objTaylor.taylorSerie}\n" )
Taylor serie: 64 + 48 * (x + (-1) * 3) *  factorial( 1 )^^-1 + 24 * (x + (-1) * 3)^^2 *  factorial( 2 )^^-1 + 6 * (x + (-1) * 3)^^3 *  factorial( 3 )^^-1
>>> for iIndex, valSym3 in enumerate(objTaylor.taylorValues): print( f"{iIndex}: {valSym3}\n")
0: 64
1: 48
2: 24
3: 6
```

### Command line
python -m sym3taylorserie

- *Help*: python -m sym3taylorserie -h
- *Taylor serie*: python -m sym3taylorserie "(1+x)^^3"

### Graphical user interface
https://github.com/SWVandenEnden/websym3
