class strategy_space(object):
    """Data structure to define the strategy space"""
    def __init__(self, s, discrete=True, rv=None, size=100):
        self.discrete = discrete
        if discrete:
            self.domain = s
            self.size = len(domain)
        else:
            self.limits = s
            self.size = size
            x_min = self.limits[0]
            x_max = self.limits[1]
            if self.size <= 1:
                self.domain = [x_min]
            step = (x_max-x_min)/(self.size-1)
            self.domain = [x_min+step*i for i in range(self.size)]
        self.rv = rv
        self.NE = []
        self.BR = []

    def __str__(self):
        return str([round(x, 3) for x in self])

    def __repr__(self):
        if self.discrete:
            return 'strategy_space({}, {}, rv={}'.format(self.domain, 'discrete', self.rv!=None)
        else:
            return 'strategy_space({}, {}, rv={})'.format(self.limits, 'continuous', self.rv!=None)

    def __iter__(self):
        for x in self.domain:
            yield x

    def __getitem__(self, i):
        if i>=self.size:
            print('Error: Index {} out of bounds for an array of length {}'.format(i, self.size))
            return 
        return self.domain[i]

    def rvs(self, n=1):
        if self.rv == None:
            print("A random variable wasn't defined")
            return None
        else:
            return self.rv.rvs(size=n)

    def pdf(self, domain=None):
        if self.rv == None:
            print("A random variable wasn't defined")
            return None
        if domain == None:
            for x in self.domain:
                yield x, self.rv.pdf(x)
        else:
            for x in domain:
                yield x, self.rv.pdf(x)



