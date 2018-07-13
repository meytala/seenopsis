from typing import Any, Union

from numpy.core.multiarray import ndarray

__author__ = "Meytal Avgil Tsadok"
__copyright__ = "Copyright 2018, TLV Israel"
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


# import shutil
# import pdfkit


#############################functions that call csv or pandas df

def process_csv():                                                                  ###a function that handle the csv file  - tranform it to pandas df
    csv_file_name = askopenfilename()
    df_table = convert_csv_to_pd(csv_file_name)
    process_pandas_df(df_table)


def process_pandas_df(name_of_pandas_df):                                           ###a function that take the pandas df and process it to an output table
    global record_count
    global column_name_list
    global number_of_variables
    global list_of_objects
    global df
    df = name_of_pandas_df
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)
    record_count = max(df.count())
    column_name_list = list(df)
    number_of_variables = len(column_name_list)
    list_of_objects = list_of_object(column_name_list, df)
    build_html()
    print("In this dataset, there are {} variables and {} observations".format(number_of_variables, record_count))


#######################################################
####################Importing Table from CSV###########
#######################################################

##input:  the name of the table
##output: a dataframe in pandas


def convert_csv_to_pd(csv_file_name):                                                 ###a function that take csv in spesific encodings and transfer it to df
    local_df = None
    for encoding in ['utf-8', 'UTF-8', 'ANSI', 'ISO-8859-1', 'ISO-8859-8']:
        try:
            local_df = pd.read_csv(csv_file_name, parse_dates=True, infer_datetime_format=True, date_parser=pd.to_datetime, encoding=encoding)
            print("The csv file is encoded with {}".format(encoding))
            break
        except UnicodeDecodeError:
            print("The csv file is not encoded with {}".format(encoding))
        except pd.errors.ParserError:
            print("Please use a csv file for your database")
    return local_df


#########################################################
####################directory for graphs#################
#########################################################
##create a directory for the graphs or use the graph directory if available

script_dir = os.path.dirname(__file__)                                              ###create a folder for storing the graphs in the active directory
graph_dir = os.path.join(script_dir, 'Graphs_for_seenopsis/')

if not os.path.isdir(graph_dir):  ###only if it doesn't exist already
    os.makedirs(graph_dir)

#########################################################
################seenopsis data to present################
#########################################################

"""Instances of the Class represents the different variables"""


####each variable will turn to an object (in the class VariableInfo) and the following are the object's methods:

