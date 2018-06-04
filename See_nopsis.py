####relevent libraries:

import pandas as pd
import numpy as np
# from scipy import stats
# from scipy.stats import zscore
# import matplotlib.pyplot as plt


#######################################################
####################Importing Table####################
#######################################################

##input:  the name of the table
##output: a dataframe in pandas

"""a function that takes the input table and manipulate it for work
    the table should be a csv table and should be located in the working directory"""

###in the beta version, only CSV will be allowed as an input table from the working directory
###the function will take the name that the user wrote and add to it ".csv"


def name_of_table (name):
    str1 = str(name)
    str2 = ".csv"
    table_name = "".join((str1, str2))
    #print("the name of the dataset is: {}".format (table_name))               ###QA
    return table_name


def table_as_df (table_name):
    df = pd.read_csv(table_name)
    #print("this is the database: ", df)                                       ###QA
    return df



#######################################################
####################number of variables################
#######################################################

""" a function that count the number of records in the table"""

##input = df
##output = number of records

def count_records (df):
    num_records = df.count()
    maximal_numer = max(num_records)
    #print("the number of records in the dataset is {}".format(maximal_numer))
    return maximal_numer




###############################################################################################
###############careat a list with the names of the variables from the original df##############
###############################################################################################

""" careat a list with the names of the variables from the original df"""
#
# input: name of the dataset
# output: a list of the names of the variables in the dataset

def name_of_variables (df):
    column_name_list = list(df)
    #print("column names: ", column_name_list)
    return column_name_list



######################################################################
################count the number of variables in a dataset############
######################################################################

##input: name of the dataset
##output: number of variables in the dataset

def count_var (df):
    number_of_variables = len(name_of_variables(df))
    #print("there are {} variables in the dataset".format(number_of_variables) )
    return  number_of_variables



########################################################################
####################create a list of Variable Type######################
########################################################################

""" a function that detect the type of the variable from the original table and add it in a new column in the var_table"""

def var_types (df):
    var_type_list = []
    for var in df:
        #var_type = df[var].dtype
        #var_type= type(var)
        var_type = np.dtype(df[var])
        var_type_list.append(var_type)
    #print ("list of variables type:", var_type_list)
    return var_type_list





##################calling tHe functions#############3

table_name = name_of_table ("weather")
print("The name of the table is: ", table_name)

df_table = table_as_df (table_name)
#print("this is the database: ", table_as_df (df_table))

record_count = count_records(df_table)
print("The number of records in the dataset is: ", record_count)

column_name_list = name_of_variables (df_table)
print("This is a list with the names of the variables: ", column_name_list)

number_of_variables = count_var (df_table)
print("In this dataset, the number of variables is: ", number_of_variables)

variable_type_list = var_types (df_table)
print("This is a list with the type of the variables: ",variable_type_list)




#######################################################
#########################ID############################
#######################################################

""" A function that identify an ID coloumn if exist"""
###this is needed to make sure that you don't run the functions for this coloumn
### if there is more than one row with the same ID - function will only work for first row
### will be identified if each row has a unique variable



##NEED TO CODE


#######################################################
####################Variable histogrial################
#######################################################

""" a function that build an histogram"""




#######################################################
####################Missing Value######################
#######################################################

"""a function that is looking for the missing values"""


#########################################################
####################Basic Statistic######################
#########################################################

"""a function that gives you basic statistics"""

class Variable:
    def __init__(self, name, values, type):
        self.name = name
        self.values=values
        self.type = type

    def mean_of_var (self):
        name = self.name
        mean = np.mean(self.values)
        #print("the mean of the coloum {} is {}".format (name, mean))
        return mean

    def median_of_var (self):
        name = self.name
        median = np.median(self.values)
        #print("the median of the coloum {} is {}".format (name, median))
        return median

    def minimum_of_var (self):
        name = self.name
        minimum = np.min(self.values)
        #print("the minimal value of coloum {} is {}".format (name, minimum))
        return minimum

    def maximum_of_var (self):
        name = self.name
        maximum = np.max(self.values)
        #print("the maximal value of coloum {} is {}".format (name, maximum))
        return maximum

    def sd_of_var (self):
        name = self.name
        sd = np.std(self.values)
        #print("the std of coloum {} is {}".format (name, sd))
        return sd

    # def count_null (self):
    #     name = self.name
    #     is_null = df[name].isnull().sum()
    #     print("there number of null values of the variable {} is {}".format (name, is_null))
    #     return is_null

    # def outliers (self):
    #     name = self.name
    #     threshold = 2
    #     outlier = df[name[(np.abs(stats.zscore()) > threshold)]]
    #     return ("there number of outliers of the variable {} is {}".format (name, outlier))



###I need to have a for loop to run this for every variable in the list of variables.
###the following works only with variables that are continoues - dtype('int64'), dtype('float64')
#

list_of_objects = []
for index, variable in enumerate (column_name_list):
    name = variable
    values = df_table[name]
    type = variable_type_list[index]
    list_of_objects.append(Variable(name, values, type))

#print("list of objects: ", list_of_objects)

for object in list_of_objects:
    if object.type.name in ('int64', 'float64'):
        print ("object: ", object.name,
               "mean: ", object.mean_of_var(),
               "median: ", object.median_of_var(),
               "minimum: ", object.minimum_of_var(),
               "maximum: ", object.maximum_of_var(),
               "sd: ", object.sd_of_var())






# if df[col].dtype.name == 'datetime64[ns]':

# name_1 = name_of_variables (df)[1]                            #QA
# values_1 = df[name_of_variables (df)[1]].values
# test = Variable(name_1, values_1 )
# print(test.maximum_of_var())
# # # , test.median_of_var(), test.minimum_of_var(), test.maximum_of_var(), test.sd_of_var())
#



#######################################################
####################Outliers###########################
#######################################################

"""a function that detect outlier"""




#######################################################
####################Output Table#######################
#######################################################

""" a function that wrap everything nicely in a table to display"""

