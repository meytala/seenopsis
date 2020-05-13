# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import paths
import numpy as np

NUMBER_TYPES = ['int64', 'float64', 'int32', 'float32']
DESCRIBE_SELF_STR = "name: {name}\tindex: {index}\ttype: {var_type}-{np_type}"

class Variable(object):
    def __init__(self, name, values, index):
        self.name = name
        self.values = values
        self.index = index
        
        # get type
        self.np_type = np.dtype(values)
        self.is_number = self.np_type in NUMBER_TYPES
        self.var_type = self.get_var_type(values)
        
        # get statistics
        self.count_unique = self.values.nunique()
        self.count_nulls = self.values.isnull().sum()
        self.percent_nulls = round((self.count_nulls / len(self.values)) * 100, 1)
        
    def get_var_type(self, values):  # variables' type in a format to be presented nicely in the seenopsis output
        if self.values.nunique() == 1:
            return "Single Variable"
        elif self.values.nunique() == 2:
            return "Binary Variable"
        elif 2 < self.values.nunique() <= 10:
            return "Categorical Variable"
        elif self.is_number:
            return "Continuous Variable"
        else:
            return "Text or Date"
        
    def export_graph(self):
        self.values.value_counts().nlargest(10).plot(kind='barh')
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=14)
        bars_file_path = paths.GRAPH_DIR + r"\bars_{}.png".format(self.index)
        plt.savefig(bars_file_path)
        plt.close()
        return bars_file_path

    def str_null_data(self):
        if self.count_nulls == 0:
            return "No missing values"
        return "N={}, {}%".format(self.count_nulls, self.percent_nulls)
    
    def str_number_of_outliers(self, outlier_constant):
        return "No outliers"
    
    def __str__(self):
        return DESCRIBE_SELF_STR.format(name=self.name, index=self.index, var_type=self.var_type, np_type=self.np_type)