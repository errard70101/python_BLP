# -*- coding: utf-8 -*-
"""
Created on Tue May  8 14:03:53 2018

@author: Shih-Yang Lin
"""
import scipy.io
import pandas as pd
import numpy as np

ps2 = scipy.io.loadmat('ps2.mat')
iv = scipy.io.loadmat('iv.mat')

iv = iv['iv']
id = ps2['id'].reshape(-1, )
x1 = np.array(ps2['x1'].todense())

IV = np.concatenate((iv[:, 1:21], x1[:, 1:25]), axis = 1)
x2 = np.array(ps2['x2'].copy())
D = np.array(ps2['demogr'])
v = np.array(ps2['v'])
s_jt = ps2['s_jt'].reshape(-1, )
ans = ps2['ans'].reshape(-1, )

ns = 20   # number of simulated "individuals" per market
nmkt = 94 # number of markets = # of cities * # of quarters
nbrn = 24 # number of brands per market

cdid = np.kron(list(range(1, nmkt + 1)), [1] * nbrn) - 1  # market id
# the number of the last observation in each market
cdindex = np.array(list(range(nbrn - 1, nbrn*nmkt, nbrn))) 

# starting values
theta2w=  np.array([0.3772,  3.0888,       0,  1.1859,       0,
                    1.8480, 16.5980, -0.6590,       0, 11.6245,
                   -0.0035, -0.1925,       0,  0.0296,       0,
                    0.0810,  1.4684,       0, -1.5143,       0]).reshape(4, 5);


#[theti, thetj, theta2] = find(theta2w);

# Create weight matrix
invA = np.linalg.inv(np.dot(IV.T, IV))

# Compute the outside good market share by market
temp = np.cumsum(s_jt)
sum1 = temp[cdindex]
sum1[1:len(sum1)] = np.diff(sum1)
outshr = 1 - sum1[cdid]

y = np.log(s_jt) - np.log(outshr)
mid = np.dot(np.dot(np.dot(x1.T, IV), invA), IV.T)
