__author__      = "Meytal Avgil Tsadok"
__copyright__   = "Copyright 2018, TLV Israel"
__credits__ = "She codes - Final project"
__version__ = "1.0.1"
__maintainer__ = "Meytal Avgil Tsadok"
__email__ = "meytala@gmail.com"
__status__ = "Production"

####relevent libraries:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
from tkinter.filedialog import askopenfilename
import os
# import matplotlib.colors as colors
# from decimal import Decimal
# from numpy import percentile
# from pandas.api.types import is_string_dtype
# from io import StringIO
# import matplotlib.cm as cm

#############################functions that call csv or pandas df

def process_csv():
    table_name = get_csv_table()
    df_table = table_as_df (table_name)
    process_pandas_df(df_table)


def process_pandas_df(name_of_df):
    global record_count
    global column_name_list
    global number_of_variables
    global list_of_objects
    global df
    df = name_of_df
    record_count = count_records(df)
    column_name_list = name_of_variables(df)
    number_of_variables = count_var(df)
    list_of_objects = list_of_object(column_name_list, df)
    build_html()
    print("In this dataset, the number of variables is: ", number_of_variables)
    print("The number of records in the dataset is: ", record_count)
    print("This is a list with the names of the variables: ", column_name_list)


#######################################################
####################Importing Table from CSV###########
#######################################################

##input:  the name of the table
##output: a dataframe in pandas

"""a function that takes the input table and manipulate it for work"""
"""if the table is a csv, the user need to choose the spesific file from a directory with a browser"""

def get_csv_table ():
    filename = askopenfilename()
    return filename


def table_as_df (filename):
    df = pd.read_csv(filename, parse_dates = True, infer_datetime_format = True, date_parser = pd.to_datetime, encoding='UTF-8')
    #print("this is the database: ", df)                                       ###QA
    return df


#######################################################
####################Meta data for  the table################
#######################################################


################count the number of variables in a dataset############
##input: name of the dataset
##output: number of variables in the dataset

def count_var (df):
    number_of_variables = len(name_of_variables(df))
    #print("there are {} variables in the dataset".format(number_of_variables) )
    return  number_of_variables


######## count the number of the values in each variable not including NA

##input = df
##output = number of nun null records

def count_records (df):
    num_records = df.count()
    maximal_numer = max(num_records)
    #print("the number of records in the dataset is {}".format(maximal_numer))
    print(num_records)
    return maximal_numer


###############careat a list with the names of the variables from the original df##############
# create a list with the names of the variables from the original df
# input: name of the dataset
# output: a list of the names of the variables in the dataset

def name_of_variables (df):
    column_name_list = list(df)
    #print("column names: ", column_name_list)
    return column_name_list

#########################################################
####################directory for graphs#################
#########################################################

######create a directory for the graphs or use the graph directory if available

script_dir = os.path.dirname(__file__)
graph_dir = os.path.join(script_dir, 'Graphs_for_seenopsis/')

if not os.path.isdir(graph_dir):
    os.makedirs(graph_dir)


#########################################################
################seenopsis data to present################
#########################################################

"""Instances of the Class represents the different variables"""
####each variable will turn to an object (in the class VariableInfo) and the following are the object's methods:

