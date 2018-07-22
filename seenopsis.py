__author__ = "Meytal Avgil Tsadok"
__copyright__ = "Copyright 2018, TLV Israel"
__credits__ = "She codes - Final project"
__version__ = "1.0.1"
__maintainer__ = "Meytal Avgil Tsadok"
__email__ = "meytala@gmail.com"
__status__ = "Production"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
from tkinter.filedialog import askopenfilename
import os
import sys


##########################################################################################
####### functions to process the df - based on the type of the df (csv or pandas)#########
##########################################################################################

def process_csv():
    csv_file_name = askopenfilename()
    pd_df = convert_csv_to_pd(csv_file_name)
    process_pandas_df(pd_df)


def process_pandas_df(pd_df):
    df = pd_df
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)
    record_count = max(df.count())
    column_name_list = list(df)
    number_of_variables = len(column_name_list)
    list_of_objects = get_list_of_objects(column_name_list, df)
    build_html(df)
    print("In this dataset, there are {} variables and {} observations".format(number_of_variables, record_count))


#########################################################
####### converting the CSV table to pandas df ###########
#########################################################

def convert_csv_to_pd(csv_file_name):
    pd_df = None
    for encoding in ['utf-8', 'UTF-8', 'ANSI', 'ISO-8859-1', 'ISO-8859-8']:
        try:
            pd_df = pd.read_csv(csv_file_name, parse_dates=True, infer_datetime_format=True,
                                    date_parser=pd.to_datetime, encoding=encoding)
            print("The csv file is encoded with {}".format(encoding))
            break
        except UnicodeDecodeError:
            pass
        except pd.errors.ParserError:
            print("Please use a csv file for your database (not excel), or encode with utf-8")
            sys.exit(1)
    return pd_df


#########################################################
#################### directory for graphs ###############
#########################################################
#create a directory for the graphs or use the graph directory if available

script_dir = os.path.dirname(__file__)
graph_dir = os.path.join(script_dir, 'Graphs_for_seenopsis/')

if not os.path.isdir(graph_dir):
    os.makedirs(graph_dir)


#########################################################################
############### The information to present in seenopsis: ################
#########################################################################

#create a class named VariableInfo with different method to represent featurs of the datasets' variables
#each variable in the dataset will turn to an object

