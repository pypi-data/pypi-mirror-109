import torch
import numpy as np
from xgboost import XGBClassifier,XGBRegressor
from collections import OrderedDict
from XBNet.Seq import Seq

class XBNETClassifier(torch.nn.Module):
    def __init__(self, X_values, y_values, num_layers, num_layers_boosted=1, k=2, epsilon=0.001):
        super(XBNETClassifier, self).__init__()
        self.name = "Classification"
        self.layers = OrderedDict()
        self.boosted_layers = {}
        self.num_layers = num_layers
        self.num_layers_boosted = num_layers_boosted
        self.X = X_values
        self.y = y_values

        self.take_layers_dim()
        self.base_tree()

        self.epsilon = epsilon
        self.k = k

        self.layers[str(0)].weight = torch.nn.Parameter(torch.from_numpy(self.temp.T))


        self.xg = XGBClassifier()

        self.sequential = Seq(self.layers)
        self.sequential.give(self.xg, self.num_layers_boosted)
        self.sigmoid = torch.nn.Sigmoid()


    def get(self, l):
        self.l = l


    def take_layers_dim(self):
        print("Enter dimensions of linear layers: ")
        for i in range(self.num_layers):
            inp = int(input("Enter input dimensions of layer " + str(i + 1) + ": "))
            out = int(input("Enter output dimensions of layer " + str(i + 1)+ ": "))
            set_bias = bool(input("Set bias as True or False: "))
            self.layers[str(i)] = torch.nn.Linear(inp, out, bias=set_bias)
            if i == 0:
                self.input_out_dim = out
            self.labels = out
        print("Enter your last layer ")
        self.ch = int(input("1. Sigmoid \n2. Softmax \n3. None \n"))
        if self.ch == 1:
            self.layers[str(self.num_layers)] = torch.nn.Sigmoid()
        elif self.ch == 2:
            dimension = int(input("Enter dimension for Softmax: "))
            self.layers[str(self.num_layers)] = torch.nn.Softmax(dim=dimension)
        else:
            pass

    def base_tree(self):
        self.temp1 = XGBClassifier().fit(self.X, self.y).feature_importances_
        self.temp = self.temp1
        for i in range(1, self.input_out_dim):
            self.temp = np.column_stack((self.temp, self.temp1))

    def forward(self, x, train=True):
        x = self.sequential(x, self.l,train)
        return x

    def save(self,path):
        torch.save(self,path)


class XBNETRegressor(torch.nn.Module):
    def __init__(self, X_values, y_values, num_layers, num_layers_boosted=1, k=2, epsilon=0.001):
        super(XBNETRegressor, self).__init__()
        self.name = "Regression"
        self.layers = OrderedDict()
        self.boosted_layers = {}
        self.num_layers = num_layers
        self.num_layers_boosted = num_layers_boosted
        self.X = X_values
        self.y = y_values

        self.take_layers_dim()
        self.base_tree()

        self.epsilon = epsilon
        self.k = k

        self.layers[str(0)].weight = torch.nn.Parameter(torch.from_numpy(self.temp.T))


        self.xg = XGBRegressor()

        self.sequential = Seq(self.layers)
        self.sequential.give(self.xg, self.num_layers_boosted)
        self.sigmoid = torch.nn.Sigmoid()


    def get(self, l):
        self.l = l


    def take_layers_dim(self):
        print("Enter dimensions of linear layers: ")
        for i in range(self.num_layers):
            inp = int(input("Enter input dimensions of layer " + str(i + 1) + ": "))
            out = int(input("Enter output dimensions of layer " + str(i + 1)+ ": "))
            set_bias = bool(input("Set bias as True or False: "))
            self.layers[str(i)] = torch.nn.Linear(inp, out, bias=set_bias)
            if i == 0:
                self.input_out_dim = out
            self.labels = out

        print("Enter your last layer ")
        self.ch = int(input("1. Sigmoid \n2. Softmax \n3. None \n"))
        if self.ch == 1:
            self.layers[str(self.num_layers)] = torch.nn.Sigmoid()
        elif self.ch == 2:
            dimension = int(input("Enter dimension for Softmax: "))
            self.layers[str(self.num_layers)] = torch.nn.Softmax(dim=dimension)
        else:
            pass

    def base_tree(self):
        self.temp1 = XGBRegressor().fit(self.X, self.y).feature_importances_
        self.temp = self.temp1
        for i in range(1, self.input_out_dim):
            self.temp = np.column_stack((self.temp, self.temp1))

    def forward(self, x, train=True):
        x = self.sequential(x,self.l,train)
        return x

    def save(self,path):
        torch.save(self,path)