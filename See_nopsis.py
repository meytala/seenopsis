####relevent libraries:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
from numpy import percentile


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
    df = pd.read_csv(table_name, parse_dates=True,infer_datetime_format=True)
    #print("this is the database: ", df)                                       ###QA
    return df



#######################################################
####################number of variables################
#######################################################

""" a function that count the number of records in the table"""

##input = df
##output = number of nun null records

def count_records (df):
    num_records = df.count()
    maximal_numer = max(num_records)
    #print("the number of records in the dataset is {}".format(maximal_numer))
    print(num_records)
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


#########################################################
####################Basic Statistic######################
#########################################################

"""a function that gives you basic statistics"""

class Variable:
    def __init__(self, name, values, type, index):
        self.name = name
        self.values=values
        self.type = type
        self.index = index

    def mean_of_var (self):
        name = self.name
        mean = np.mean(self.values)
        #print("the mean of the coloum {} is {}".format (name, mean))
        return round(mean,2)

    def median_of_var (self):
        name = self.name
        median = np.nanmedian(self.values)
        #print("the median of the coloum {} is {}".format (name, median))
        return round(median,1)

    def lower_iqr (self):
        name = self.name
        values = self.values
        low_iqr = np.nanpercentile(values,25)
        return low_iqr

    def upper_iqr(self):
        name = self.name
        values = self.values
        up_iqr = np.nanpercentile(values, 75)
        return up_iqr

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
        return round(sd,2)

    def count_null (self):
        name = self.name
        values = self.values
        number_of_null=values.isnull().sum()
        return number_of_null


    # def outliers (self):
    #     name = self.name
    #     threshold = 2
    #     outlier = df[name[(np.abs(stats.zscore()) > threshold)]]
    #     return ("there number of outliers of the variable {} is {}".format (name, outlier))

    #
    def histogram (self):
        plt.hist(self.values.dropna(), bins=50)    ######this returns n=array, bins, patch=Silent list of individual patches used to create the histogram
        plt.savefig("hist_{}".format(self.index))
        plt.close()
        return self.index


    ###QA
# name_2 = column_name_list[1]                            #QA
# values_2 = df_table[name_2]
# type_2 = variable_type_list[1]
# test = Variable(name_2, values_2, type_2, index=1)
# print("histogram", test.histogram())
# # # , test.median_of_var(), test.minimum_of_var(), test.maximum_of_var(), test.sd_of_var())



#######################################################
####################Variable histogrial################
#######################################################

""" a function that build an histogram"""




#######################################################
####################Missing Value######################
#######################################################

"""a function that is looking for the missing values"""


# name_1 = name_of_variables (df)[1]                            #QA
# values_1 = df[name_of_variables (df)[1]].values
# test = Variable(name_1, values_1 )
# print(test.maximum_of_var())
# # # , test.median_of_var(), test.minimum_of_var(), test.maximum_of_var(), test.sd_of_var())




######creating a list of objects for the Variable class. Each object has to have:
#  1. a name (the name of the variable)   - line 67, def: name_of_variables, line 119 - the name of the list (column_name_list)
#  2. The values of the variables  - in the dataframe - the values of rows 1 and more (0 is the title) - line 33 the def, line 113 - name of table: df_table
#  3. The type of the variable - line 94: var type, line 125: name of variable: variable_type_list

## I have extracted all of these properties before (lines

list_of_objects = []
for index, variable in enumerate (column_name_list):
    name = variable
    values = df_table[name]  ##in pandas - this is how you get the values
    type = variable_type_list[index]
    index=index
    list_of_objects.append(Variable(name, values, type,index))

#print("list of objects: ", list_of_objects)            #QA


##### for each object, apply the methods of the class Variable. The stat methods are only for variables that are int64 and float64
##### store it as a list

# stat_list = []
# for object in list_of_objects:
#     if object.type.name in ('int64', 'float64'):
#         stat_list.append ( [object.name,
#                       object.type,
#                       object.mean_of_var(),
#                       object.sd_of_var(),
#                       object.median_of_var(),
#                       object.lower_iqr(),
#                       object.upper_iqr(),
#                       object.minimum_of_var(),
#                       object.maximum_of_var(),
#                       object.count_null(),
#                       object.histogram()])   ###appending the list with few variables
#
#
# ##print ("this is the stat list: ", stat_list)            ##QA





#######################################################
####################Output Table#######################
#######################################################

""" a function that wrap everything nicely in a table to display """

##https://stackoverflow.com/questions/1475123/easiest-way-to-turn-a-list-into-an-html-table-in-python

######first, given a "flat list", produce a list of sublists

html_top = """<html>
<table border = 5 border-spacing: 0.5rem>
<caption>SEENOPSIS</caption>
    <tr>
        <th>Variable name</th>
        <th>Type</th>
        <th>Mean &plusmn sd</th>
        <th>Median (IQR) </th>
        <th>Min</th>
        <th>Max</th>
        <th>Null</th>
        <th>Histogram</th>
    </tr>"""

#<th>histogram</th>

html_bottomn = """</table>
</html>"""


body_list = []
for object in list_of_objects:
    if object.type.name in ('int64', 'float64'):
        list_for_body = "<tr>" \
                            "<th> {} </ th>" \
                            "<td> {} </ td>" \
                            "<td> {} &plusmn  <br> {} </ td>" \
                            "<td> {} <br> ({}, {}) </ td>" \
                            "<td> {} </ td>" \
                            "<td> {} </ td>" \
                            "<td> {} </ td>" \
                            "<td> <img src='hist_{}.png' width ='200' hight='150'> </img> </td>"\
                         "</tr>".format ( object.name,
                                          object.type,
                                          object.mean_of_var(),
                                          object.sd_of_var(),
                                          object.median_of_var(),
                                          object.lower_iqr(),
                                          object.upper_iqr(),
                                          object.minimum_of_var(),
                                          object.maximum_of_var(),
                                          object.count_null(),
                                          object.histogram())
        body_list.append(list_for_body)


##############################the histogram doesn't show. in the function (219) I return a saved file. I tried show.

merged_html = html_top + "".join(body_list) +html_bottomn

##print(merged_html)            ##QA


with open("test2.html","w") as html_file:
    html_file.write(merged_html)
    html_file.close()