class VariableInfo:
    def __init__(self, name, values, index):
        self.name = name
        self.values = values
        self.index = index


    def var_type(self):  ### get the variable type based on numpy
        type_of_variable = np.dtype(self.values)
        return type_of_variable


    def type_for_operation(self):  ###subdivide the variable type to single, binary, category, continuous, test/date
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


    def type(self):  ### variables' type in a format to be presented nicely in the seenopsis output
        if "single" in self.type_for_operation():
            return "Single Variable\n" \
                   "({})".format(self.var_type())
        elif "binary" in self.type_for_operation():
            return "Binary Variable\n" + \
                   "({})".format(self.var_type())
        elif "category" in self.type_for_operation():
            return "Categorical Variable\n" + \
                   "({})".format(self.var_type())
        elif "continuous number" in self.type_for_operation():
            return "Continuous Variable\n" + \
                   "({})".format(self.var_type())
        else:
            return "Text or Date"


    def histogram(self):
        plt.hist(self.values.dropna(), bins=50)
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)
        plt.savefig(graph_dir + "hist_{}".format(self.index))
        plt.close()
        return "hist_{}.png".format(self.index)


    def bars(self):
        self.values.value_counts().nlargest(10).plot(kind='barh')
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=14)
        plt.savefig(graph_dir + "bars_{}".format(self.index))
        plt.close()
        return "bars_{}.png".format(self.index)


    def create_hist_or_bars_graph(self):
        if "continuous number" in self.type_for_operation():
            return self.histogram()
        else:
            return self.bars()


    def mean_of_var(self):
        mean = np.nanmean(self.values)
        return round(float(mean), 2)


    def median_of_var(self):
        median = np.nanmedian(self.values)
        return round(float(median), 2)


    def lower_iqr(self):
        values = self.values
        low_iqr = np.nanpercentile(values, 25)
        return round(float(low_iqr), 2)


    def upper_iqr(self):
        values = self.values
        up_iqr = np.nanpercentile(values, 75)
        return round(float(up_iqr), 2)


    def minimum_of_var(self):
        minimum = np.nanmin(self.values)
        return round(float(minimum), 2)


    def maximum_of_var(self):
        maximum = np.nanmax(self.values)
        return round(float(maximum), 2)


    def sd_of_var(self):
        sd = np.nanstd(self.values)
        return round(float(sd), 2)


    def count_binary(self):  ### return a list of the percentage for binary variables
        percentage_list = []
        count = self.values.value_counts()
        for name, count in count.items():
            percentage = round((count / len(self.values)) * 100, 2)
            sub_list = [name, percentage]
            percentage_list.append(sub_list)
        return percentage_list


    def count_unique_values(self):
        unique_counts = self.values.nunique()
        return unique_counts


    def statistics(self):  ### returns what will be written in the statistic column of seenopsis- based on variable type
        if self.type_for_operation() == "continuous number":
            return ["Min: {}".format(self.minimum_of_var()),
                    "Max: {}".format(self.maximum_of_var()),
                    "Mean &plusmn SD: {} &plusmn {}".format(self.mean_of_var(), self.sd_of_var()),
                    "Median (IQR): {} ({}, {})".format(self.median_of_var(), self.lower_iqr(), self.upper_iqr())]

        elif "category" in self.type_for_operation():
            return ["Categorical Variable",
                    "{} unique values".format(self.count_unique_values()),
                    "Up to top 10 values are presented"]

        elif "binary" in self.type_for_operation ():
            return ["Binary variable",
                    "{}: {}%".format(self.count_binary()[0][0], self.count_binary()[0][1]),
                    "{}: {}%".format(self.count_binary()[1][0], self.count_binary()[1][1])]

        elif "single" in self.type_for_operation():
            return ["Single value",
                    "No Statistics"]

        else:
            return ["Text/Date variable",
                    "Up to top 10 values are presented",
                    "Out of {} unique values".format(self.count_unique_values())]


    def count_null(self):
        number_of_null = self.values.isnull().sum()
        if number_of_null == 0:
            return ["No missing",
                    "values"]
        else:
            percent_of_null = round((number_of_null / len(self.values)) * 100, 1)
            return [("N={}, {}%".format(number_of_null, percent_of_null))]


    def number_of_outliers(self, outlier_constant):
        if self.type_for_operation() == "continuous number":
            a = np.array(self.values)
            upper_quartile = np.nanpercentile(a, 75)
            lower_quartile = np.nanpercentile(a, 25)
            iqr = (upper_quartile - lower_quartile)
            extend_iqr = iqr * outlier_constant
            lower_boundary = lower_quartile - extend_iqr
            upper_boundary = upper_quartile + extend_iqr
            count = 0
            if iqr == 0:
                return ["IQR=0",
                        "Outliers were not analyzed"]
            else:
                for y in a:
                    if (y <= lower_boundary) or (y >= upper_boundary):
                        count += 1
                return ["N={}".format(count)]
        elif "category" in self.type_for_operation():
            return ["Categorical variable",
                    "No outliers"]
        elif "binary" in self.type_for_operation():
            return ["Binary variable",
                    "No outliers"]
        elif "single" in self.type_for_operation():
            return ["Single variable",
                    "No outliers"]
        else:
            return ["Text/Date variable",
                    "No outliers"]




###########################################################################
###### Transform variable in the dataset to a VariableInfo object #########
###########################################################################

def get_list_of_objects(column_name_list, df_table):
    list_of_objects = []
    for index, name in enumerate(column_name_list):
        values = df_table[name]
        list_of_objects.append(VariableInfo(name, values, index))
    return list_of_objects


###########################################################
############## Building the HTML ##########################
###########################################################

def build_html(df):
    column_name_list = list(df)
    record_count = max(df.count())
    number_of_variables = len(column_name_list)
    list_of_objects = get_list_of_objects(column_name_list, df)
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
                      <th width="10%">Missing<br/> (N, %)</th>
                      <th width="10%">Outliers (N)<br/>(Median &plusmn 3 IQR) </th>
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
        <tr align="left" class="single-row">""".format\
            (object.name,
             object.type(),
             object.create_hist_or_bars_graph(),
             "<br>".join(object.statistics()),
             "<br>".join(object.count_null()),
             "<br>".join(object.number_of_outliers(3)))
        body_list.append(list_for_body)

    html_bottom = """</tr>
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

    merged_html = html_top + "".join(body_list) + html_bottom

    with open("seenopsis_output.html", "w") as html_file:
        html_file.write(merged_html)
        html_file.close()

    webbrowser.open_new_tab('seenopsis_output.html')


###########################################################
#############  call seenopsis  ############################
###########################################################

####call seenopsis
# process_csv()
# process_pandas_df()
