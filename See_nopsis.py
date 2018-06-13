####relevent libraries:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
from tkinter.filedialog import askopenfilename
import matplotlib.colors as colors
# from decimal import Decimal
# from numpy import percentile
# from pandas.api.types import is_string_dtype
# from io import StringIO
import matplotlib.cm as cm

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
    # str1 = str(name)
    # str2 = ".csv"
    # filename = "".join((str1, str2))
    filename = askopenfilename()
    #print("the name of the dataset is: {}".format (filename))               ###QA
    return filename


def table_as_df (filename):
    global df
    df = pd.read_csv(filename, parse_dates = True, infer_datetime_format = True, date_parser = pd.to_datetime, encoding='UTF-8')
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


##################calling tHe functions#############3

table_name = name_of_table ("weather")
print("The name of the table is: ", table_name)

df_table = table_as_df (table_name)
#print("this is the database: ", table_as_df (df_table))

record_count = count_records(df_table)
print("The number of records in the dataset is: ", record_count)

column_name_list = name_of_variables (df_table)
print("This is a list with the names of the variables: ", column_name_list)

#
# if is_string_dtype(column_name_list[4]==True):
#     print ("the variable {} is a string".format ("name3"))

number_of_variables = count_var (df_table)
print("In this dataset, the number of variables is: ", number_of_variables)


#########################################################
####################Basic Statistic######################
#########################################################

"""Instances of the Class represents the variable"""
####decided to run as a class, than, for each variable (will turn to object) there will be methods
####the output of the method will be displayed in the output table


class ContVariable:
    def __init__(self, name, values, index):
        self.name = name
        self.values=values
        self.index = index

    def var_type (self):
        type_of_variable = np.dtype(df[self.name])
        return type_of_variable

    def mean_of_var (self):
        name = self.name
        mean = np.mean(self.values)
        #print("the mean of the coloum {} is {}".format (name, mean))
        return round(mean,2)    ####this function returns mean round to 2 decimal

    def median_of_var (self):
        name = self.name
        median = np.nanmedian(self.values)
        #print("the median of the coloum {} is {}".format (name, median))
        return round(median,2)   ####this function returns median round to 2 decimal

    def lower_iqr (self):
        name = self.name
        values = self.values
        low_iqr = np.nanpercentile(values,25)
        return round(low_iqr,2)       ####this function returns the lower boundry of IQR

    def upper_iqr(self):
        name = self.name
        values = self.values
        up_iqr = np.nanpercentile(values, 75)    ####this function returns the upper boundry of IQR
        return round(up_iqr,2)

    def minimum_of_var (self):
        name = self.name
        minimum = np.min(self.values)
        #print("the minimal value of coloum {} is {}".format (name, minimum))    ##QA
        return round(minimum,2) ####this function returns the minimal value of the variable

    def maximum_of_var (self):
        name = self.name
        maximum = np.max(self.values)
        #print("the maximal value of coloum {} is {}".format (name, maximum))    ##QA
        return round(maximum,2)    ####this function returns the maximal value of the variable

    def sd_of_var (self):
        name = self.name
        sd = np.std(self.values)
        #print("the std of coloum {} is {}".format (name, sd))        ##QA
        return round(sd,2)   #####this function returns the sd, round to 2 decimals

    def count_null (self):
        name = self.name
        values = self.values
        number_of_null=values.isnull().sum()
        return number_of_null   ####this function returns the number of nulls in the variable

    def number_of_outliers(self, outlier_constant):
        a = np.array(self.values)
        upper_quartile = np.nanpercentile(a,75)
        lower_quartile = np.nanpercentile(a, 25)
        IQR = (upper_quartile - lower_quartile)
        extend_IQR = IQR * outlier_constant
        louer_boundry = lower_quartile - extend_IQR
        upper_boundry = upper_quartile + extend_IQR
        count=0
        for y in a:
            if (y <= louer_boundry) or (y >= upper_boundry):
                count +=1
        return count   ####this function returns the number of outliers, based on bounderies +/-  X times IQR

    def histogram (self):
        plt.hist(self.values.dropna(), bins=50)    ######this returns n=array, bins, patch=Silent list of individual patches used to create the histogram
        plt.savefig("hist_{}".format(self.index))
        plt.close()
        return self.index


    def pie (self):
        self.values.value_counts().plot(kind='pie')
        # plt.pie(self.values.dropna())    ######this returns n=array, bins, patch=Silent list of individual patches used to create the histogram
        plt.savefig("pie_{}".format(self.index))
        plt.close()
        counts = self.values.value_counts()
        return self.index


    def bars (self):
        self.values.value_counts().nlargest(10).plot(kind='barh')
        plt.savefig("bars_{}".format(self.index))
        plt.close()
        return self.index


    def count_binary (self):
        # unique, counts = np.unique(self.values, return_counts=True)
        # percentage = self.values.value_counts()/len(self.values)*100
        percentage = (np.unique(self.values, return_counts=True)[1] / len(self.values)) * 100
        # counts, freq = self.values.value_counts(normalize=True)
        # percent = freq *100
        # return round(percentage,1)
        return percentage.round(1)



