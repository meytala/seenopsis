# -*- coding: utf-8 -*-
"""
Created on Sun May 10 11:46:45 2020
"""
#create a class named VariableInfo with different method to represent featurs of the datasets' variables
#each variable in the dataset will turn to an object

import variable_types
from variable import Variable

def get_variable_info(name, values, index):
    v = Variable(name, values, index)
    if v.var_type == "Single Variable":
        return variable_types.SingleVariable(name, values, index)
    elif v.var_type == "Binary Variable":
        return variable_types.BinaryVariable(name, values, index)
    elif v.var_type == "Categorical Variable":
        return variable_types.CategoricalVariable(name, values, index)
    elif v.var_type == "Continuous Variable":
        return variable_types.ContinuousVariable(name, values, index)
    else:
        return variable_types.TextOrDateVariable(name, values, index)