class VariableInfo:
    def __init__(self, name, values, index):
        self.name = name
        self.values = values
        self.index = index

    def var_type(self):                                                             ### a variable that get the variable type based on numpy
        type_of_variable = np.dtype(self.values)
        return type_of_variable

    def type_for_operation(self):
        if self.var_type() in ('int64', 'float64', 'int32', 'float32'):
            if self.values.nunique() == 1:
                return "single number"
            elif self.values.nunique() == 2:
                return "binary number"
            elif 2 < self.values.nunique() <= 10:
                return "category number"
            else:
                return "continuous number"
        elif self.var_type() == 'object':
            if self.values.nunique() == 1:
                return "single text"
            elif self.values.nunique() == 2:
                return "binary text"
            elif 2 < self.values.nunique() <= 10:
                return "category text"
            else:
                return "general text"
        else:
            return "general text"

    def type(self):                                                                ### a function that subdivid the types for more accurate categories
        if self.var_type() in ('int64', 'float64', 'int32', 'float32'):
            if self.values.nunique() == 1:
                return "Single Variable\n" \
                       " ({})".format(self.var_type())
            elif self.values.nunique() == 2:
                return "Binary Variable\n" + \
                       " ({})".format(self.var_type())
            elif 2 < self.values.nunique() <= 10:
                return "Categorical variable\n" + \
                       " ({})".format(self.var_type())
            else:
                return "Continuous variable\n" + \
                       " ({})".format(self.var_type())
        elif self.var_type() == 'object':
            if self.values.nunique() == 1:
                return "Single Variable"
            elif self.values.nunique() == 2:
                return "Binary Variable"
            elif 2 < self.values.nunique() <= 10:
                return "Categorical variable"
            else:
                return "Text or Date"
        else:
            return "Text or Date"

    def histogram(self):                                                     ### a function that create a histogram with 50 bins/20%!!!
        plt.hist(self.values.dropna(), bins=50)
        plt.yticks(fontsize=14)
        plt.xticks(fontsize=14)
        plt.savefig(graph_dir + "hist_{}".format(self.index))
        plt.close()
        return "hist_{}.png".format(self.index)

    def bars(self):                                                                 ### a function that create an horisontal barchart
        self.values.value_counts().nlargest(10).plot(kind='barh')
        plt.yticks(fontsize=14)
        plt.xticks(fontsize=14)
        plt.savefig(graph_dir + "bars_{}".format(self.index))
        plt.close()
        return "bars_{}.png".format(self.index)

    def graph(self):                                                                ### a function that match the graph type to present based on the variable type
        my_type = self.type_for_operation()
        if my_type == "continuous number":
            return self.histogram()
        else:
            return self.bars()

    def mean_of_var(self):                                                          ### this function returns mean round to 2 decimal
        name = self.name
        mean = np.mean(self.values)
        # print("the mean of the column {} is {}".format (name, mean))
        return round(float(mean), 2)

    def median_of_var(self):                                                        ### this function returns median round to 2 decimal
        name = self.name
        median = np.nanmedian(self.values)
        # print("the median of the column {} is {}".format (name, median))
        return round(float(median), 2)

    def lower_iqr(self):                                                            ### this function returns the lower boundary of IQR
        name = self.name
        values = self.values
        low_iqr = np.nanpercentile(values, 25)
        return round(low_iqr, 2)

    def upper_iqr(self):                                                            ### this function returns the upper boundary of IQR
        name = self.name
        values = self.values
        up_iqr = np.nanpercentile(values, 75)
        return round(up_iqr, 2)

    def minimum_of_var(self):                                                       ### this function returns the minimal value of the variable
        name = self.name
        minimum = np.min(self.values)
        # print("the minimal value of column {} is {}".format (name, minimum))    ##QA
        return round(minimum, 2)

    def maximum_of_var(self):                                                       ### this function returns the maximal value of the variable
        name = self.name
        maximum = np.max(self.values)
        # print("the maximal value of column {} is {}".format (name, maximum))    ##QA
        return round(maximum, 2)

    def sd_of_var(self):                                                            ### this function returns the sd, round to 2 decimals
        name = self.name
        sd = np.std(self.values)
        # print("the std of column {} is {}".format (name, sd))        ##QA
        return round(float(sd), 2)

    def statistics(self):                                                                  ### this function returns what will be written in the statistic column - based on variable type
        if self.type_for_operation() == "continuous number":
            return ["Min: {}".format(self.minimum_of_var()),
                    "Max: {}".format(self.maximum_of_var()),
                    "Mean &plusmn SD: {} &plusmn {}".format(self.mean_of_var(), self.sd_of_var()),
                    "Median (IQR): {} ({}, {})".format(self.median_of_var(), self.lower_iqr(), self.upper_iqr())]

        elif "category" in self.type_for_operation():
            return ["Categorical Variable",
                    "{} unique values".format(self.unique_categories()),
                    "Up to top 10 values are presented"]

        elif "binary" in self.type_for_operation():
            return ["Binary variable",
                    "{}: {}%".format(self.count_binary()[0][0], self.count_binary()[0][1]),
                    "{}: {}%".format(self.count_binary()[1][0], self.count_binary()[1][1])]

        elif "unique" in self.type_for_operation():
            return ["Single value",
                    "No Statistics"]

        else:
            return ["Text/Date variable",
                    "Up to top 10 values are presented",
                    "Out of {} unique values".format(self.unique_categories())]

    def count_null(self):                                                            ### this function counts the nulls
        name = self.name
        values = self.values
        number_of_null = values.isnull().sum()
        if number_of_null == 0:
            return ["No missing",
                    "values"]
        else:
            percent_of_null = round((number_of_null / len(self.values)) * 100, 1)
            return [("N={}, {}%".format(number_of_null, percent_of_null))]

    def number_of_outliers(self, outlier_constant):                                       ### this function counts the number of outliers based on a distance of XX IQR
        if self.type_for_operation() == "continuous number":
            a = np.array(self.values)
            upper_quartile = np.nanpercentile(a, 75)
            lower_quartile = np.nanpercentile(a, 25)
            IQR = (upper_quartile - lower_quartile)
            extend_IQR = IQR * outlier_constant
            lower_boundary: Union[Union[int, float, complex, ndarray], Any] = lower_quartile - extend_IQR
            upper_boundary = upper_quartile + extend_IQR
            count = 0
            for y in a:
                if (y <= lower_boundary) or (y >= upper_boundary):
                    count += 1
            return ["N={}".format(count)]
        elif "category" in self.type_for_operation():
            return ["Categorical variable",
                    "No outlier"]
        elif "binary" in self.type_for_operation():
            return ["Binary variable",
                    "No outlier"]
        elif "single" in self.type_for_operation():
            return ["Single variable",
                    "No outlier"]
        else:
            return ["Text/Date variable",
                    "No outliers"]

    def count_binary(self):                                                         ### this function return a list of the percentage of the binary variables
        percentage_list = []
        count = self.values.value_counts()
        for name, count in count.items():
            percentage = round((count / len(self.values)) * 100, 2)
            sub_list = [name, percentage]
            percentage_list.append(sub_list)
        return percentage_list

    def unique_categories(self):                                                    ### this function return the number of unique values
        unique_counts = self.values.nunique()
        return unique_counts


