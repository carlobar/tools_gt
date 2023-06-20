import itertools
import numpy as np

class game(object):
    """Data structure to define a game"""
    def __init__(self, U, S, P):
        if type(P) == int:
            self.n = P
            self.P = [i for i in range(P)]
        else:
            self.n = len(P)
            self.P = P
        
        if self.verify(S, self.n, 'S'):
            self.S = S

        if self.verify(U, self.n, 'U'):
            self.U = U

    def verify(self, x, n, name):
        """Check if a variable has lenght n"""
        if len(x) != n:
            print('Error: {} has length {}, but the expected length is {}.'.format(name, len(x), n))
            return False
        return True

    def __len__(self):
        """The lenght of the game is the number of players"""
        return self.n

    def __repr__(self):
        s_text = 'x'.join( ['{}' for i in range(n)] )
        s_val = [S[i].size for i in range(n)]
        text = 'Game(Players={}, Strategies='+s_text+')'
        return text.format(n, *s_val)

    def __iter__(self):
        """Return utilities and strategy spaces in an iterator"""
        for i in range(self.n):
            yield U[i], S[i]

    def split_strategies(self, S, i):
        """Return the strategies of player i (s_{i}) and others (s_{-i})"""
        n = len(S)
        if i<0 or i>=n:
            return None
        S_i = S[i]
        if i == 0:
            S_j = S[i+1:]
        elif i == n-1:
            S_j = S[0:n-1]
        else:
            S_j = S[0:i] + S[i+1:]
        return S_i, S_j
        
    def merge_strategies(self, s_i, s_j, i):
        """Return the joint strategy of players s = (s_i, s_{-i})"""
        n = len(s_j)+1
        if type(s_j) == tuple:
            s_j = list(s_j)
        if i==0:
            s = [s_i] + s_j
        elif i == n-1:
            s = s_j + [s_i]
        else:
            s = s_j[0:i] + [s_i] + s_j[i:]
        return s


    def best_response(self, i):
        """Returns the best action s_i for each s_{-i}"""
        BR = {}
        S_i, S_j = self.split_strategies(self.S, i)
        for s_j in itertools.product( *S_j ):
            max_val = -np.inf
            idx_max = []
            s_max = []
            for k, s_i_k in enumerate(S_i):
                s = self.merge_strategies(s_i_k, s_j, i)
                u_i = self.U[i]( *s )
                if u_i > max_val:
                    max_val = u_i
                    idx_max = [k]
                    s_max = [s_i_k]
                elif u_i == max_val:
                    idx_max.append(k)
                    s_max.append( s_i_k )
            #BR[ s_j ] = idx_max
            BR[ s_j ] = s_max
        return BR

    def valid_NE(self, s, BR, S):
        """Verifies if s_i is the best strategy given s_{-i}, for each player i"""
        n = len(s)
        for i in range(n):
            s_i, s_j = self.split_strategies(s, i)
            if s_i not in BR[i][ tuple(s_j) ]:
                return False
        return True

    def find_NE(self):
        """Search the strategy space for NE"""
        n = len(self.S)
        BR = [[] for i in range(n)]
        for i in range(n):
            BR[i] = self.best_response(i)

        NE = []
        i=0
        S_i, S_j = self.split_strategies(self.S, i)
        for s_j in itertools.product( *S_j ):
            for s_i_k in BR[i][ tuple(s_j) ]:
                #s_i = S_i[k]
                s = self.merge_strategies(s_i_k, s_j, i)
                if self.valid_NE(s, BR, self.S):
                    NE.append(s)
        self.BR = BR
        self.NE = NE
        return NE

    def BR_mapping(self, i):
        """Returns the pair (x, y) to plot the best response of player i"""
        S_i, S_j = self.split_strategies(self.S, i)
        x = []
        y = []
        if self.BR == []:
            BR = [[] for i in range(n)]
            for i in range(n):
                BR[i] = self.best_response(i)
            self.BR = BR

        for s_j in itertools.product( *S_j ):
            for s_i_k in self.BR[i][ s_j ]:
                #s_i = S[i][k]
                x.append( s_j )
                y.append( s_i_k )
        return y, x