# #     ###QA
# name_2 = column_name_list[9]                            #QA
# values_2 = df_table[name_2]
# test = ContVariable(name_2, values_2, index=9)
# # print("var_type", test.var_type()) ###there is a problem, date returns as an object
# # # # , test.median_of_var(), test.minimum_of_var(), test.maximum_of_var(), test.sd_of_var())
# print("pie",test.pie() )


#######################################################
#######################OBJECTS#########################
#######################################################

"""creating a list of objects for the Variable class. Each object has to have:
#  1. a name - the name of the variable
#  2. The values of the variable
#  3. The index of the variable"""


list_of_objects = []
for index, variable in enumerate (column_name_list):
    name = variable
    values = df_table[name]  ##in pandas - this is how you get the values
    index=index
    list_of_objects.append(ContVariable(name, values, index))

#print("list of objects: ", list_of_objects)            #QA


#######################################################
####################Output Table#######################
#######################################################

##the output will be differential based on the type of the variable

##potential types:

###if dtype is in (int64, float64):
#single variable - only one value
#binary - only 2 unique values (except for null)
#categorical - <= 10 unique variables
#continuoues - >10 unique variables

####if dtype is object:
#single variable - only one value
#binary - only 2 unique values (except for null)
#categorical - <= 10 unique variables
#text/date - >10 unique variables

####will do it while building the HTML


""" a function that wrap everything nicely in a table to display """

html_top = """<html> 
<head>
  <title>SEENOPSIS</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="bootstrap.min.css">
</head>
<body>
<div class="container">
<h2>SEENOPSIS</h2> 
<p>This is the seenopsis of the detaset:  {} <br>
This detaset has {} records and {} variables</p> 
<table class="table table-hover"> 
    <thead>
    <tr> 
        <th>Variable Name</th>  
        <th>Type</th> 
        <th>Graphic Representation</th>
        <th>Basic Statistic</th>
        <th>Missing</th> 
        <th>Outliers (n)</th>  
    </tr></thead>""".format(table_name, record_count, number_of_variables  )