#######################################################
#######################OBJECTS#########################
#######################################################

"""creating a list of objects for the Variable class. Each object has to have:
#  1. a name - the name of the variable
#  2. The values of the variable
#  3. The index of the variable"""

def list_of_object(column_name_list, df_table):                                                       ###this functin create a list of objects with the attributes of VariableInfo
    list_of_objects = []
    for index, name in enumerate(column_name_list):
        values = df_table[name]
        list_of_objects.append(VariableInfo(name, values, index))
    return list_of_objects


# print("list of objects: ", list_of_objects)            #QA


###########################################################
###############building the HTML###########################
###########################################################

""" a function that wrap everything nicely in an html table to display """


def build_html():
    html_top = """<html>
    <head>
       <title>SEENOPSIS</title>
       <meta charset="utf-8">
       <meta name="viewport" content="width=device-width, initial-scale=1">
       <link rel="stylesheet" href="bootstrap.min.css">
       <style>
          .bottom-bar{{
             background: #deede9;
          }}
          .navbar.bottom-bar{{
             border: none;
          }}
          .main-bg{{
             background-color: #FFFFFF;
         }}
          .single-row{{
             margin-bottom: 5px;
          }}
          .content-table td{{
             padding-bottom: 10px;
          }}
       </style>
    </head>
    <body class="main-bg">
    <div class="navbar-wrapper" >
       <div class="container main-bg">
          <div class="row  navbar-fixed-top">
             <div class="container main-bg" style="color: #1d576b">
            <h2>SEENOPSIS</h2> 
            <span>The file you are investing has {} variables for {} observations. <br>
            This is the seenopsis of your file:</span> 
            <br>
            <table class="table table-hover" style="margin-bottom:0px">
                <thead>
                <tr align="right" >
                    <th width="10%">Variable<br/>Name</th>
                      <th width="10%" >Type</th>
                      <th width="10%">Graphic<br/> Representation</th>
                      <th width="10%">Basic<br/> Statistics</th>
                      <th width="10%">Missing</th>
                      <th width="10%">Outliers (n)</th>
                </tr></thead></table>
             </div>
          </div>
       </div>
    </div> 
    <div class="container" style="padding-top:160px">
       <div class="row">
          <div class="container">
             <table class="content-table">
                <thead>
                <tr >
                   <th width="10%"></th>
                   <th width="10%"></th>
                   <th width="10%"></th>
                   <th width="10%"></th>
                   <th width="10%"></th>
                   <th width="10%"></th>
                </tr>
                </thead>""".format(number_of_variables, record_count)

    body_list = []
    for object in list_of_objects:
        list_for_body = """ 
        <tr align="left" class="single-row">
        <th width="10%"  align="left"> {} </th>
        <td width="10%" align="left"> {} </td>
        <td width="10%" align="left"> <img src='Graphs_for_seenopsis/{}' width='200' hight='200'> </img> </td>
        <td width="10%" align="left"> {} </td>
        <td width="10%" align="left"> {} </td>
        <td width="10%" align="left"> {} </td>
        <tr align="left" class="single-row">""".format \
            (object.name,
             object.type(),
             object.graph(),
             "<br>".join(object.statistics()),
             "<br>".join(object.count_null()),
             "<br>".join(object.number_of_outliers(3)))
        body_list.append(list_for_body)

    html_bottomn = """</tr>
         </table>
     <br />
     <br />
     <br />
      </div>
           <div class="navbar navbar-fixed-bottom bottom-bar" >
         <div class="container">
            <div class="nav navbar-nav pull-right ">
               <br/>
               <span style="color: #257D92">&copy; Copyright 2018 Meytal Avgil Tsadok</span>
                </div>
             </div>
          </div>
       </div>
    </div>
    </body>
    </html>"""

    merged_html = html_top + "".join(body_list) + html_bottomn

    with open("seenopsis_output.html", "w") as html_file:  ### write the html to a file
        html_file.write(merged_html)
        html_file.close()

    webbrowser.open_new_tab('seenopsis_output.html')




    # config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf.exe')
    #
    # with open('output_seenopsis.html') as pdf:
    #     pdfkit.from_file(pdf, 'seenopsis_pdf.pdf')

    # pdfkit.from_file("output_seenopsis.html", graph_dir +"seenopsis.pdf")

###############call seenopsis

####call seenopsis fron this file
# process_csv()
# process_pandas_df()

####call seenopsis from a different tab
# import seenopsis
# seenopsis.process_csv()
