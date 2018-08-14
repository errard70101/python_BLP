# -*- coding: utf-8 -*-
"""
Created on Wed May  9 15:41:32 2018

@author: Shih-Yang Lin
"""
import numpy as np

n_obs = int(1e4)
n_consumers = int(1e3)

estimates = [-5.246, -0.629, -0.826, -1.605, 1.448,
             0.796, 1.093, -0.224, -0.137, -6.127]
sigma = [2.816, 3]

data = np.random.randn(n_obs, len(estimates))

mkt = np.random.randint(low = 0, high = 25, size = n_obs)

end_var = [0, 1]

def utility(estimates, sigma, data, end_var):
    '''
    Calculate mean utility of each products base on the estimates and data.
    input: 
        estimates: list, the estimates of BLP.
        sigma: list, the estimated standard errors of random coefficients.
        data: numpy ndarray, n x k.
        end_var: list, the position of endogenous variables.
        n_consumers: int, number of simulated consumers in each market.
    output:
        uti: numpy array, the mean utility of each products.
    '''
    
    # Examine the number of variables
    Worning_Message_0 = ('The length of estimates is ' + str(len(estimates)) + 
                         ', but the number of columns of data is ' + 
                         str(data.shape[1]) + '.')
    
    assert len(estimates) == data.shape[1], Worning_Message_0
    
    Worning_Message_1 = ('The length of sigma is ' + str(len(sigma)) + 
                         ', but the number of endogenous variables is ' + 
                         str(len(end_var)) + '.')
    
    assert len(sigma) == len(end_var), Worning_Message_1  

    del Worning_Message_0, Worning_Message_1
    
    # Data preparation    
    estimates = np.array(estimates).reshape(len(estimates), 1)
    sigma = np.array(sigma).reshape(len(sigma), 1)
    v = np.random.randn(len(sigma), 1)
    endogenous_variables = data[:, end_var]
    
    # Calculate utilities
    uti = np.dot(data, estimates) + np.dot(endogenous_variables, sigma*v)
    
    return(uti)

def market_share(uti, mkt):
    '''
    Calculate simulated market share of each products in each markets
    base on their utilities.
    input:
        uti: n x 1 numpy array, the utilities of each products in each markets.
        mkt: n x 1 numpy array, the market id of each products in each markets.
    output:
        mkt_shr: n x 1 numpy array, the market share of each products in each 
            markets.
    '''
    # Generate new market id
    mkt_list =  np.unique(mkt)
    new_mkt = np.zeros((len(mkt), ))
    new_mkt_id = 0
    for mkt_id in mkt_list:
        new_mkt[mkt == mkt_id] = new_mkt_id
        new_mkt_id += 1
    
    # Calculate the denominators of market shares in each markets
    denominator = list()
    for i in range(len(uti)):
        denominator.append(1 + np.sum(np.exp(uti[new_mkt == i])))
    denominator = np.array(denominator)
    denominator = denominator[new_mkt.astype(int)]
    
    # Calculate the market share
    mkt_shr = np.exp(uti.reshape(len(uti), ))/denominator
    
    return(mkt_shr)
    

uti = utility(estimates, sigma, data, end_var)

mkt_shr = np.zeros((n_obs, ))
for i in range(n_consumers):
    mkt_shr += market_share(uti, mkt)
mkt_shr = mkt_shr/n_consumers