class VariableInfo:
    def __init__(self, name, values, index):
        self.name = name
        self.values=values
        self.index = index


    def var_type (self):
        type_of_variable = np.dtype(df[self.name])
        return type_of_variable


    def type (self):
        if self.var_type() in ('int64', 'float64', 'int32', 'float32'):
            if self.values.nunique()== 1:
                return "single"
            elif self.values.nunique()== 2:
                return "binary"
            elif self.values.nunique()>2 and self.values.nunique()<=10:
                return "categorical"
            else:
                return "continuous"
        elif self.var_type() == 'object':
            if self.values.nunique()== 1:
                return "single"
            elif self.values.nunique()== 2:
                return "binary"
            elif self.values.nunique()> 2 and self.values.nunique()<=10:
                return "categorical"
            else:
                return "text or Date"
        else:
            return "text or Date"


    def mean_of_var (self):
        if self.type() == "continuous":
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


    def statistics (self):
        if self.type() == "continuous":
            return """
                    <td> Min: {}  
                    <br> Max: {} 
                    <br> Mean &plusmn SD: {} &plusmn {}  
                    <br> Median (IQR): {} ({}, {}) </td>""".format (self.minimum_of_var(),
                              self.maximum_of_var(),
                              self.mean_of_var(),
                              self.sd_of_var(),
                              self.median_of_var(),
                              self.lower_iqr(),
                              self.upper_iqr())

        elif self.type() == "categorical":
             return """
                    <td> Categorical Variable 
                    <br> {} unique values </td>""".format (self.unique_categories())

        elif self.type() == "binary":
            return """
                    <td> Binary variable 
                    <br> {}: {}% 
                    <br> {}: {}% </td>""".format (self.count_binary()[0][0],
                                                  self.count_binary()[0][1],
                                                  self.count_binary()[1][0],
                                                  self.count_binary()[1][1])
        elif self.type() == "single":
            return """<td> Single value 
                      <br> No Statisticc </td>"""

        else:
            return """
                    <td> Text/Date variable - 
                    <br> only top 10 values are presented 
                    <br> out of {} unique values </td>""".format(self.unique_categories())


    def count_null (self):
        name = self.name
        values = self.values
        number_of_null=values.isnull().sum()
        if number_of_null == 0:
            return "No Missing Values"
        else:
            percent_of_null = round((number_of_null/len(self.values)) *100,1)
            return ("N={} <br>{}%".format(number_of_null,  percent_of_null) ) ####this function returns the number of nulls in the variable


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
        plt.savefig(graph_dir + "hist_{}".format(self.index))
        plt.close()
        return self.index


    def pie (self):
        self.values.value_counts().plot(kind='pie')
        # plt.pie(self.values.dropna())    ######this returns n=array, bins, patch=Silent list of individual patches used to create the histogram
        plt.savefig(graph_dir + "pie_{}".format(self.index))
        plt.close()
        counts = self.values.value_counts()
        return self.index


    def bars (self):
        self.values.value_counts().nlargest(10).plot(kind='barh')
        plt.savefig(graph_dir + "bars_{}".format(self.index))
        plt.close()
        return self.index


    def count_binary (self):
        # unique, counts = np.unique(self.values, return_counts=True)
        # percentage = self.values.value_counts()/len(self.values)*100
        percentage_list = []
        count = self.values.value_counts()
        for name, count in count.items():
            percentage = round(count/len(self.values),3)*100
            sub_list = [name, percentage]
            percentage_list.append(sub_list)
            # (np.unique(self.values, return_counts=True)[1] / len(self.values)) * 100
        # counts, freq = self.values.value_counts(normalize=True)
        # percent = freq *100
        # return round(percentage,1)
        return percentage_list

    def unique_categories (self):
        unique_counts = self.values.nunique()
        return unique_counts

#######################################################
#######################OBJECTS#########################
#######################################################


"""creating a list of objects for the Variable class. Each object has to have:
#  1. a name - the name of the variable
#  2. The values of the variable
#  3. The index of the variable"""


def list_of_object(column_name_list, df_table):
    list_of_objects = []
    for index, variable in enumerate(column_name_list):
        name = variable
        values = df_table[name]  ##in pandas - this is how you get the values
        index=index
        list_of_objects.append(VariableInfo(name, values, index))
    return list_of_objects

#print("list of objects: ", list_of_objects)            #QA

#######################################################
####################Output Table#######################
#######################################################

##the output table is differential based on the types of the variables

##currently categorized  out put based on the types:

###if dtype is in (int64, float64):
#single variable - only one value
#binary - only 2 unique values (except for null)
#categorical - >2 and <=10 unique variables
#continuoues - >10 unique variables

####if dtype is object:
#single variable - only one value
#binary - 2 unique values (except for null)
#categorical - >2 and <= 10 unique variables
#text/date - >10 unique variables

####the categorization is executed while building the HTML


###########################################################
###############building the HTML###########################
###########################################################



##############need to deal with bool


""" a function that wrap everything nicely in an html table to display """


