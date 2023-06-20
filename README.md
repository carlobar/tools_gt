# tools-gt

Package to define and analyze games of n players 

## Requirements

Needs the libraries `itertools` and `numpy`


## Usage

```
import tools_gt as gt

S_1 = gt.strategy_space([0, 1], discrete=False, size=2)
S_2 = gt.strategy_space([0, 1], discrete=False, size=2)

S = [S_1, S_2]

U = [U1, U2]

P = 2

G = gt.game(U, S, P)

NE = G.find_NE()
```

