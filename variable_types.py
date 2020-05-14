# -*- coding: utf-8 -*-
"""
Created on Sun May 10 18:11:37 2020

@author: leah.london
"""
from variable import Variable
import numpy as np
import matplotlib.pyplot as plt
import paths
import variable_info

class ContinuousVariable(Variable):
    def __init__(self, name, values, index):
        super().__init__(name, values, index)
        self.mean = round(float(np.nanmean(self.values)), 2)
        self.median = round(float(np.nanmedian(self.values)), 2)
        self.lower_iqr = round(float(np.nanpercentile(self.values, 25)), 2)
        self.upper_iqr = round(float(np.nanpercentile(self.values, 75)), 2)
        self.min = round(float(np.nanmin(self.values)), 2)
        self.max = round(float(np.nanmax(self.values)), 2)
        self.sd = round(float(np.nanstd(self.values)), 2)
    
    def export_graph(self):
        plt.hist(self.values.dropna(), bins=50)
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)
        hist_file_path = paths.GRAPH_DIR + r"\hist_{}.png".format(self.index)
        plt.savefig(hist_file_path)
        plt.close()
        return hist_file_path
    
    def str_number_of_outliers(self, outlier_constant):
        a = np.array(self.values)
        upper_quartile = np.nanpercentile(a, 75)
        lower_quartile = np.nanpercentile(a, 25)
        iqr = (upper_quartile - lower_quartile)
        extend_iqr = iqr * outlier_constant
        lower_boundary = lower_quartile - extend_iqr
        upper_boundary = upper_quartile + extend_iqr
        count = 0
        if iqr == 0:
            return "IQR=0, Outliers were not analyzed"
        else:
            for y in a:
                if (y <= lower_boundary) or (y >= upper_boundary):
                    count += 1
            return "N={}".format(count)
    
    def list_statistics(self):  ### returns what will be written in the statistic column of seenopsis- based on variable type
        return ["Continuous Variable",
                "Min: {}".format(self.min),
                "Max: {}".format(self.max),
                "Mean & plusmn SD: {} &plusmn {}".format(self.mean, self.sd),
                "Median (IQR): {} ({}, {})".format(self.median, self.lower_iqr, self.upper_iqr)]

    
class BinaryVariable(Variable):
    def __init__(self, name, values, index):
        super().__init__(name, values, index)
        self.unique_values = self.values.dropna().unique().tolist()

    def list_statistics(self):  ### returns what will be written in the statistic column of seenopsis- based on variable type
        all_count = len(self.values)
        val_0_count = self.values.isin([self.unique_values[0]]).sum(axis=0)
        val_1_count = self.values.isin([self.unique_values[1]]).sum(axis=0)
        return ["Binary Variable",
        "{}: {}, {}%".format(self.unique_values[0], val_0_count, round(val_0_count / all_count * 100.0, 2)),
        "{}: {}, {}%".format(self.unique_values[1], val_1_count, round(val_1_count  / all_count * 100.0, 2))]


class CategoricalVariable(Variable):
    def __init__(self, name, values, index):
        super().__init__(name, values, index)
        
    def list_statistics(self):  ### returns what will be written in the statistic column of seenopsis- based on variable type
        return ["Categorical Variable",
                "{} unique values".format(self.count_unique),
                "Up to top 10 values are presented"]

class SingleVariable(Variable):
    def __init__(self, name, values, index):
        super().__init__(name, values, index)
        
    def list_statistics(self):  ### returns what will be written in the statistic column of seenopsis- based on variable type
        return ["Single Variable",
                "No Statistics"]

class TextOrDateVariable(Variable):
    def __init__(self, name, values, index):
        super().__init__(name, values, index)
        
    def list_statistics(self):  ### returns what will be written in the statistic column of seenopsis- based on variable type
        return ["Text or Date",
                "Up to top 10 values are presented",
                "Out of {} unique values".format(self.count_unique)]