def build_html():
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
        <p>The file you are investing has {} records and {} variables <br>
        This is the seenopsis of your file:</p> 
        <table class="table table-hover"> 
            <thead>
            <tr align="left"> 
                <th>Variable Name</th>  
                <th >Type</th> 
                <th>Graphic Representation</th>
                <th>Basic Statistic</th>
                <th>Missing</th> 
                <th>Outliers (n)</th>  
            </tr></thead>""".format(record_count, number_of_variables)

    body_list = []
    for object in list_of_objects:
        if object.var_type() in ('int64', 'float64', 'int32', 'float32'):
            if object.values.nunique()== 1:
                list_for_body = """ <tr align="left">
                                    <th> {} </th>
                                    <td> Single Value </td>
                                    <td> <img src='Graphs_for_seenopsis/bars_{}.png' width='200' hight='200'> </img> </td>
                                    <td> Single value: 
                                    <br> No statistic </td>
                                    <td> {} </td>
                                    <td> Single Value: 
                                    <br>No outliers </td>
                                    </tr>""".format (object.name,
                                                  object.bars(),
                                                  object.count_null())
            elif object.values.nunique()== 2:
                list_for_body = """<tr align="left">
                                <th> {} </th>
                                <td> Binary Variable 
                                <br> (integer based)</td>
                                <td> <img src='Graphs_for_seenopsis/bars_{}.png' width='200' hight='200'> </img> </td>
                                <td> Binary variable 
                                <br> {}: {}% 
                                <br> {}: {}% </td>
                                <td> {} </td>
                                <td> Binary variable
                                <br>No outliers </ td>
                             </tr>""".format (object.name,
                                             object.bars(),
                                              object.count_binary()[0][0],
                                              object.count_binary()[0][1],
                                              object.count_binary()[1][0],
                                              object.count_binary()[1][1],
                                              object.count_null())
            elif object.values.nunique()>2 and object.values.nunique()<=10 :
                list_for_body = """<tr align="left">
                                <th> {} </th>
                                <td> Categorical Variable 
                                <br> (integer based) </td>
                                <td> <img src='Graphs_for_seenopsis/bars_{}.png' width='200' hight='200'> </img> </td>
                                <td> Categorical Variable 
                                <br> {} unique values </td>
                                <td> {} </td>
                                <td> Categorical Variable
                                <br>No outliers </td>
                             </tr>""".format (object.name,
                                              object.bars(),
                                              object.unique_categories(),
                                              object.count_null())
            else: list_for_body = """<tr align="left">
                                <th> {} </th>
                                <td> Continuous variable 
                                <br>({}) </td>
                                <td> <img src='Graphs_for_seenopsis/hist_{}.png' width ='200' hight='150'> </img> </td>
                                <td> Min: {} 
                                <br> Max: {} 
                                <br> Mean &plusmn SD: {} &plusmn {} 
                                <br> Median (IQR): {} ({}, {}) </td>
                                <td> {} </td>
                                <td> {} </td>
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
        elif object.var_type() == 'object':
            if object.values.nunique()== 1:
                list_for_body = """<tr align="left">
                                <th> {} </th>
                                <td> Single value</td>
                                <td> <img src='Graphs_for_seenopsis/bars_{}.png' width ='200' hight='150'> </img> </td>
                                <td> Single Value:
                                <br> No statistic </td> 
                                <td> {} </td>
                                <td> Single Value:
                                <br>No outliers </td>
                             </tr>""".format (object.name,
                                              object.bars(),
                                              object.count_null())
            elif object.values.nunique()== 2:
                list_for_body = """<tr align="left">
                                <th> {} </th>
                                <td> Binary Variable
                                <br> (text/date based) </td>
                                <td> <img src='Graphs_for_seenopsis/bars_{}.png' width ='200' hight='150'> </img> </td>
                                <td> Binary variable 
                                <br> {}: {}%
                                <br> {}: {}% </td>
                                <td> {} </td>
                                <td> Binary variable
                                <br>No outliers </td>
                             </tr >""".format (object.name,
                                              object.bars(),
                                              object.count_binary()[0][0],
                                              object.count_binary()[0][1],
                                              object.count_binary()[1][0],
                                              object.count_binary()[1][1],
                                              object.count_null())
            elif object.values.nunique()> 2 and object.values.nunique()<=10:
                list_for_body = """<tr align="left">
                                <th> {} </th>
                                <td> Categorical Variable 
                                <br> (text/date based) </td>
                                <td> <img src='Graphs_for_seenopsis/bars_{}.png' width ='200' hight='150'> </img> </td>
                                <td> Categorical variable
                                <br> {} unique values  
                                <td> {} </td>
                                <td> Categorical variable
                                <br>No outliers </td>
                                </tr>""".format (object.name,
                                             object.bars(),
                                             object.unique_categories(),
                                             object.count_null())
            else:
                list_for_body = """<tr align="left">
                                    <th> {} </th>
                                    <td> Text/Date variable </td>
                                    <td> <img src='Graphs_for_seenopsis/bars_{}.png' width ='200' hight='150'> </img> </td>
                                    <td> Text/Date variable - 
                                    <br> only top 10 values are presented 
                                    <br> out of {} unique values </td>
                                    <td> {} </td>
                                    <td> Text/Date variable
                                    <br>No outliers </td>
                                 </tr>""".format(object.name,
                                                 object.bars(),
                                                 object.unique_categories(),
                                                 object.count_null())
        else:
            list_for_body = """<tr align="left">
                                <th> {} </th>
                                <td> Text/Date variable </td>
                                <td> <img src='Graphs_for_seenopsis/bars_{}.png' width ='200' hight='150'> </img> </td>
                                <td> Text/Date variable - 
                                <br> only top 10 values are presented 
                                <br> out of {} unique values </td>
                                <td> {} </td>
                                <td> Text/Date variable
                                <br>No outliers </td>
                             </tr>""".format(object.name,
                                             object.bars(),
                                             object.unique_categories(),
                                             object.count_null())
        body_list.append(list_for_body)

    html_bottomn = """</table> 
                    <footer>&copy; Copyright 2018 Meytal Avgil Tsadok</footer>
                    </div></body>
                    </html>"""

    merged_html = html_top + "".join(body_list) +html_bottomn

    with open("output_seenopsis.html","w") as html_file:
        html_file.write(merged_html)
        html_file.close()

    with open("output_seenopsis.html","r") as html_file:
        Seenopsis_table = html_file.read()
        webbrowser.open_new_tab('output_seenopsis.html')
        html_file.close()




###############call seenopsis

####call seenopsis fron this file
# process_csv()
# process_pandas_df()

####call seenopsis from a different tab
# import seenopsis
# seenopsis.process_csv()
