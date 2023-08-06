# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 10:55:30 2019

@author: Administrator
"""

import matplotlib.pyplot as plt


import random
import numpy as np
import pandas as pd
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

class PSpace:
    def __init__(self, 
                 P_min = 0.1, 
                 P_max = 100,
                 P_e = 50,
                 tick_size = 0.1,
                 lot_size = 100):
        self.P_maxOrg = P_max
        self.P_minOrg = P_min
        # P_spaceOrg => Unscaled Price Space
        self.P_spaceOrg = np.arange(0,(P_max-P_min)/tick_size+1)*tick_size + np.round(P_min/tick_size)*tick_size
        self.Pdiv = (self.P_maxOrg - self.P_minOrg) / 2.0
        # Scale the resuting prices to fit a range from -1 to 1
        self.P_space = (self.P_spaceOrg - P_e)/ self.Pdiv        
        self.TickSizeOrg = tick_size        
        self.TickSize = (self.P_space[1] - self.P_space[0])
        self.LotSize = lot_size
        self.P_eOrg = P_e

                
    def PriceOrg(self, d):
        return find_nearest(self.P_spaceOrg, d)

    def Price(self, d):
        return find_nearest(self.P_space, d)
  
    def PriceSamplerOrg(self, sampleSize):
        return self.P_spaceOrg
    
    def SpreadCost(self, d_n):
        return self.TickSize * np.abs(d_n)
    
    def ImpactCost(self, d_n, LotSizeScl):
        return d_n * d_n*self.TickSize/LotSizeScl
    
    def SpreadCostOrg(self, d_n):
        return self.TickSizeOrg * np.abs(d_n)
    
    def ImpactCostOrg(self, d_n, LotSizeScl):
        return d_n * d_n*self.TickSizeOrg/LotSizeScl
      
    def PriceSamplerPath(self, prices):  
        return ((pd.DataFrame(prices) - self.P_eOrg) / self.Pdiv).values

    def PriceSampler(self, sampleSize):
        prices = self.PriceSamplerOrg(sampleSize)
        return self.PriceSamplerPath(prices)
  
    
class PSpaceRitter(PSpace):
    def __init__(self, 
                 H = 5, 
                 sigma = 0.1):

                 
        PSpace.__init__(self)
        self.theta = np.log(2) / H
        self.sigma = sigma
        
                
  
    def PriceSamplerOrg(self, sampleSize):
        eps_t = np.random.randn(sampleSize)
        pe = self.P_eOrg
        sigma = self.sigma
        lambda_ = self.theta
        p = self.PriceOrg(pe)

        prices = [p]
        for i in range(0,sampleSize):
            y = np.log(p / pe)
            y = y + sigma * eps_t[i] - lambda_ * y
            pnew = pe * np.exp(y)
            # pnew = np.min([pnew, self.P_max])
            # discretizing to make sure it appear in P_space
            prices.append(self.PriceOrg(pnew))
            p = pnew
        return prices
    

 # The following is a different way to model the Ornstein Uhlenbeck Time Series      
class PSpaceOU(PSpace):
    def __init__(self,
                 sigma = 26, 
                 half_life_periods = 90.0, 
                 mu = 50.0, 
                 std_mult = 4, #  1 in 15 787 periods, from: https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule
                 tick_size = 0.01,
                 lot_size = 100,
                ):
        self.TickSizeOrg = tick_size
        # constant 10: empirical value that has worked to get optimal portolios
        self.sampling_frequency = half_life_periods / 10 
        self.deltaT = (self.sampling_frequency / 365.25)
        #self.deltaT = (1 / 365.25)
        
        self.lambda_ = 365.25 * np.log(2) / half_life_periods
        self.std_mult = std_mult
        self.sigmaOrg = sigma
        self.sigma = np.sqrt(2*self.lambda_ * ( 1 / self.std_mult) ** 2)
        self.std_band = np.sqrt(self.sigmaOrg*self.sigmaOrg / (2*self.lambda_))
        self.P_maxOrg = np.round((mu + self.std_mult * self.std_band)/tick_size ) * tick_size
        self.P_minOrg = np.round((mu - self.std_mult * self.std_band)/tick_size ) * tick_size
        self.P_spaceOrg = np.arange(0,(self.P_maxOrg-self.P_minOrg)/tick_size+1)*tick_size + np.round(self.P_minOrg/tick_size)*tick_size
        self.P_eOrg = mu

        self.Pdiv = (self.P_maxOrg - self.P_minOrg) / 2.0

class PHASpace:
    def __init__(self, pSpace,
                  M = 10, 
                  K = 5):


        self.Pdiv = pSpace.Pdiv
        self.P_e = pSpace.Pdiv
        self.P_space = pSpace.P_space
        self.P_spaceOrg = pSpace.P_spaceOrg
        self.pSpace = pSpace       
        self.A_spaceOrg = np.arange(-K ,K+1)*pSpace.LotSize
        self.H_spaceOrg = np.arange(-M, M+1)*pSpace.LotSize
        self.Hdiv = M * pSpace.LotSize
        self.TickSize = (self.P_space[1] - self.P_space[0])

        self.A_space = self.A_spaceOrg / self.Hdiv
        self.H_space = self.H_spaceOrg / self.Hdiv
        
        self.LotSize = pSpace.LotSize / self.Hdiv

        self.iterables = [ self.P_space, self.H_space ]
        self.State_space = pd.MultiIndex.from_product(self.iterables)    
        self.Q_space = pd.DataFrame(index = self.State_space, columns = self.A_space).fillna(0)

        self.iterablesOrg = [ self.P_spaceOrg, self.H_spaceOrg ]
        self.State_spaceOrg = pd.MultiIndex.from_product(self.iterablesOrg)    
        self.Q_spaceOrg = pd.DataFrame(index = self.State_spaceOrg, columns = self.A_spaceOrg).fillna(0)
    

    def Holding(self ,d):
        return find_nearest(self.H_space, d)
      
    def PriceSampler(self, N_train):
        return self.pSpace.PriceSampler(N_train)

    def Price(self, dn):
        return self.pSpace.Price(dn)
           
    def HoldingOrg(self ,d):
        return find_nearest(self.H_spaceOrg, d)
      
    def PriceSamplerOrg(self, N_train):
        return self.pSpace.PriceSamplerOrg(N_train)

    def PriceOrg(self, dn):
        return self.pSpace.PriceOrg(dn)
    
class DQNAgent:
    def __init__(self,
                 phaSp, \
                 batch_size = 1000, \
                 gamma = 0.999, \
                 epsilon = 0.1, \
                 epsilon_min = 0.01, \
                 epsilon_decay = 1, \
                 learning_rate = 0.001, \
                 kappa = 0.0001, \
                 N_train = 10000, \
                 ):

        self.phaSp = phaSp
        
        self.state_example = (self.phaSp.Price(0), self.phaSp.Holding(0))
        self.state_size = len(self.state_example)
        self.action_size = len(self.phaSp.A_space)
        self.batch_size = batch_size

        self.memory = deque(maxlen=self.batch_size*100)
        self.gamma = gamma    # discount rate
        self.epsilon = epsilon  # exploration rate
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.alpha = self.learning_rate
        self.kappa = kappa
        self.N_train = N_train
        self.TickSize = phaSp.TickSize  
        self.LotSize = phaSp.LotSize         
        self.model = self._build_model()
    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()      
        # Attempt one: Use 24 neurons per row 
        model.add(Dense(24, input_dim=self.state_size, activation='hard_sigmoid'))
        model.add(Dense(24, activation='hard_sigmoid'))
        # Or dynamic architecture
        #model.add(Dense(self.action_size*2, input_dim=self.state_size, activation='hard_sigmoid'))
        #model.add(Dense(self.action_size*2, activation='hard_sigmoid'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

      
    def draw_model(self, ax):
        layer_sizes = [self.state_size,self.action_size*2, self.action_size*2, self.action_size ]
        self.draw_neural_net(ax, layer_sizes)
        
    def draw_neural_net(self, 
                   ax, 
                   layer_sizes,
                   left = 0.1, right = 0.9, bottom = 0.1, top = 0.9 ):
        '''
        Draw a neural network cartoon using matplotilb.

        :usage:
            >>> fig = plt.figure(figsize=(12, 12))
            >>> draw_neural_net(fig.gca(), .1, .9, .1, .9, [4, 7, 2])

        :parameters:
            - ax : matplotlib.axes.AxesSubplot
                The axes on which to plot the cartoon (get e.g. by plt.gca())
            - left : float
                The center of the leftmost node(s) will be placed here
            - right : float
                The center of the rightmost node(s) will be placed here
            - bottom : float
                The center of the bottommost node(s) will be placed here
            - top : float
                The center of the topmost node(s) will be placed here
            - layer_sizes : list of int
                List of layer sizes, including input and output dimensionality
        '''
        n_layers = len(layer_sizes)
        v_spacing = (top - bottom)/float(max(layer_sizes))
        h_spacing = (right - left)/float(len(layer_sizes) - 1)
        # Nodes
        for n, layer_size in enumerate(layer_sizes):
            layer_top = v_spacing*(layer_size - 1)/2. + (top + bottom)/2.
            for m in range(layer_size):
                circle = plt.Circle((n*h_spacing + left, layer_top - m*v_spacing), v_spacing/4.,
                                    color='w', ec='k', zorder=4)
                ax.add_artist(circle)
        # Edges
        for n, (layer_size_a, layer_size_b) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
            layer_top_a = v_spacing*(layer_size_a - 1)/2. + (top + bottom)/2.
            layer_top_b = v_spacing*(layer_size_b - 1)/2. + (top + bottom)/2.
            for m in range(layer_size_a):
                for o in range(layer_size_b):
                    line = plt.Line2D([n*h_spacing + left, (n + 1)*h_spacing + left],
                                      [layer_top_a - m*v_spacing, layer_top_b - o*v_spacing], c='k')
                    ax.add_artist(line)

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action
    def oosAct(self, state):
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action
  
    def replay(self,  batch_random):
        if batch_random:
            minibatch = random.sample(self.memory, self.batch_size)
        else:
            minibatch = self.memory[-self.batch_size:]
          
        for state, action, reward, next_state in minibatch:
            target = reward
            target = reward + self.gamma * \
                       np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    def train(self, state, action, reward, next_state):
        target = reward + self.gamma * \
                   np.amax(self.model.predict(next_state)[0])
        target_f = self.model.predict(state)
        target_f[0][action] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)
    def save(self, name):
        self.model.save_weights(name)
    def load(self, name):
        self.model.load_weights(name)
        

    def TotalCost(self, d_n):
        return self.phaSp.pSpace.SpreadCost(d_n) + self.phaSp.pSpace.ImpactCost(d_n, self.LotSize)

    def TotalCostOrg(self, d_n):
        return self.phaSp.pSpace.SpreadCostOrg(d_n) + self.phaSp.pSpace.ImpactCostOrg(d_n, self.LotSize)


    def Reward(self, currState, nextState, TotalCost):
        currPrice = currState[0]
        nextPrice = nextState[0]
        currHolding = currState[1]
        nextHolding = nextState[1]
        dn = nextHolding - currHolding
        cost = self.TotalCost(dn)
        pricedif = nextPrice - currPrice
        pnl = nextHolding * pricedif - cost
        reward = pnl -0.5 * self.kappa * (pnl * pnl)
        result = {
                'pnl': pnl,
                'cost': cost,
                'reward' : reward,
                'dn' : dn
                }
        return result
    
    def ResultReward(self, currState, nextState):
        return self.Reward(currState, nextState, self.TotalCost)

    def ResultRewardOrg(self, currState, nextState):
        return self.Reward(currState, nextState, self.TotalCostOrg)

   
    
    def _Learning(self,randomBatch, N_train) : 
        #pricePath = self.ps.PriceSampler(self.N_train)
        pricePath = self.phaSp.PriceSampler(N_train)
        currState = (self.phaSp.Price(self.phaSp.P_e), self.phaSp.Holding(0))
        for e in range(0, self.N_train-1):
            state = np.reshape(currState, [1, self.state_size])
            action = self.act(state)
            shares_traded = self.phaSp.A_space[action]
            currHolding = currState[1]
            nextHolding = self.phaSp.Holding(currHolding + shares_traded)
            nextPrice = pricePath[e+1]
            nextState = (nextPrice, nextHolding)
            next_state = np.reshape(nextState, [1, self.state_size])
            result = self.ResultReward(currState, nextState)
            reward = result['reward']
            self.remember(state, action, reward, next_state)
            state = next_state
            currState = nextState
            if len(self.memory) > self.batch_size:
                self.replay(randomBatch)
                
            if e % 10000 == 0:
                print(e)

                    
    def LearningBatch(self, N_train) : 
        #pricePath = self.ps.PriceSampler(self.N_train)
        pricePath = self.phaSp.PriceSampler(N_train)
        currState = (self.phaSp.Price(self.phaSp.P_e), self.phaSp.Holding(0))
        for e in range(0, self.N_train-1):
            state = np.reshape(currState, [1, self.state_size])
            action = self.act(state)
            shares_traded = self.phaSp.A_space[action]
            currHolding = currState[1]
            nextHolding = self.phaSp.Holding(currHolding + shares_traded)
            nextPrice = pricePath[e+1]
            nextState = (nextPrice, nextHolding)
            next_state = np.reshape(nextState, [1, self.state_size])
            result = self.ResultReward(currState, nextState)
            reward = result['reward']
            self.remember(state, action, reward, next_state)
            state = next_state
            currState = nextState
            if len(self.memory) > self.batch_size:
                self.replay(randomBatch)
                
            if e % 10000 == 0:
                print(e)

                
    def LearningPath(self, pricePath):
        #pricePath = self.phaSp.PriceSampler(N_train)
        N_train = len(pricePath)
        currState = (self.phaSp.Price(self.phaSp.P_e), self.phaSp.Holding(0))
        for e in range(0, N_train-1):
            state = np.reshape(currState, [1, self.state_size])
            action = self.act(state)
            shares_traded = self.phaSp.A_space[action]
            currHolding = currState[1]
            nextHolding = self.phaSp.Holding(currHolding + shares_traded)
            nextPrice = pricePath[e+1]
            nextState = (nextPrice, nextHolding)
            next_state = np.reshape(nextState, [1, self.state_size])
            result = self.ResultReward(currState, nextState)
            reward = result['reward']
            self.train(state, action, reward, next_state)
            state = next_state
            currState = nextState
            #if e % 1000 == 0:
            #    print(e)
            #    print(currState, reward)
            
                
    def LearningSimple(self, N_train) :
        pricePath = self.phaSp.PriceSampler(N_train)
        self.LearningPath(pricePath)

      
    def OutOfSamplePath(self, pricePath):
        #pricePath = self.phaSp.PriceSampler(nsteps+1)
        nsteps = len(pricePath) -1
        currHolding = self.phaSp.Holding(0)
        pnl = []

        for i in range(0, nsteps):
            currPrice = pricePath[i]
            currState = (currPrice, currHolding)

            state = np.reshape(currState, [1, self.state_size])
            #action = self.act(state)
            action = self.oosAct(state)
            shares_traded = self.phaSp.A_space[action]
            nextHolding = self.phaSp.Holding(currHolding + shares_traded)

            nextPrice = pricePath[i+1]
            nextState = (nextPrice, nextHolding)

            result = self.ResultReward(currState, nextState)
            #pnl.append(result['pnl'])
            pnl.append(result['pnl'] * self.phaSp.Pdiv * self.phaSp.Hdiv)

            currHolding = nextHolding

        return pd.DataFrame(pnl)

    def OutOfSample(self, nsteps):
        pricePath = self.phaSp.PriceSampler(nsteps+1)
        
        return self.OutOfSamplePath(pricePath)

    def OutOfSampleQmap(self, nsteps, QmapIn):
        pricePath = self.phaSp.PriceSamplerOrg(nsteps+1)
        
        return self.OutOfSampleQmapPath(pricePath, QmapIn)
      
      
    def OutOfSampleQmapPath(self, pricePath, Qmap):
        #pricePath = self.phaSp.PriceSamplerOrg(nsteps+1)
        nsteps = len(pricePath) -1
        currHolding = self.phaSp.HoldingOrg(0)
        pnl = []

        for i in range(0, nsteps):

            currPrice = pricePath[i]
            currState = (currPrice, currHolding)
            shares_traded = Qmap.loc[currPrice][0][currHolding]
            #print ('sh_rd',shares_traded)
            nextHolding = self.phaSp.HoldingOrg(currHolding + shares_traded)
            nextPrice = pricePath[i+1]
            nextState = (nextPrice, nextHolding)

            result = self.ResultRewardOrg(currState, nextState)
            pnl.append(result['pnl'] )

            currHolding = nextHolding

        return pd.DataFrame(pnl)

      
      
    def mapQspace(self):
        
        aa = self.phaSp.Q_space.reset_index()
        bb = self.model.predict(aa[['level_0', 'level_1']].values)
        cc = self.phaSp.Q_spaceOrg.copy()
 
        cc.iloc[:,:] = bb
        return cc
  
    def mapQaction(self):
        DQ_space = self.mapQspace()
        return ((pd.DataFrame(DQ_space.idxmax(axis =1))).unstack())

    def drawQspace(self):
      
        
        DQ_full_action = self.mapQaction()
        ax = sns.heatmap(DQ_full_action[0], 
                         yticklabels=int(len(self.phaSp.P_space) / 10), 
                         cmap = 'RdYlBu') 
        majorFormatter = FormatStrFormatter('%0.2f')
        plt.show()
        
               
        self.P_space = (self.P_spaceOrg - mu)/ self.Pdiv
        self.P_e = self.P_eOrg - mu
        self.TickSize = (self.P_space[1] - self.P_space[0])
        self.LotSize = lot_size

      
    def PriceSamplerOrg(self, sampleSize):
        eps_t = np.random.randn(sampleSize)

        #deltaT = 1.0/ 365.25
        deltaT = self.deltaT
        mu = self.P_eOrg
        sigma = self.sigmaOrg 
        theta = self.lambda_
        #theta = (1 / deltaT) * np.log(2) / half_life_periods
        p = self.PriceOrg(mu)


        prices = [p]
        for i in range(0,sampleSize):
            meanChangeValue = (mu - p)*(1 - np.exp(-theta*deltaT))
            standardDeviationValue = sigma * np.sqrt((1 - np.exp(-2 * theta * deltaT)) / (2 * theta))
            actualChange = meanChangeValue + standardDeviationValue * eps_t[i]
            pnew = p + actualChange
            # discretizing to make sure it appear in P_space
            prices.append(self.PriceOrg(pnew))
            # this one seems missing !
            p = pnew
        return prices

    # Here we can add trading costs (including cost borrowing, impact of large trades, etc)
    def ImpactCost(self, d_n, LotSizeScl):
    #    return d_n * d_n*self.TickSize/LotSizeScl
        return 0.0

    def ImpactCostOrg(self, d_n, LotSizeScl):
    #    return d_n * d_n*self.TickSizeOrg/LotSizeScl
        return 0.0
    
    
def plotPNL(pricePathOrg, agent, AlgoT):
    pricePath = agent.phaSp.pSpace.PriceSamplerPath(pricePathOrg)
    pnl = agent.OutOfSamplePath(pricePath)

    fig = plt.figure()
    ax = fig.add_subplot(211)

    ax.plot(pnl.cumsum())

    sharpe_nn = pnl.cumsum().mean()[0] / pnl.cumsum().std()[0] * np.sqrt(one_year)
    print ('-------------------')
    print ('NN', sharpe_nn, pnl.cumsum()[-1:])
    print ('-------------------')


    pnl = agent.OutOfSampleQmapPath(pricePathOrg,AlgoT)
    sharpe_qm = pnl.cumsum().mean()[0] / pnl.cumsum().std()[0] * np.sqrt(one_year)

    ax.plot(pnl.cumsum())
    print ('-------------------')
    print ('Qmap', sharpe_qm, pnl.cumsum()[-1:][0])
    print ('-------------------')

    print ('Sharpe ratio NN/Qmap', sharpe_nn/ sharpe_qm)
    ax2 = fig.add_subplot(212)
    ax2.plot(pricePathOrg, color = 'purple', linestyle = ':')
    plt.show()



    