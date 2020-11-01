import numpy as np

class portfolio():
    # init with value=None calculates the total value from ASSETS subvalues
    # init with value assumes ASSETS as weights (can be non-normalized)
    def __init__(self, assets, value=None):
        if value:
            self.values = np.array(value, ndmin=2)
            self.assets = np.array(np.array(assets) / np.sum(assets) * self.values, ndmin=2)
        else:
            self.assets = np.array(assets, ndmin=2)
            self.values = np.array(self.assets.sum(), ndmin=2)
        self.__n = len(assets)
        self.weights = np.array(self.assets / self.values, ndmin=2)
        # # self.returns = np.zeros(self.assets.shape)
        self.returns = []
        self.profits = []
        self.r = []
        self.rebalance = []

    def add_returns(self, ret):
        self.returns = np.append(self.returns, ret).reshape(-1,self.__n)
        # self.returns = np.append(self.returns, r.reshape(-1,len(self.assets)), axis=0)
        # self.returns = np.insert(self.returns, len(self.returns), r, axis=0)
        # self.r = (self.returns * self.weights[0]).sum(axis=1).reshape(-1,1)

    def value(self, val=None):
        if not val:
            return self.values[-1][0]
        else:
            self.values[-1] = val
            _ass = self.assets[-1]
            _new_ass = val * self.weights[-1]
            _temp = self.rebalance[-1] + _new_ass - _ass
            
            self.assets[-1] = _new_ass
            self.rebalance[-1] = _temp

    # continue with last (or new) weight
    def const_weight(self, weights=None):
        if not weights:
            weights = self.weights[-1]
        else:
            weights = weights
        index = len(self.weights)

        for r in self.returns[index-1:]:
            _ass = self.assets[-1]
            _profit = r * _ass
            _r = (r * weights).sum()
            _ass_out = _ass + _profit
            _val = _ass_out.sum()
            _ass_new = _val * weights
            _rebalance = _ass_new - _ass_out

            self.rebalance = np.append(self.rebalance, _rebalance).reshape(-1,self.__n)
            self.profits = np.append(self.profits, _profit).reshape(-1,self.__n)
            self.weights = np.append(self.weights, weights).reshape(-1,self.__n)
            self.assets = np.append(self.assets, _ass_new).reshape(-1,self.__n)
            self.values = np.append(self.values, _val).reshape(-1,1)
            self.r = np.append(self.r, _r).reshape(-1,1)


p = portfolio([100,200,300,150], value=10000)

for i in range(200):
    p.add_returns(np.random.normal(0.005, size=4, scale=0.025))

p.const_weight()

print(p.value())
