import itertools
import numpy as np
import random
import pickle
import time
import math
import copy
class Net(object):

    def __init__(self):
        self.time_step = 0
        # number of feature inputs
        self.num_inputs = 198
        # number of hidden layer 'neurons'
        self.num_hidden_units = 40
        # number of output units - 1 signifying the probability of white winning, the 2nd is black winning
        self.num_output_units = 2
        # how many iterations?
        self.cycles = 100
        # Use the step size that Tesauro used
        self.learning_rate = .1
        # Use the Gamma size that Tesauro used
        self.discount_rate = .9
        # Use the Lambda size that Tesauro used
        self.l = .7

        # Set up the network weights
        self.features = [[np.random.randn() for x in range(self.num_inputs)] for y in range(self.cycles)]
        self.hidden_layer = [np.random.randn() for x in range(self.num_hidden_units)]
        self.output_layer = [np.random.randn() for x in range(self.num_output_units)]
        self.input_weights = [[np.random.randn() for x in range(self.num_hidden_units)] for y in range(self.num_inputs)]
        self.hidden_weights = [[np.random.randn() for x in range(self.num_output_units)] for y in range(self.num_hidden_units)]

        # Some of these might not need later down the road
        self.old_output = [0 for x in range(self.num_output_units)];
        # Set up an eligibility_trace for the weights in between the input layer and the hidden layer
        self.input_eligibility_trace = [[[0 for x in range(self.num_output_units)] for y in range(self.num_hidden_units)] for z in range(self.num_inputs)]
        # Set up an eligibility_trace for the weights in between the hidden layer and the output layer
        self.hidden_eligibility_trace = [[0 for x in range(self.num_output_units)] for y in range(self.num_hidden_units)]
        # self.reward = [[0 for x in range(self.num_output_units)] for y in range(self.cycles)]
        # self.error = [0 for x in range(self.num_output_units)]

    #Helper functions
    def sigmoid(self, z):
           return 1.0 / (1.0 + np.exp(-z))

    def getValue(self, features):
        # getValue feeds an input representation through and returns what the value would be
        # (feedforward alters the actual self network)

        # Replicate and copy the layers
        out = [np.random.randn() for x in range(self.num_output_units)]
        # Hidden layer copy
        h_l = [np.random.randn() for x in range(self.num_hidden_units)]
        # Input weight layer copy
        i_w = [[np.random.randn() for x in range(self.num_hidden_units)] for y in range(self.num_inputs)]
        # Hidden weight layer copy
        h_w = [[np.random.randn() for x in range(self.num_output_units)] for y in range(self.num_hidden_units)]

        # Find the dot product of the input features and the hidden weights
        # Run through the activation function
        for j in range(0, 40):
            for i in range(0, 198):
                h_l[j] += (features[i] * self.input_weights[i][j])
                h_l[j] = self.sigmoid(h_l[j])

        # Find the dot product of the hidden layer weights and the output units
        # Run through the activation function
        for k in range(0, 2):
            out[k] = h_l[j] * self.hidden_weights[j][k]
            out[k] = self.sigmoid(out[k])
        return out

    def feedforward(self, features):
        for j in range(0, 40):
            for i in range(0, 198):
                self.hidden_layer[j] += (features[i] * self.input_weights[i][j])
                self.hidden_layer[j] = self.sigmoid(self.hidden_layer[j])

        for k in range(0, 2):
            self.output_layer[k] = self.hidden_layer[j] * self.hidden_weights[j][k]
            self.output_layer[k] = self.sigmoid(self.output_layer[k])

        self.time_step += 1


    def do_td(self, features, out, error):

        # Calculate the gradient of the output for the current state
        gradient = []
        for k in range(0,2):
            gradient.append(out[k] * (1 - out[k]))

        # Trying to maintain eligibility traces for respective weights in both input and hidden layers
        # Each eligibility trace is updated everytime td learing is called
        for j in range(0, self.num_hidden_units):
            for k in range(0,2):
                self.hidden_eligibility_trace[j][k] = (self.l * self.hidden_eligibility_trace[j][k] + gradient[k] * self.hidden_layer[j])

                for i in range(0, 198):
                    self.input_eligibility_trace[i][j][k] = (self.l * self.input_eligibility_trace[i][j][k] + gradient[k] * self.hidden_weights[j][k] * self.hidden_layer[j] * (1-self.hidden_layer[j]) * features[i])

        for k in range(0,2):
            for j in range(0, 40):
                self.hidden_weights[j][k] += self.learning_rate * self.error[k] * self.hidden_eligibility_trace[j][k]
                for i in range(0, 198):
                    self.input_weights[i][j] += self.learning_rate * self.error[k] * self.input_eligibility_trace[i][j][k]

    # Helpers to save so I don't have to spend hours training again.
    def save(self):
    	with open('../data/hidden_weights_file', 'wb') as wf:
    		pickle.dump(self.hidden_weights, wf)
    	with open('../data/input_weights_file', 'wb') as bf:
    		pickle.dump(self.input_weights, bf)
    	with open('../data/hidden_eligibility__file', 'wb') as wf:
    		pickle.dump(self.hidden_eligibility_trace, wf)
    	with open('../data/input_eligibility_trace', 'wb') as bf:
    		pickle.dump(self.input_eligibility_trace, bf)

    def load(self):
    	with open('../data/hidden_weights_file', 'rb') as wf:
    		self.hidden_weights = pickle.load(wf)
    	with open('../data/input_weights_file', 'rb') as bf:
    		self.input_weights = pickle.load(bf)
    	with open('../data/hidden_eligibility__file', 'rb') as wf:
    		self.hidden_eligibility_trace = pickle.load(wf)
    	with open('../data/input_eligibility_trace', 'rb') as bf:
    		self.input_eligibility_trace = pickle.load(bf)