body_list = []
for object in list_of_objects:
    if object.var_type() in ('int64', 'float64'):
        if object.values.nunique()== 1:
            list_for_body = """<tr>
                            <th> {} </ th>
                            <td> Single Value</ td>
                            <td> <img src='bars_{}.png' width='200' hight='200'> </img> </td>
                            <td> Single value:
                            <br> {}: {}% </ td>
                            <td> {} </ td>
                            <td> Single Value: 
                             <br>No outliers </ td>
                         </tr>""".format (object.name,
                                          object.bars(),
                                          object.values.unique()[0],
                                          object.count_binary()[0],
                                          object.count_null())
        elif object.values.nunique()== 2:
            list_for_body = """<tr>
                            <th> {} </ th>
                            <td> Binary Variable </ td>
                            <td> <img src='bars_{}.png' width='200' hight='200'> </img> </td>
                            <td> Binary variable 
                            <br> {}: {}%, {}: {}% </ td>
                            <td> {} </ td>
                            <td> Binary variable
                             <br>No outliers </ td>
                         </tr>""".format (object.name,
                                          object.bars(),
                                          object.values.unique()[0],
                                          object.count_binary()[0],
                                          object.values.unique()[1],
                                          object.count_binary()[1],
                                          object.count_null())
        elif object.values.nunique()>2 and object.values.nunique()<=10 :
            list_for_body = """<tr>
                            <th> {} </ th>
                            <td> Categorical Variable* </ td>
                            <td> <img src='bars_{}.png' width='200' hight='200'> </img> </td>
                            <td> Categorical Variable </ td>
                            <td> {} </ td>
                            <td> Categorical Variable
                             <br>No outliers </ td>
                         </tr>""".format (object.name,
                                          object.bars(),
                                          object.count_null())
        else: list_for_body = """<tr>
                            <th> {} </ th>
                            <td> Continuous variable 
                            <br>({}) </ td>
                            <td> <img src='hist_{}.png' width ='200' hight='150'> </img> </td>
                            <td> Min: {} 
                            <br> Max: {} 
                            <br> Mean &plusmn SD: {} &plusmn {} 
                            <br> Median (IQR): {} ({}, {}) </ td>
                            <td> {} </ td>
                            <td> {} </ td>
                         </tr>""".format ( object.name,
                                        object.var_type(),
                                        object.histogram(),
                                        object.minimum_of_var(),
                                        object.maximum_of_var(),
                                        object.mean_of_var(),
                                        object.sd_of_var(),
                                        object.median_of_var(),
                                        object.lower_iqr(),
                                        object.upper_iqr(),
                                        object.count_null(),
                                        object.number_of_outliers(outlier_constant=1.5))
        body_list.append(list_for_body)
    elif object.var_type() == 'object':
        if object.values.nunique()== 1:
            list_for_body = """<tr>
                            <th> {} </ th>
                            <td> Single value </ td>
                            <td> <img src='bars_{}.png' width ='200' hight='150'> </img> </td>
                            <td> Single Value: 
                            <br> {}: {}% </ td>
                            <td> {} </ td>
                            <td> Single Value:
                             <br>No outliers </ td>
                         </tr>""".format (object.name,
                                          object.bars(),
                                          object.values.unique()[0],
                                          object.count_binary()[0],
                                          object.count_null())
        elif object.values.nunique()== 2:
            list_for_body = """<tr>
                            <th> {} </ th>
                            <td> Binary Variable </ td>
                            <td> <img src='bars_{}.png' width ='200' hight='150'> </img> </td>
                            <td> Binary variable 
                            <br> {}: {}%, {}: {}% </ td>
                            <td> {} </ td>
                            <td> Binary variable
                             <br>No outliers </ td>
                         </tr>""".format (object.name,
                                          object.bars(),
                                          object.values.unique()[0],
                                          object.count_binary()[0],
                                          object.values.unique()[1],
                                          object.count_binary()[1],
                                          object.count_null())
        elif object.values.nunique()> 2 and object.values.nunique()<=10:
            list_for_body = """<tr>
                            <th> {} </ th>
                            <td> Categorical Variable** </ td>
                            <td> <img src='bars_{}.png' width ='200' hight='150'> </img> </td>
                            <td> Categorical variable  
                            <td> {} </ td>
                            <td> Categorical variable
                             <br>No outliers </ td>
                         </tr>""".format (object.name,
                                         object.bars(),
                                          object.count_null())
        else:
            list_for_body = """<tr>
                                <th> {} </ th>
                                <td> Text/Date variable</ td>
                                <td> <img src='bars_{}.png' width ='200' hight='150'> </img> </td>
                                <td> Text/Date variable - 
                                <br> only top 10 values are presented </td>
                                <td> {} </ td>
                                <td> Text/Date variable
                                 <br>No outliers </ td>
                             </tr>""".format(object.name,
                                             object.bars(),
                                             object.count_null())
        body_list.append(list_for_body)

html_bottomn = """</table> 
</div></body>
</html>"""



##############################the histogram doesn't show. in the function (219) I return a saved file. I tried show.

merged_html = html_top + "".join(body_list) +html_bottomn

##print(merged_html)            ##QA

with open("output_seenopsis.html","w") as html_file:
    html_file.write(merged_html)
    html_file.close()

with open("output_seenopsis.html","r") as html_file:
    Seenopsis_table = html_file.read()
    webbrowser.open_new_tab('output_seenopsis.html')
    html_file.close()

